#include <algorithm>
#include <filesystem>
#include <numeric>
#include <string>
#include <tuple>
namespace fs = std::filesystem;

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"
using namespace fwlite;

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Scouting/interface/Run3ScoutingMuon.h"
#include "DataFormats/Scouting/interface/Run3ScoutingPFJet.h"
#include "DataFormats/Scouting/interface/Run3ScoutingParticle.h"
#include "DataFormats/Scouting/interface/Run3ScoutingVertex.h"

#include "TFile.h"
#include "TLorentzVector.h"
#include "TMath.h"
#include "TRandom3.h"
#include "TString.h"
#include "TTree.h"

#include "tools/dorky.h"
#include "tools/goodrun.h"
#include "tools/tqdm.h"

// Partial unblinding
bool doPartialUnblinding = true;
float partialUnblindingPercentage = 0.1; // 10% of each era

// SV selection
bool relaxedSVSel = false;
float sfSVsel = (relaxedSVSel) ? 5.0 : 1.0;
float maxXerr=0.05*sfSVsel, maxYerr=0.05*sfSVsel, maxZerr=0.10*sfSVsel, maxChi2=3.0*sfSVsel;
float maxDXYerr=0.05*sfSVsel, maxD3Derr=0.10*sfSVsel; // for identification of overlapping SVs

template<class T>
const T getObject(const Event& ev, const char* prodLabel, const char* outLabel = "") {
  Handle<T> obj;
  obj.getByLabel(ev,prodLabel,outLabel);
  return *obj.product();
}

template <typename T, typename Compare>
std::vector<std::size_t> sort_permutation(const std::vector<T>& vec, Compare compare) {
  std::vector<std::size_t> p(vec.size());
  std::iota(p.begin(), p.end(), 0);
  std::sort(p.begin(), p.end(), [&](std::size_t i, std::size_t j){ return compare(vec[i], vec[j]); });
  return p;
}

template <typename T>
void apply_permutation_in_place(std::vector<T>& vec, const std::vector<std::size_t>& p) {
  std::vector<bool> done(vec.size());
  for (std::size_t i=0; i<vec.size(); ++i) {
    if (done[i])
      continue;
    done[i] = true;
    std::size_t prev_j = i;
    std::size_t j = p[i];
    while (i != j) {
      std::swap(vec[prev_j], vec[j]);
      done[j] = true;
      prev_j = j;
      j = p[j];
    }
  }
}


float getMiniIsoDR(const TLorentzVector muVec, const float minDR=0.05, const float maxDR=0.2, const float kt=10.0) {
  return std::min(maxDR, std::max(minDR, kt/(float)muVec.Pt()));
}

std::tuple<float,float,float,float,float> getPFIsolation(const TLorentzVector muVec, const std::vector<Run3ScoutingParticle>& pfs, const float maxDR=0.3, const float vetoDR=0.01, const float maxdz=0.1,const bool doMini=false, const bool doMindrMuPF=true) {
  float maxdr, mindrMuPF=1e6;
  float chIso=0, nhIso=0, phIso=0, puIso=0;
  if (doMini)
    maxdr = getMiniIsoDR(muVec);
  for (auto pf : pfs) {
    TLorentzVector pfvec;
    pfvec.SetPtEtaPhiM(pf.pt(),pf.eta(),pf.phi(),0.0);
    float dr = muVec.DeltaR(pfvec);
    if (dr<mindrMuPF)
      mindrMuPF = dr;
    if (dr<vetoDR || dr>maxDR)
      continue;
    bool fromPV = !(abs(pf.vertex())>0 || pf.dz()>maxdz);
    bool isCh=false, isNh=false, isPh=false, isPU=false;
    if (fabs(pf.pdgId())==211) {
      if (fromPV) {
        isCh = true;
        chIso = chIso + pf.pt();
      }
      else {
        isPU = true;
        puIso = puIso + pf.pt();
      }
    }
    if (fabs(pf.pdgId())==130) {
      isNh  = true;
      nhIso = nhIso + pf.pt();
    }
    if (fabs(pf.pdgId())==22) {
      isPh  = true;
      phIso = phIso + pf.pt();
    }
  }
  if (doMindrMuPF)
    return {chIso,nhIso,phIso,puIso,mindrMuPF};
  else
    return {chIso,nhIso,phIso,puIso,1e6};
}

std::tuple<float,float,float> get_track_reference_point(const Run3ScoutingMuon& mu, const float dxyCorr) {
  const auto phi = mu.phi();
  const auto dsz = mu.trk_dsz();
  const auto dz = mu.trk_dz();
  const auto lmb = mu.trk_lambda();

  const auto sinphi = TMath::Sin(phi);
  const auto cosphi = TMath::Cos(phi);
  const auto sinlmb = TMath::Sin(lmb);
  const auto tanlmb = sinlmb/TMath::Cos(lmb);

  float refz = 1.0*dz;
  float refx = -sinphi*dxyCorr - (cosphi/sinlmb)*dsz + (cosphi/tanlmb)*refz;
  float refy =  cosphi*dxyCorr - (sinphi/sinlmb)*dsz + (sinphi/tanlmb)*refz;

  return {refx,refy,refz};
}

float recalculate_phi_at_DV(
  float refx, float refy, float refz, // initial position in cm
  float px, float py, float pz, // initial momentum in GeV
  int charge, // -1 or 1, matches Muon_charge
  float dvx, float dvy // DV coordinates to propagate to
  ) {
  // Performs a helix propagation from 
  // track reference point (initial position)
  // to cylinder containing DV x,y, and then reports
  // the updated phi coordinate the the muon at that point
  float B = 3.8; // b field in Tesla
  float mass = 0.10566; // muon mass in GeV
  float c = 0.29979; // speed of light in m/ns

  float P = pow(px*px + py*py + pz*pz, 0.5);
  float Pxy = pow(px*px + py*py, 0.5);
  float E = pow(P*P + mass*mass, 0.5);

  // relativistic velocities
  float vx = px/E * c;
  float vy = py/E * c;
  float vz = pz/E * c;
  float vxy = pow(vx*vx + vy*vy, 0.5);

  // larmor radius/angular frequency
  float R = 1e3*Pxy/(3.*charge*B);
  float w = vxy/R;

  float t = 0.;
  float curr_x = refx;
  float curr_y = refy;
  float current_rho = -1;
  float target_rho = pow(dvx*dvx + dvy*dvy, 0.5);
  float dt = 0.1;
  int nsteps = 0;
  while(current_rho < target_rho) {
      curr_x = refx + (vy/w)*( 1-TMath::Cos(w*t)) + (vx/w)*TMath::Sin(w*t);
      curr_y = refy + (vx/w)*(-1+TMath::Cos(w*t)) + (vy/w)*TMath::Sin(w*t);
      current_rho = pow(curr_x*curr_x + curr_y*curr_y, 0.5);
      t += dt;
      nsteps++;
      if (nsteps > 10000) {
          //std::cout << "Warning, >10000 steps in propagate_to_cylinder" << std::endl;
          break;
      }
  }
  float curr_vx = vy*TMath::Sin(w*t) + vx*TMath::Cos(w*t);
  float curr_vy = vy*TMath::Cos(w*t) - vx*TMath::Sin(w*t);
  float newphi = atan2(curr_vy, curr_vx);
  return newphi;
}

float getCorrectedPhi(const Run3ScoutingMuon& mu, const TLorentzVector muVec, const float dxyCorr, const float bestSVPosition_x, const float bestSVPosition_y) {
  const auto refs = get_track_reference_point(mu, dxyCorr);
  const auto refx = std::get<0>(refs);
  const auto refy = std::get<1>(refs);
  const auto refz = std::get<2>(refs);
  float phiCorr = recalculate_phi_at_DV(refx, refy, refz, muVec.Px(), muVec.Py(), muVec.Pz(), mu.charge(), bestSVPosition_x, bestSVPosition_y);
  return phiCorr;
}


struct GenPart {
  std::vector<float> pt, eta, phi, m;
  std::vector<float> vx, vy, vz, lxy;
  std::vector<int> status, index, pdgId, motherIndex, motherPdgId;

  void clear() {
    pt.clear(); eta.clear(); phi.clear(); m.clear();
    vx.clear(); vy.clear(); vz.clear(); lxy.clear();
    status.clear(); index.clear(); pdgId.clear(); motherIndex.clear(); motherPdgId.clear();
  }
};

struct SV {
  std::vector<unsigned int> index, ndof;
  std::vector<float> x, y, z;
  std::vector<float> xe, ye, ze;
  std::vector<float> chi2, prob, chi2Ndof;
  std::vector<float> lxy, l3d;
  std::vector<float> mindx, mindy, mindz, mindxy, mind3d;
  std::vector<float> maxdx, maxdy, maxdz, maxdxy, maxd3d;
  std::vector<bool> selected;
  std::vector<bool> onModule, onModuleWithinUnc;
  std::vector<float> closestDet_x, closestDet_y, closestDet_z;
  std::vector<float> minDistanceFromDet, minDistanceFromDet_x, minDistanceFromDet_y, minDistanceFromDet_z;

  void clear() {
    index.clear(); ndof.clear();
    x.clear(); y.clear(); z.clear();
    xe.clear(); ye.clear(); ze.clear();
    chi2.clear(); prob.clear(); chi2Ndof.clear();
    lxy.clear(); l3d.clear();
    mindx.clear(); mindy.clear(); mindz.clear(); mindxy.clear(); mind3d.clear();
    maxdx.clear(); maxdy.clear(); maxdz.clear(); maxdxy.clear(); maxd3d.clear();
    selected.clear();
    onModule.clear(); onModuleWithinUnc.clear();
    closestDet_x.clear(); closestDet_y.clear(); closestDet_z.clear();
    minDistanceFromDet.clear(), minDistanceFromDet_x.clear(), minDistanceFromDet_y.clear(), minDistanceFromDet_z.clear();
  }

  void sort() {
    auto comp = sort_permutation(prob, [](float const& a, float const& b){ return a > b; }); // Define permutations based on the prob vector
    // Apply the permutation to all vectors
    apply_permutation_in_place(index, comp);
    apply_permutation_in_place(ndof, comp);
    apply_permutation_in_place(x, comp);
    apply_permutation_in_place(y, comp);
    apply_permutation_in_place(z, comp);
    apply_permutation_in_place(xe, comp);
    apply_permutation_in_place(ye, comp);
    apply_permutation_in_place(ze, comp);
    apply_permutation_in_place(chi2, comp);
    apply_permutation_in_place(prob, comp);
    apply_permutation_in_place(chi2Ndof, comp);
    apply_permutation_in_place(lxy, comp);
    apply_permutation_in_place(l3d, comp);
    apply_permutation_in_place(mindx, comp);
    apply_permutation_in_place(mindy, comp);
    apply_permutation_in_place(mindz, comp);
    apply_permutation_in_place(mindxy, comp);
    apply_permutation_in_place(mind3d, comp);
    apply_permutation_in_place(maxdx, comp);
    apply_permutation_in_place(maxdy, comp);
    apply_permutation_in_place(maxdz, comp);
    apply_permutation_in_place(maxdxy, comp);
    apply_permutation_in_place(maxd3d, comp);
    apply_permutation_in_place(selected, comp);
    apply_permutation_in_place(onModule, comp);
    apply_permutation_in_place(onModuleWithinUnc, comp);
    apply_permutation_in_place(closestDet_x, comp);
    apply_permutation_in_place(closestDet_y, comp);
    apply_permutation_in_place(closestDet_z, comp);
  }
};

struct SVOverlap {
  std::vector<std::vector<unsigned int>> vtxIdxs;
  std::vector<float> x, y, z;
  std::vector<float> lxy, l3d;

  void clear() {
    vtxIdxs.clear();
    x.clear(); y.clear(); z.clear();
    lxy.clear(); l3d.clear();
  }
};

float MUON_MASS = 0.10566;

bool isGlobalMuon(const unsigned int type) {
  return type & (1<<1);
}

bool isTrackerMuon(const unsigned int type) {
  return type & (1<<2);
}

bool isStandAloneMuon(const unsigned int type) {
  return type & (1<<3);
}

struct Muon {
  std::vector<std::vector<int>> vtxIdxs;
  std::vector<unsigned int> saHits, saMatchedStats;
  std::vector<unsigned int> muHits, muChambs, muCSCDT, muMatch, muMatchedStats, muExpMatchedStats, muMatchedRPC;
  std::vector<unsigned int> pixHits, stripHits;
  std::vector<unsigned int> pixLayers, trkLayers;
  std::vector<int> bestAssocSVIdx, bestAssocSVOverlapIdx;
  std::vector<int> ch;
  std::vector<int> isGlobal, isTracker, isStandAlone;
  std::vector<float> pt, eta, phi;
  std::vector<float> chi2Ndof;
  std::vector<float> ecalIso, hcalIso, trackIso;
  std::vector<float> ecalRelIso, hcalRelIso, trackRelIso;
  std::vector<float> dxy, dxye, dz, dze;
  std::vector<float> dxysig, dzsig;
  std::vector<float> phiCorr, dxyCorr;
  std::vector<float> PFIsoChg0p3, PFIsoChg0p4, PFIsoAll0p3, PFIsoAll0p4;
  std::vector<float> PFRelIsoChg0p3, PFRelIsoChg0p4, PFRelIsoAll0p3, PFRelIsoAll0p4;
  std::vector<float> mindrPF0p3, mindrPF0p4;
  std::vector<float> mindr, maxdr;
  std::vector<float> mindrJet, mindphiJet, mindetaJet;
  std::vector<TLorentzVector> vec;
  std::vector<bool> selected;
  std::vector<int> nhitsbeforesv, ncompatible, ncompatibletotal, nexpectedhits, nexpectedhitsmultiple, nexpectedhitsmultipletotal, nexpectedhitstotal;

  void clear() {
  vtxIdxs.clear();
  saHits.clear(); saMatchedStats.clear();
  muHits.clear(); muChambs.clear(); muCSCDT.clear(); muMatch.clear(); muMatchedStats.clear(); muExpMatchedStats.clear(); muMatchedRPC.clear();
  pixHits.clear(); stripHits.clear();
  pixLayers.clear(); trkLayers.clear();
  bestAssocSVIdx.clear(); bestAssocSVOverlapIdx.clear();
  ch.clear();
  isGlobal.clear(); isTracker.clear(); isStandAlone.clear();
  pt.clear(); eta.clear(); phi.clear();
  chi2Ndof.clear();
  ecalIso.clear(); hcalIso.clear(); trackIso.clear();
  ecalRelIso.clear(); hcalRelIso.clear(); trackRelIso.clear();
  dxy.clear(); dxye.clear(); dz.clear(); dze.clear();
  dxysig.clear(); dzsig.clear();
  phiCorr.clear(); dxyCorr.clear();
  PFIsoChg0p3.clear(); PFIsoAll0p3.clear();
  PFRelIsoChg0p3.clear(); PFRelIsoAll0p3.clear();
  PFIsoChg0p4.clear(); PFIsoAll0p4.clear();
  PFRelIsoChg0p4.clear(); PFRelIsoAll0p4.clear();
  mindrPF0p3.clear(); mindrPF0p4.clear();
  mindr.clear(); maxdr.clear();
  mindrJet.clear(); mindphiJet.clear(); mindetaJet.clear();
  vec.clear();
  selected.clear();
  nhitsbeforesv.clear(); ncompatible.clear(); ncompatibletotal.clear(); nexpectedhits.clear(); nexpectedhitsmultiple.clear(); nexpectedhitsmultipletotal.clear(); nexpectedhitstotal.clear();
  }

  void sort() {
    auto comp = sort_permutation(pt, [](float const& a, float const& b){ return a > b; }); // Define permutations based on the prob vector
    // Apply the permutation to all vectors
    apply_permutation_in_place(vtxIdxs, comp);
    apply_permutation_in_place(saHits, comp);
    apply_permutation_in_place(saMatchedStats, comp);
    apply_permutation_in_place(muHits, comp);
    apply_permutation_in_place(muChambs, comp);
    apply_permutation_in_place(muCSCDT, comp);
    apply_permutation_in_place(muMatch, comp);
    apply_permutation_in_place(muMatchedStats, comp);
    apply_permutation_in_place(muExpMatchedStats, comp);
    apply_permutation_in_place(muMatchedRPC, comp);
    apply_permutation_in_place(pixHits, comp);
    apply_permutation_in_place(stripHits, comp);
    apply_permutation_in_place(pixLayers, comp);
    apply_permutation_in_place(trkLayers, comp);
    apply_permutation_in_place(bestAssocSVIdx, comp);
    apply_permutation_in_place(bestAssocSVOverlapIdx, comp);
    apply_permutation_in_place(ch, comp);
    apply_permutation_in_place(isGlobal, comp);
    apply_permutation_in_place(isTracker, comp);
    apply_permutation_in_place(isStandAlone, comp);
    apply_permutation_in_place(pt, comp);
    apply_permutation_in_place(eta, comp);
    apply_permutation_in_place(phi, comp);
    apply_permutation_in_place(chi2Ndof, comp);
    apply_permutation_in_place(ecalIso, comp);
    apply_permutation_in_place(hcalIso, comp);
    apply_permutation_in_place(trackIso, comp);
    apply_permutation_in_place(ecalRelIso, comp);
    apply_permutation_in_place(hcalRelIso, comp);
    apply_permutation_in_place(trackRelIso, comp);
    apply_permutation_in_place(dxy, comp);
    apply_permutation_in_place(dxye, comp);
    apply_permutation_in_place(dz, comp);
    apply_permutation_in_place(dze, comp);
    apply_permutation_in_place(dxysig, comp);
    apply_permutation_in_place(dzsig, comp);
    apply_permutation_in_place(phiCorr, comp);
    apply_permutation_in_place(dxyCorr, comp);
    apply_permutation_in_place(PFIsoChg0p3, comp);
    apply_permutation_in_place(PFIsoAll0p3, comp);
    apply_permutation_in_place(PFRelIsoChg0p3, comp);
    apply_permutation_in_place(PFRelIsoAll0p3, comp);
    apply_permutation_in_place(mindrPF0p3, comp);
    apply_permutation_in_place(PFIsoChg0p4, comp);
    apply_permutation_in_place(PFIsoAll0p4, comp);
    apply_permutation_in_place(PFRelIsoChg0p4, comp);
    apply_permutation_in_place(PFRelIsoAll0p4, comp);
    apply_permutation_in_place(mindrPF0p4, comp);
    apply_permutation_in_place(mindr, comp);
    apply_permutation_in_place(maxdr, comp);
    apply_permutation_in_place(mindrJet, comp);
    apply_permutation_in_place(mindphiJet, comp);
    apply_permutation_in_place(mindetaJet, comp);
    apply_permutation_in_place(vec, comp);
    apply_permutation_in_place(selected, comp);
    apply_permutation_in_place(nhitsbeforesv, comp);
    apply_permutation_in_place(ncompatible, comp);
    apply_permutation_in_place(ncompatibletotal, comp);
    apply_permutation_in_place(nexpectedhits, comp);
    apply_permutation_in_place(nexpectedhitsmultiple, comp);
    apply_permutation_in_place(nexpectedhitsmultipletotal, comp);
    apply_permutation_in_place(nexpectedhitstotal, comp);
  }
};


void run3ScoutingLooper(std::vector<TString> inputFiles, TString year, TString process, const char* outdir="temp_data", TString label="") {
  // Output folders and files
  fs::create_directory(outdir);
  fs::permissions(outdir,fs::perms::owner_all | fs::perms::group_read | fs::perms::group_exec | fs::perms::others_read | fs::perms::others_exec);
  TFile* fout = new TFile(TString(outdir)+"/output_"+process+"_"+year+label+".root", "RECREATE");
  TTree* tout = new TTree("tout","Run3ScoutingTree");

  // Branch variables
  unsigned int run, lumi, evtn;
  bool passL1, passHLT;
  float nPV, PV_x, PV_y, PV_z;
  GenPart GenParts;
  SV SVs;
  SVOverlap SVOverlaps;
  int nMuonAssoc;
  Muon Muons;
  TFile *file0 = TFile::Open(inputFiles[0]);
  Event ev0(file0);
  ev0.toBegin();
  auto l1Names = getObject<std::vector<std::string>>(ev0, "triggerMaker", "l1name");
  bool l1fired[l1Names.size()] = {false};

  // Branch definition
  tout->Branch("run", &run);
  tout->Branch("lumi", &lumi);
  tout->Branch("evtn", &evtn);

  tout->Branch("passL1", &passL1);
  for (unsigned int iL1=0; iL1<l1Names.size(); ++iL1) {
    tout->Branch(TString(l1Names[iL1]), &l1fired[iL1]);
  }
  tout->Branch("passHLT", &passHLT);

  tout->Branch("nPV", &nPV);
  tout->Branch("PV_x", &PV_x);
  tout->Branch("PV_y", &PV_y);
  tout->Branch("PV_z", &PV_z);

  tout->Branch("GenPart_pt", &GenParts.pt);
  tout->Branch("GenPart_eta", &GenParts.eta);
  tout->Branch("GenPart_phi", &GenParts.phi);
  tout->Branch("GenPart_m", &GenParts.m);
  tout->Branch("GenPart_vx", &GenParts.vx);
  tout->Branch("GenPart_vy", &GenParts.vy);
  tout->Branch("GenPart_vz", &GenParts.vz);
  tout->Branch("GenPart_lxy", &GenParts.lxy);
  tout->Branch("GenPart_status", &GenParts.status);
  tout->Branch("GenPart_index", &GenParts.index);
  tout->Branch("GenPart_pdgId", &GenParts.pdgId);
  tout->Branch("GenPart_motherIndex", &GenParts.motherIndex);
  tout->Branch("GenPart_motherPdgId", &GenParts.motherPdgId);

  tout->Branch("SV_index", &SVs.index);
  tout->Branch("SV_ndof", &SVs.ndof);
  tout->Branch("SV_x", &SVs.x);
  tout->Branch("SV_y", &SVs.y);
  tout->Branch("SV_z", &SVs.z);
  tout->Branch("SV_xe", &SVs.xe);
  tout->Branch("SV_ye", &SVs.ye);
  tout->Branch("SV_ze", &SVs.ze);
  tout->Branch("SV_chi2", &SVs.chi2);
  tout->Branch("SV_prob", &SVs.prob);
  tout->Branch("SV_chi2Ndof", &SVs.chi2Ndof);
  tout->Branch("SV_lxy", &SVs.lxy);
  tout->Branch("SV_l3d", &SVs.l3d);
  tout->Branch("SV_mindx", &SVs.mindx);
  tout->Branch("SV_mindy", &SVs.mindy);
  tout->Branch("SV_mindz", &SVs.mindz);
  tout->Branch("SV_maxdx", &SVs.maxdx);
  tout->Branch("SV_maxdy", &SVs.maxdy);
  tout->Branch("SV_maxdz", &SVs.maxdz);
  tout->Branch("SV_selected", &SVs.selected);
  tout->Branch("SV_onModule", &SVs.onModule);
  tout->Branch("SV_onModuleWithinUnc", &SVs.onModuleWithinUnc);
  tout->Branch("SV_closestDet_x", &SVs.closestDet_x);
  tout->Branch("SV_closestDet_y", &SVs.closestDet_y);
  tout->Branch("SV_closestDet_z", &SVs.closestDet_z);
  tout->Branch("SV_minDistanceFromDet", &SVs.minDistanceFromDet);
  tout->Branch("SV_minDistanceFromDet_x", &SVs.minDistanceFromDet_x);
  tout->Branch("SV_minDistanceFromDet_y", &SVs.minDistanceFromDet_y);
  tout->Branch("SV_minDistanceFromDet_z", &SVs.minDistanceFromDet_z);

  tout->Branch("SVOverlap_vtxIdxs", &SVOverlaps.vtxIdxs);
  tout->Branch("SVOverlap_x", &SVOverlaps.x);
  tout->Branch("SVOverlap_y", &SVOverlaps.y);
  tout->Branch("SVOverlap_z", &SVOverlaps.z);
  tout->Branch("SVOverlap_lxy", &SVOverlaps.lxy);
  tout->Branch("SVOverlap_l3d", &SVOverlaps.l3d);

  tout->Branch("nMuonAssoc", &nMuonAssoc);
  tout->Branch("Muon_vtxIdxs", &Muons.vtxIdxs);
  tout->Branch("Muon_saHits", &Muons.saHits);
  tout->Branch("Muon_saMatchedStats", &Muons.saMatchedStats);
  tout->Branch("Muon_muHits", &Muons.muHits);
  tout->Branch("Muon_muChambs", &Muons.muChambs);
  tout->Branch("Muon_muCSCDT", &Muons.muCSCDT);
  tout->Branch("Muon_muMatch", &Muons.muMatch);
  tout->Branch("Muon_muMatchedStats", &Muons.muMatchedStats);
  tout->Branch("Muon_muExpMatchedStats", &Muons.muExpMatchedStats);
  tout->Branch("Muon_muMatchedRPC", &Muons.muMatchedRPC);
  tout->Branch("Muon_pixHits", &Muons.pixHits);
  tout->Branch("Muon_stripHits", &Muons.stripHits);
  tout->Branch("Muon_pixLayers", &Muons.pixLayers);
  tout->Branch("Muon_trkLayers", &Muons.trkLayers);
  tout->Branch("Muon_pt", &Muons.pt);
  tout->Branch("Muon_eta", &Muons.eta);
  tout->Branch("Muon_phi", &Muons.phi);
  tout->Branch("Muon_ch", &Muons.ch);
  tout->Branch("Muon_bestAssocSVIdx", &Muons.bestAssocSVIdx);
  tout->Branch("Muon_bestAssocSVOverlapIdx", &Muons.bestAssocSVOverlapIdx);
  tout->Branch("Muon_isGlobal", &Muons.isGlobal);
  tout->Branch("Muon_isTracker", &Muons.isTracker);
  tout->Branch("Muon_isStandAlone", &Muons.isStandAlone);
  tout->Branch("Muon_chi2Ndof", &Muons.chi2Ndof);
  tout->Branch("Muon_ecalIso", &Muons.ecalIso);
  tout->Branch("Muon_hcalIso", &Muons.hcalIso);
  tout->Branch("Muon_trackIso", &Muons.trackIso);
  tout->Branch("Muon_ecalRelIso", &Muons.ecalRelIso);
  tout->Branch("Muon_hcalRelIso", &Muons.hcalRelIso);
  tout->Branch("Muon_trackRelIso", &Muons.trackRelIso);
  tout->Branch("Muon_dxy", &Muons.dxy);
  tout->Branch("Muon_dxye", &Muons.dxye);
  tout->Branch("Muon_dz", &Muons.dz);
  tout->Branch("Muon_dze", &Muons.dze);
  tout->Branch("Muon_dxysig", &Muons.dxysig);
  tout->Branch("Muon_dzsig", &Muons.dzsig);
  tout->Branch("Muon_phiCorr", &Muons.phiCorr);
  tout->Branch("Muon_dxyCorr", &Muons.dxyCorr);
  tout->Branch("Muon_PFIsoChg0p3", &Muons.PFIsoChg0p3);
  tout->Branch("Muon_PFIsoAll0p3", &Muons.PFIsoAll0p3);
  tout->Branch("Muon_PFRelIsoChg0p3", &Muons.PFRelIsoChg0p3);
  tout->Branch("Muon_PFRelIsoAll0p3", &Muons.PFRelIsoAll0p3);
  tout->Branch("Muon_mindrPF0p3", &Muons.mindrPF0p3);
  tout->Branch("Muon_PFIsoChg0p4", &Muons.PFIsoChg0p4);
  tout->Branch("Muon_PFIsoAll0p4", &Muons.PFIsoAll0p4);
  tout->Branch("Muon_PFRelIsoChg0p4", &Muons.PFRelIsoChg0p4);
  tout->Branch("Muon_PFRelIsoAll0p4", &Muons.PFRelIsoAll0p4);
  tout->Branch("Muon_mindrPF0p4", &Muons.mindrPF0p4);
  tout->Branch("Muon_mindr", &Muons.mindr);
  tout->Branch("Muon_maxdr", &Muons.maxdr);
  tout->Branch("Muon_mindrJet", &Muons.mindrJet);
  tout->Branch("Muon_mindphiJet", &Muons.mindphiJet);
  tout->Branch("Muon_mindetaJet", &Muons.mindetaJet);
  tout->Branch("Muon_vec", &Muons.vec);
  tout->Branch("Muon_selected", &Muons.selected);
  tout->Branch("Muon_nhitsbeforesv", &Muons.nhitsbeforesv);
  tout->Branch("Muon_ncompatible", &Muons.ncompatible);
  tout->Branch("Muon_ncompatibletotal", &Muons.ncompatibletotal);
  tout->Branch("Muon_nexpectedhits", &Muons.nexpectedhits);
  tout->Branch("Muon_nexpectedhitsmultiple", &Muons.nexpectedhitsmultiple);
  tout->Branch("Muon_nexpectedhitsmultipletotal", &Muons.nexpectedhitsmultipletotal);
  tout->Branch("Muon_nexpectedhitstotal", &Muons.nexpectedhitstotal);
  

  // Event setup
  TRandom3 rndm_partialUnblinding(42);
  tqdm bar;

  bool isMC = true;
  if ( process.Contains("Data") )
    isMC = false;

  if ( !isMC ) {
    if ( year == "2022" )
      set_goodrun_file_json("../data/Cert_Collisions2022_355100_362760_Golden.json");
    else if ( year == "2023" )
      set_goodrun_file_json("../data/Cert_Collisions2023_366442_370790_Golden.json");
  }

  // File loop
  unsigned int iFile = 1;
  for (auto inputFile : inputFiles) {
    std::cout << "File number: " << iFile << "\t" << inputFile <<  "\n";
    TFile *file = TFile::Open(inputFile);
    auto nEventsFile = ((TTree*)file->Get("Events"))->GetEntries();
    Event ev(file);

    // Event loop
    unsigned int iEv = 0;
    for (ev.toBegin(); ! ev.atEnd(); ++ev) {
      iEv++;
      //if (iEv > 10)
      //  break;
      bar.progress(iEv, nEventsFile);

      auto evAux = ev.eventAuxiliary();
      auto eID = evAux.id();
      run  = eID.run();
      lumi = eID.luminosityBlock();
      evtn = eID.event();

      // JSON and duplicate removal
      if ( !isMC ) {
        if ( !(goodrun(run, lumi)) )
          continue;
        duplicate_removal::DorkyEventIdentifier id(run, evtn, lumi);
        if ( is_duplicate(id) )
          continue;
        if ( doPartialUnblinding && rndm_partialUnblinding.Rndm() > partialUnblindingPercentage )
          continue;
      }

      // L1 selection
      auto l1s = getObject<std::vector<bool>>(ev, "triggerMaker", "l1result");
      auto l1Prescales = getObject<std::vector<double>>(ev, "triggerMaker", "l1prescale");
      passL1 = false;
      for (unsigned int iL1=0; iL1<l1s.size(); ++iL1) {
        l1fired[iL1] = l1s[iL1];
        if (l1s[iL1]==true && l1Prescales[iL1]==1) { // L1 trigger fired and is not prescaled
          passL1 = true;
        }
      }
      if (!passL1)
	continue;

      // HLT selection
      auto hlts = getObject<std::vector<bool>>(ev, "triggerMaker", "hltresult");
      passHLT = false;
      for (auto hlt : hlts) {
        if (hlt==true) {
          passHLT = true;
          break;
        }
      }
      if (!passHLT)
	continue;

      // PV selection
      auto pvs = getObject<std::vector<Run3ScoutingVertex>>(ev, "hltScoutingPrimaryVertexPacker", "primaryVtx");
      nPV = 0; PV_x = 0; PV_y = 0; PV_z = 0;

      nPV = pvs.size();
      if (pvs.size() > 0 && pvs[0].isValidVtx()) {
        PV_x = pvs[0].x();
        PV_y = pvs[0].y();
        PV_z = pvs[0].z();
      }

      // GenPart
      GenParts.clear();
      if (isMC) {
        auto genparts = getObject<std::vector<reco::GenParticle>>(ev, "genParticles", "");
        for (unsigned int iGen=0; iGen<genparts.size(); iGen++) {
          auto genpart = genparts[iGen];
          if (abs(genpart.pdgId())!=13 && // Muon
              abs(genpart.pdgId())!=999999 && // Dark photon
              abs(genpart.pdgId())!=4900111 && // Dark pion
              abs(genpart.pdgId())!=4900211 && // Dark pion
              abs(genpart.pdgId())!=4900221 && // Dark eta
              abs(genpart.pdgId())!=4900113 && // Dark rho
              abs(genpart.pdgId())!=4900213 && // Dark rho
              abs(genpart.pdgId())!=4900101 && // Dark mass
              abs(genpart.pdgId())!=4900102 && // Dark mass
              abs(genpart.pdgId())!=1023 && // Dark photon from Higgs
              abs(genpart.pdgId())!=25 && // Higgs
              abs(genpart.pdgId())!=443) // JPsi
            continue;
          if (!genpart.isLastCopy())
            continue;

          int motherIdx = -1, motherPdgId = 0; // Default value
          if (genpart.numberOfMothers() > 0) {
            motherIdx = genpart.motherRef().index();
            while (genparts[motherIdx].pdgId() == genpart.pdgId()) {
              motherIdx = genparts[motherIdx].motherRef().index();
            }
            motherPdgId = genparts[motherIdx].pdgId();
          }
          GenParts.pt.push_back(genpart.pt());
          GenParts.eta.push_back(genpart.eta());
          GenParts.phi.push_back(genpart.phi());
          GenParts.m.push_back(genpart.mass());
          GenParts.vx.push_back(genpart.vx());
          GenParts.vy.push_back(genpart.vy());
          GenParts.vz.push_back(genpart.vz());
          GenParts.lxy.push_back(TMath::Hypot(genpart.vx(), genpart.vy()));
          GenParts.status.push_back(genpart.status());
          GenParts.index.push_back(iGen);
          GenParts.pdgId.push_back(genpart.pdgId());
          GenParts.motherIndex.push_back(motherIdx);
          GenParts.motherPdgId.push_back(motherPdgId);
        }
      }

      // SV selection
      auto svs = getObject<std::vector<Run3ScoutingVertex>>(ev, "hltScoutingMuonPacker", "displacedVtx");
      auto dvonmodule = getObject<std::vector<bool>>(ev, "hitMaker", "dvonmodule");
      auto dvonmodulewithinunc = getObject<std::vector<bool>>(ev, "hitMaker", "dvonmodulewithinunc");
      auto dvdetxmind = getObject<std::vector<float>>(ev, "hitMaker", "dvdetxmind");
      auto dvdetymind = getObject<std::vector<float>>(ev, "hitMaker", "dvdetymind");
      auto dvdetzmind = getObject<std::vector<float>>(ev, "hitMaker", "dvdetzmind");
      auto dvmindfromdet = getObject<std::vector<float>>(ev, "hitMaker", "dvmindfromdet");
      auto dvmindfromdetx = getObject<std::vector<float>>(ev, "hitMaker", "dvmindfromdetx");
      auto dvmindfromdety = getObject<std::vector<float>>(ev, "hitMaker", "dvmindfromdety");
      auto dvmindfromdetz = getObject<std::vector<float>>(ev, "hitMaker", "dvmindfromdetz");
      SVs.clear();

      unsigned int nSVs = svs.size();
      if (nSVs < 1)
        continue;

      for (unsigned int iSV=0; iSV<nSVs; ++iSV) {
        auto sv = svs[iSV];
        if (!(sv.isValidVtx()))
          continue;

        float x=sv.x(), y=sv.y(), z=sv.z();
        float xe=sv.xError(), ye=sv.yError(), ze=sv.zError();
        float chi2=sv.chi2(), ndof=sv.ndof();

        SVs.index.push_back(iSV);
        SVs.ndof.push_back(ndof);
        SVs.x.push_back(x);
        SVs.y.push_back(y);
        SVs.z.push_back(z);
        SVs.xe.push_back(xe);
        SVs.ye.push_back(ye);
        SVs.ze.push_back(ze);
        SVs.chi2.push_back(chi2);
        SVs.prob.push_back(TMath::Prob(chi2, ndof));
        SVs.chi2Ndof.push_back(chi2/ndof);
        float lxy = TMath::Sqrt((x-PV_x)*(x-PV_x)+(y-PV_y)*(y-PV_y));
        SVs.lxy.push_back(lxy);
        SVs.l3d.push_back(TMath::Sqrt(lxy*lxy+(z-PV_z)*(z-PV_z)));
        SVs.onModule.push_back(dvonmodule.at(iSV));
        SVs.onModuleWithinUnc.push_back(dvonmodulewithinunc.at(iSV));
        SVs.closestDet_x.push_back(dvdetxmind.at(iSV));
        SVs.closestDet_y.push_back(dvdetymind.at(iSV));
        SVs.closestDet_z.push_back(dvdetzmind.at(iSV));
        SVs.minDistanceFromDet.push_back(dvmindfromdet.at(iSV));
        SVs.minDistanceFromDet_x.push_back(dvmindfromdetx.at(iSV));
        SVs.minDistanceFromDet_y.push_back(dvmindfromdety.at(iSV));
        SVs.minDistanceFromDet_z.push_back(dvmindfromdetz.at(iSV));

        float mindx=1e6, mindy=1e6, mindz=1e6, mindxy=1e6, mind3d=1e6;
        float maxdx=-1, maxdy=-1, maxdz=-1, maxdxy=-1, maxd3d=-1;
        for (unsigned int jSV=0; jSV<nSVs; ++jSV) {
          if (jSV==iSV)
            continue;
          auto svOther = svs[jSV];
          if (!(svOther.isValidVtx()))
            continue;

          float xOther=svOther.x(), yOther=svOther.y(), zOther=svOther.z();
          float dx = (x-xOther)*(x-xOther); // Squared for the moment
          float dy = (y-yOther)*(y-yOther); // Squared for the moment
          float dz = (z-zOther)*(z-zOther); // Squared for the moment
          float dxy = TMath::Sqrt(dx+dy);
          float d3d = TMath::Sqrt(dx+dy+dz);
          dx = TMath::Sqrt(dx); // Back to the proper value
          dy = TMath::Sqrt(dy); // Back to the proper value
          dz = TMath::Sqrt(dz); // Back to the proper value

          if (dx<mindx) mindx = dx;
          if (dx>maxdx) maxdx = dx;
          if (dy<mindy) mindy = dy;
          if (dy>maxdy) maxdy = dy;
          if (dz<mindz) mindz = dz;
          if (dz>maxdz) maxdz = dz;
          if (dxy<mindxy) mindxy = dxy;
          if (dxy>maxdxy) maxdxy = dxy;
          if (d3d<mind3d) mind3d = d3d;
          if (d3d>maxd3d) maxd3d = d3d;
        }
        SVs.mindx.push_back(mindx);
        SVs.mindy.push_back(mindy);
        SVs.mindz.push_back(mindz);
        SVs.mindxy.push_back(mindxy);
        SVs.mind3d.push_back(mind3d);
        SVs.maxdx.push_back(maxdx);
        SVs.maxdy.push_back(maxdy);
        SVs.maxdz.push_back(maxdz);
        SVs.maxdxy.push_back(maxdxy);
        SVs.maxd3d.push_back(maxd3d);

        SVs.selected.push_back( (xe<maxXerr && ye<maxYerr && ze<maxZerr && chi2/ndof<maxChi2) );
      }
      SVs.sort();

      // SV overlap
      SVOverlaps.clear();
      for (unsigned int iSV=0; iSV<SVs.x.size(); ++iSV) {
        if (SVs.selected[iSV]==0)
          continue;

        float sumOfProb = 0.0;
        std::vector<unsigned int> vtxIdxs_temp = {};

        bool usedSV=false;
        for (unsigned int iSVOverlap=0; iSVOverlap<SVOverlaps.vtxIdxs.size(); iSVOverlap++) {
          for (auto SVOverlapVtxIdx : SVOverlaps.vtxIdxs[iSVOverlap]) {
            if (iSV==SVOverlapVtxIdx) {
              usedSV=true;
              break;
            }
          }
        }
        if (usedSV)
          continue;

        float x=SVs.x[iSV], y=SVs.y[iSV], z=SVs.z[iSV];
        float xe=SVs.xe[iSV], ye=SVs.ye[iSV], ze=SVs.ze[iSV];
        for (unsigned int jSV=iSV+1; jSV<SVs.x.size(); ++jSV) {
          if (SVs.selected[jSV]==0)
            continue;

          float xOther=SVs.x[jSV], yOther=SVs.y[jSV], zOther=SVs.z[jSV];
          float dx = x - xOther;
          float dy = y - yOther;
          float dz = z - zOther;
	  float xeOther=SVs.xe[jSV], yeOther=SVs.ye[jSV], zeOther=SVs.ze[jSV];
          float dxy = dx*dx + dy*dy;
          float d3d = dxy*dxy + dz*dz;
	  float xeOverlap = std::max(xe, xeOther);
	  float yeOverlap = std::max(ye, yeOther);
	  float zeOverlap = std::max(ze, zeOther);
	  float dxyeOverlap = TMath::Sqrt(xeOverlap*xeOverlap+yeOverlap*yeOverlap);
	  float d3deOverlap = TMath::Sqrt(dxyeOverlap*dxyeOverlap+zeOverlap*zeOverlap);
          if ( fabs(dx)<xeOverlap && fabs(dy)<yeOverlap && fabs(dz)<zeOverlap && TMath::Sqrt(dxy)<std::min(dxyeOverlap, maxDXYerr) && TMath::Sqrt(d3d)<std::min(d3deOverlap, maxD3Derr) ) {
            vtxIdxs_temp.push_back(jSV);
            sumOfProb += SVs.prob[jSV];
          }
        }
        if (vtxIdxs_temp.size() > 0) {
          // Add initial SV to the SVOverlap
          vtxIdxs_temp.insert(vtxIdxs_temp.begin(),iSV);
          sumOfProb += SVs.prob[iSV];

          // Compute and fill SVOverlap properties
          SVOverlaps.vtxIdxs.push_back(vtxIdxs_temp);
          float xOverlap=0.0, yOverlap=0.0, zOverlap=0.0;
          for (auto vtxIdx : vtxIdxs_temp) {
            xOverlap += SVs.prob[vtxIdx]/sumOfProb * SVs.x[vtxIdx];
            yOverlap += SVs.prob[vtxIdx]/sumOfProb * SVs.y[vtxIdx];
            zOverlap += SVs.prob[vtxIdx]/sumOfProb * SVs.z[vtxIdx];
          }
          SVOverlaps.x.push_back(xOverlap);
          SVOverlaps.y.push_back(yOverlap);
          SVOverlaps.z.push_back(zOverlap);
          float lxyOverlap = TMath::Sqrt((xOverlap-PV_x)*(xOverlap-PV_x)+(yOverlap-PV_y)*(yOverlap-PV_y));
          SVOverlaps.lxy.push_back(lxyOverlap);
          SVOverlaps.l3d.push_back(TMath::Sqrt(lxyOverlap*lxyOverlap+(zOverlap-PV_z)*(zOverlap-PV_z)));
        }
      }

      // Muon selection
      auto mus = getObject<std::vector<Run3ScoutingMuon>>(ev, "hltScoutingMuonPacker");
      auto jets = getObject<std::vector<Run3ScoutingPFJet>>(ev, "hltScoutingPFPacker");
      auto pfs = getObject<std::vector<Run3ScoutingParticle>>(ev, "hltScoutingPFPacker");
      auto nhitsbeforesv = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "nhitsbeforesv");
      auto ncompatible = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "ncompatible");
      auto ncompatibletotal = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "ncompatibletotal");
      auto nexpectedhits = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "nexpectedhits");
      auto nexpectedhitsmultiple = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "nexpectedhitsmultiple");
      auto nexpectedhitsmultipletotal = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "nexpectedhitsmultipletotal");
      auto nexpectedhitstotal = getObject<std::vector<std::vector<int>>>(ev, "hitMaker", "nexpectedhitstotal");
      Muons.clear();
      unsigned int nMus = mus.size();
      nMuonAssoc=0;

      for (unsigned int iMu=0; iMu<nMus; ++iMu) {
        auto mu = mus[iMu];
        std::vector<int> matchedAndSelVtxIdxs;
        for (auto matchedVtxIdx : mu.vtxIndx()) {
          for (unsigned int iSV=0; iSV<SVs.index.size(); ++iSV) {
            if (matchedVtxIdx==SVs.index[iSV] && SVs.selected[iSV])
              matchedAndSelVtxIdxs.push_back(matchedVtxIdx);
          }
        }
        if (matchedAndSelVtxIdxs.size() < 1) // Require muon to be associated to at least one of the selected SVs
          continue;
        nMuonAssoc++; // Count muon associated to at least one selected SV
        if (!(fabs(mu.eta())<2.4))
          continue;

        float pt=mu.pt(), eta=mu.eta(), phi=mu.phi();

        Muons.vtxIdxs.push_back(matchedAndSelVtxIdxs);

        int bestAssocSVIdx=-1;
        for (auto matchedAndSelVtxIdx : matchedAndSelVtxIdxs) {
          if (bestAssocSVIdx==-1)
            bestAssocSVIdx = matchedAndSelVtxIdx;
          else {
            if (SVs.prob[matchedAndSelVtxIdx] > SVs.prob[bestAssocSVIdx])
              bestAssocSVIdx = matchedAndSelVtxIdx;
          }
        }
        Muons.bestAssocSVIdx.push_back(bestAssocSVIdx);

        int bestAssocSVOverlapIdx=-1;
        for (unsigned int iSVOverlap=0; iSVOverlap<SVOverlaps.vtxIdxs.size(); iSVOverlap++) {
          for (auto SVOverlapVtxIdx : SVOverlaps.vtxIdxs[iSVOverlap]) {
            if (bestAssocSVIdx==SVOverlapVtxIdx)
              bestAssocSVOverlapIdx = iSVOverlap;
          }
        }
        Muons.bestAssocSVOverlapIdx.push_back(bestAssocSVOverlapIdx);

        Muons.saHits.push_back(mu.nValidStandAloneMuonHits());
        Muons.saMatchedStats.push_back(mu.nStandAloneMuonMatchedStations());
        Muons.muHits.push_back(mu.nValidRecoMuonHits());
        Muons.muChambs.push_back(mu.nRecoMuonChambers());
        Muons.muCSCDT.push_back(mu.nRecoMuonChambersCSCorDT());
        Muons.muMatch.push_back(mu.nRecoMuonMatches());
        Muons.muMatchedStats.push_back(mu.nRecoMuonMatchedStations());
        Muons.muExpMatchedStats.push_back(mu.nRecoMuonExpectedMatchedStations());
        Muons.muMatchedRPC.push_back(mu.nRecoMuonMatchedRPCLayers());
        Muons.pixHits.push_back(mu.nValidPixelHits());
        Muons.stripHits.push_back(mu.nValidStripHits());
        Muons.pixLayers.push_back(mu.nPixelLayersWithMeasurement());
        Muons.trkLayers.push_back(mu.nTrackerLayersWithMeasurement());
        Muons.pt.push_back(pt);
        Muons.eta.push_back(eta);
        Muons.phi.push_back(phi);
        Muons.ch.push_back(mu.charge());
        Muons.isGlobal.push_back(isGlobalMuon(mu.type()));
        Muons.isTracker.push_back(isTrackerMuon(mu.type()));
        Muons.isStandAlone.push_back(isStandAloneMuon(mu.type()));
        Muons.chi2Ndof.push_back(mu.normalizedChi2());
        Muons.ecalIso.push_back(mu.ecalIso());
        Muons.hcalIso.push_back(mu.hcalIso());
        Muons.trackIso.push_back(mu.trackIso());
        Muons.ecalRelIso.push_back(mu.ecalIso()/pt);
        Muons.hcalRelIso.push_back(mu.hcalIso()/pt);
        Muons.trackRelIso.push_back(mu.trackIso()/pt);
        Muons.dxy.push_back(mu.trk_dxy());
        Muons.dxye.push_back(mu.trk_dxyError());
        Muons.dz.push_back(mu.trk_dz());
        Muons.dze.push_back(mu.trk_dzError());
        Muons.dxysig.push_back(mu.trk_dxy()/mu.trk_dxyError());
        Muons.dzsig.push_back(mu.trk_dz()/mu.trk_dzError());
        Muons.selected.push_back(pt>3.0 && fabs(eta)<2.4 && mu.normalizedChi2()<3.0);

        for (unsigned int iDV=0; iDV<mu.vtxIndx().size(); ++iDV) {
	        if (mu.vtxIndx().at(iDV)==bestAssocSVIdx) {
            Muons.nhitsbeforesv.push_back(nhitsbeforesv.at(iMu).at(iDV));
            Muons.ncompatible.push_back(ncompatible.at(iMu).at(iDV));
            Muons.ncompatibletotal.push_back(ncompatibletotal.at(iMu).at(iDV));
            Muons.nexpectedhits.push_back(nexpectedhits.at(iMu).at(iDV));
            Muons.nexpectedhitsmultiple.push_back(nexpectedhitsmultiple.at(iMu).at(iDV));
            Muons.nexpectedhitsmultipletotal.push_back(nexpectedhitsmultipletotal.at(iMu).at(iDV));
            Muons.nexpectedhitstotal.push_back(nexpectedhitstotal.at(iMu).at(iDV));
            break;
          }
        }

        float bestSVPosition_x, bestSVPosition_y;
        if (bestAssocSVOverlapIdx!=-1) {
          bestSVPosition_x = SVOverlaps.x[bestAssocSVOverlapIdx];
          bestSVPosition_y = SVOverlaps.y[bestAssocSVOverlapIdx];
        }
        else {
          bestSVPosition_x = SVs.x[bestAssocSVIdx];
          bestSVPosition_y = SVs.y[bestAssocSVIdx];
        }
        float dxyCorr = -(bestSVPosition_x - PV_x)*TMath::Sin(phi) + (bestSVPosition_y - PV_y)*TMath::Cos(phi);
        Muons.dxyCorr.push_back(dxyCorr);
        TLorentzVector muVec; muVec.SetPtEtaPhiM(pt, eta, phi, MUON_MASS);
        float phiCorr = getCorrectedPhi(mu, muVec, dxyCorr, bestSVPosition_x, bestSVPosition_y);
        Muons.phiCorr.push_back(phiCorr);
        muVec.SetPtEtaPhiM(pt, eta, phiCorr, MUON_MASS);
        Muons.vec.push_back(muVec);

        const auto pfIsos0p3 = getPFIsolation(muVec, pfs, 0.3);
        const auto pfIsoChg0p3 = std::get<0>(pfIsos0p3);
        const auto pfIsoAll0p3 = pfIsoChg0p3 + std::max(0.0, std::get<1>(pfIsos0p3)+std::get<2>(pfIsos0p3)-0.5*std::get<3>(pfIsos0p3));
        Muons.PFIsoChg0p3.push_back(pfIsoChg0p3);
        Muons.PFIsoAll0p3.push_back(pfIsoAll0p3);;
        Muons.PFRelIsoChg0p3.push_back(pfIsoChg0p3/pt);
        Muons.PFRelIsoAll0p3.push_back(pfIsoAll0p3/pt);
        Muons.mindrPF0p3.push_back(std::get<4>(pfIsos0p3));

        const auto pfIsos0p4 = getPFIsolation(muVec, pfs, 0.4);
        const auto pfIsoChg0p4 = std::get<0>(pfIsos0p4);
        const auto pfIsoAll0p4 = pfIsoChg0p4 + std::max(0.0, std::get<1>(pfIsos0p4)+std::get<2>(pfIsos0p4)-0.5*std::get<3>(pfIsos0p4));
        Muons.PFIsoChg0p4.push_back(pfIsoChg0p4);
        Muons.PFIsoAll0p4.push_back(pfIsoAll0p4);;
        Muons.PFRelIsoChg0p4.push_back(pfIsoChg0p4/pt);
        Muons.PFRelIsoAll0p4.push_back(pfIsoAll0p4/pt);
        Muons.mindrPF0p4.push_back(std::get<4>(pfIsos0p4));

        float mindr=1e6;
        float maxdr=-1;
        for (unsigned int jMu=0; jMu<nMus; ++jMu) {
          if (jMu==iMu)
            continue;
          auto muOther = mus[jMu];
          bool matchedAndSelVtx = false;
          for (auto matchedVtxIdx : muOther.vtxIndx()) {
            for (auto selVtxIdx : SVs.index) {
              if (matchedVtxIdx==selVtxIdx) {
                matchedAndSelVtx = true;
                break;
              }
              if (matchedAndSelVtx)
                break;
            }
          }
          if (!matchedAndSelVtx)
            continue;
          if (!(fabs(muOther.eta())<2.4))
            continue;
          TLorentzVector muVecOther; muVecOther.SetPtEtaPhiM(muOther.pt(), muOther.eta(), muOther.phi(), MUON_MASS);
          float dr = muVec.DeltaR(muVecOther);
          if (dr<mindr) mindr = dr;
          if (dr>maxdr) maxdr = dr;
        }
        Muons.mindr.push_back(mindr);
        Muons.maxdr.push_back(maxdr);

        float mindrJet=1e6;
        float mindphiJet=1e6;
        float mindetaJet=1e6;
        for (auto jet : jets) {
          if (!(jet.pt()>20.0 && fabs(jet.eta())<3.0))
            continue;
          TLorentzVector jetVec; jetVec.SetPtEtaPhiM(jet.pt(), jet.eta(), jet.phi(), jet.m());
          float dr = muVec.DeltaR(jetVec);
          if (dr<mindrJet) {
	    mindrJet = dr;
	    mindphiJet = fabs(muVec.DeltaPhi(jetVec));
	    mindetaJet = fabs(muVec.Eta()-jetVec.Eta());
	  }
        }
        Muons.mindrJet.push_back(mindrJet);
        Muons.mindphiJet.push_back(mindphiJet);
        Muons.mindetaJet.push_back(mindetaJet);
      }
      if (Muons.pt.size() < 2)
        continue;
      Muons.sort();

      tout->Fill();
    }
    iFile++;
    std::cout<<"\n\n";
  }

  bar.finish();
  fout->Write();
  fout->Close();

  return;
}
