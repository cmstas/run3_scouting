import ROOT
import os,sys,json
from datetime import date    
import numpy as np
import argparse
from tqdm import tqdm
from DataFormats.FWLite import Events, Handle
import mplhep as hep
import matplotlib.pyplot as plt

MUON_MASS = 0.10566
user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

def getValues(histo):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins)

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--inDir", default="/ceph/cms/store/user/"+user+"/Run3ScoutingOutput/looperOutput_"+today, help="Choose input directory. Default: '/ceph/cms/store/user/"+user+"/Run3ScoutingOutput/looperOutput_"+today+"'")
parser.add_argument("--inSample", default="*", help="Choose sample; for all samples in input directory, choose '*'")
parser.add_argument("--inFile", default="*", help="Choose input file by index (for debug); for all files in input directory, choose '*'")
parser.add_argument("--outDir", default=os.environ.get("PWD")+"/outputGENHistograms_"+today, help="Choose output directory. Default: '"+os.environ.get("PWD")+"/outputGENHistograms_"+today+"'")
parser.add_argument("--nmin", default=0, help="Number of min event to process")
parser.add_argument("--nmax", default=100, help="Number of max event to process")
parser.add_argument("--mass", default='2p0', help="Mass")
parser.add_argument("--output", default='', help="Output")
args = parser.parse_args()

nmin = int(args.nmin)
nmax = int(args.nmax)
mass = args.mass


# Load the tree
dirs = {}
dirs['0p3'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-0p3_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_051833/0000/'
dirs['0p4'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-0p4_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052325/0000/'
dirs['0p5'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-0p5_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052337/0000/'
dirs['0p6'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-0p6_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052351/0000/'
dirs['0p7'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-0p7_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052404/0000/'
dirs['0p9'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-0p9_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052419/0000/'
dirs['1p25'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-1p25_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052436/0000/'
dirs['1p5'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-1p5_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052450/0000/'
dirs['2p0'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-2p0_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052508/0000/'
dirs['2p85'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-2p85_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052524/0000/'
dirs['3p35'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-3p35_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052547/0000/'
#dirs['4p0'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-4p0_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052606/0000/'
dirs['4p0'] = '/ceph/cms/store/group/Run3Scouting/RAWScouting_BToPhi_2022_vbtophi_final_8p0/BToPhi_MPhi-4p0_ctau-100mm_TuneCP5_13p6TeV_pythia8/crab_centralSkim__BToPhi_2022_m-4p0_ctau-100mm_btophi_final_8p0/250826_144811/0000/'
#dirs['4p6'] = '/ceph/cms/store/user/fernance/BToPhi-samples/BToPhi_MPhi-4p6_ctau-1mm_TuneCP5_13p6TeV_pythia8/private-GENSIM-2022postEE/251029_161656/0000/'
dirs['4p6'] = '/ceph/cms/store/user/fernance/BToPhi-samples/BToPhi_MPhi-4p6_ctau-100mm_TuneCP5_13p6TeV_pythia8_ext//private-GENSIM-2022//251101_094211/0000/'
#dirs['4p6'] = '/ceph/cms/store/user/fernance/BToPhi-samples/BToPhi_MPhi-4p6_ctau-10mm_TuneCP5_13p6TeV_pythia8_ext//private-GENSIM-2022/251101_094216/0000/'
dirs['5p0'] = '/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-5p0_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052619/0000/'
indir = dirs[mass]
files = [f for f in os.listdir(indir) if '.root' in f]
files = files[nmin:nmax]
print(f'Number of files: {len(files)}')
#['/ceph/cms/store/group/Run3Scouting/GENScouting_noFilter_v1/BToPhi_MPhi-2p0_ctau-1mm-pythia8/private-Run3Summer22_noFilter_/250207_052508/0000/output_gensim_773.root']
events = Events(['%s/%s'%(indir,f) for f in files])

# Handler
ghandle = Handle('std::vector<reco::GenParticle>')
glabel  = ("genParticles")


# Histograms:
h1d = []

h_nbhadron = ROOT.TH1D("h_nbhadron","",10,0,10)
h_nbhadron.GetXaxis().SetTitle("Number of b-hadrons")
h_nbhadron.GetYaxis().SetTitle("Events")

h_bhadron_pt = ROOT.TH1D("h_bhadron_pt","",40,0,40)
h_bhadron_pt.GetXaxis().SetTitle("b-hadron pt")
h_bhadron_pt.GetYaxis().SetTitle("Events")

h_bhadron_pt_filtered = ROOT.TH1D("h_bhadron_pt_filtered","",35,5,40)
h_bhadron_pt_filtered.GetXaxis().SetTitle("b-hadron pt")
h_bhadron_pt_filtered.GetYaxis().SetTitle("Events")

h_bhadron_pt_withDaugther = ROOT.TH1D("h_bhadron_pt_withDaugther","",40,0,40)
h_bhadron_pt_withDaugther.GetXaxis().SetTitle("b-hadron pt")
h_bhadron_pt_withDaugther.GetYaxis().SetTitle("Events")


h_bhadron_pt_withDaugtherFilter = ROOT.TH1D("h_bhadron_pt_withDaugtherFilter","",40,0,40)
h_bhadron_pt_withDaugtherFilter.GetXaxis().SetTitle("b-hadron pt")
h_bhadron_pt_withDaugtherFilter.GetYaxis().SetTitle("Events")

h_bhadron_eta = ROOT.TH1D("h_bhadron_eta","",100,-8,8)
h_bhadron_eta.GetXaxis().SetTitle("b-hadron eta")
h_bhadron_eta.GetYaxis().SetTitle("Events")

h_phi_mass = ROOT.TH1D("h_phi_mass","",200,0,6)
h_phi_mass.GetXaxis().SetTitle("phi mass")
h_phi_mass.GetYaxis().SetTitle("Events")

h_phi_lxy = ROOT.TH1D("h_phi_lxy","",70,0,70)
h_phi_lxy.GetXaxis().SetTitle("phi lxy")
h_phi_lxy.GetYaxis().SetTitle("Events")

h_phi_mass_frommu = ROOT.TH1D("h_phi_mass_frommu","",200,0,6)
h_phi_mass_frommu.GetXaxis().SetTitle("phi mass (from mu)")
h_phi_mass_frommu.GetYaxis().SetTitle("Events")

h_counts_1b = ROOT.TH1D("h_counts_1b","",1,0,1)

h_counts_sel1b = ROOT.TH1D("h_counts_sel1b","",1,0,1)

# Acceptance studies
acc_parent_pt_eta_level1 = ROOT.TH2F("acc_parent_pt_eta_level1","",40,0,40, 40, 0, 8)
acc_nonparent_pt_eta_level1 = ROOT.TH2F("acc_nonparent_pt_eta_level1","",40,0,40, 40, 0, 8)
acc_parent_pt_eta_level2 = ROOT.TH2F("acc_parent_pt_eta_level2","",40,0,40, 40, 0, 8)
acc_nonparent_pt_eta_level2 = ROOT.TH2F("acc_nonparent_pt_eta_level2","",40,0,40, 40, 0, 8)
acc_parent_pt_eta_level3 = ROOT.TH2F("acc_parent_pt_eta_level3","",40,0,40, 40, 0, 8)
acc_nonparent_pt_eta_level3 = ROOT.TH2F("acc_nonparent_pt_eta_level3","",40,0,40, 40, 0, 8)
acc_summary = ROOT.TH1F("acc_summary","",2, 0, 2)

###
#
for h in h1d:
    h.Sumw2(ROOT.kFALSE)

###
#
print("Starting loop over %d events"%events.size())
for en,e in tqdm(enumerate(events), total=events.size(), desc="Processing", unit="event"):
    #
    e.getByLabel(glabel,ghandle)
    genParticles = ghandle.product()
    #
    bhadrons = []
    other_bhadrons = []
    for gn,g in enumerate(genParticles):
        # get b-hadron
        if not (g.isLastCopy()):
            continue
        if abs(g.pdgId()) not in [521, 511, 531, 541, 5122]:
            continue
        # get b-hadron decaying to phi
        hasPhi = False
        for dn in range(g.numberOfDaughters()):
            if (abs(g.daughter(dn).pdgId())==6000211):
                hasPhi = True
                h_phi_mass.Fill(g.daughter(dn).mass())
                #print('mass:', g.daughter(dn).mass())
        if hasPhi:
            bhadrons.append(g) 
        else:
            other_bhadrons.append(g)
        #else:
        #    print('This b-hadron doesnt have a phi')
    nbhadron = len(bhadrons)
    #
    h_nbhadron.Fill(nbhadron)
    #
    if nbhadron == 1:
        h_bhadron_pt.Fill(bhadrons[0].pt())
        h_bhadron_eta.Fill(bhadrons[0].eta())
        passFilter = False
        hassPhi = False
        for dn in range(bhadrons[0].numberOfDaughters()):
            if (abs(bhadrons[0].daughter(dn).pdgId())==6000211):
                hassPhi = True
                phi = bhadrons[0].daughter(dn)
                g1 = ROOT.TLorentzVector()
                g1.SetPtEtaPhiM(phi.daughter(0).pt(), phi.daughter(0).eta(), phi.daughter(0).phi(), 0.106)
                g2 = ROOT.TLorentzVector()
                g2.SetPtEtaPhiM(phi.daughter(1).pt(), phi.daughter(1).eta(), phi.daughter(1).phi(), 0.106)
                h_phi_mass_frommu.Fill((g1+g2).M())
                h_phi_lxy.Fill(((phi.daughter(0).vx())**2 + (phi.daughter(0).vy())**2 )**0.5)
                if phi.daughter(0).pt() > 2. and phi.daughter(1).pt() > 2. and abs(phi.daughter(0).eta()) < 3. and abs(phi.daughter(1).eta()) < 3.:
                    passFilter = True
                break
        if bhadrons[0].pt() > 5 and abs(bhadrons[0].eta()) < 2.8:
            h_counts_1b.Fill(0)
            h_bhadron_pt_filtered.Fill(bhadrons[0].pt())
            if passFilter:
                h_counts_sel1b.Fill(0)
        if hassPhi:
            h_bhadron_pt_withDaugther.Fill(bhadrons[0].pt())
        if passFilter:
            h_bhadron_pt_withDaugtherFilter.Fill(bhadrons[0].pt())
        #
        # Studies for acceptance and normalization
        if len(other_bhadrons)==1:
            parent = bhadrons[0]
            nonparent = other_bhadrons[0]
            acc_parent_pt_eta_level1.Fill(parent.pt(), abs(parent.eta()))        
            acc_nonparent_pt_eta_level1.Fill(nonparent.pt(), abs(nonparent.eta()))
            if passFilter:     
                acc_parent_pt_eta_level2.Fill(parent.pt(), abs(parent.eta()))        
                acc_nonparent_pt_eta_level2.Fill(nonparent.pt(), abs(nonparent.eta()))
                if parent.pt() > 5 and abs(parent.eta()) < 2.8:
                    acc_parent_pt_eta_level3.Fill(parent.pt(), abs(parent.eta()))        
                    acc_nonparent_pt_eta_level3.Fill(nonparent.pt(), abs(nonparent.eta()))
                    if nonparent.pt() > 5 and abs(nonparent.eta()) < 2.8:
                        acc_summary.Fill(1)
                    else:
                        acc_summary.Fill(0)

print(h_bhadron_pt.GetEntries())

h1d.append(h_nbhadron)
h1d.append(h_bhadron_pt)
h1d.append(h_bhadron_eta)
h1d.append(h_bhadron_pt_filtered)
h1d.append(h_counts_1b)
h1d.append(h_counts_sel1b)
h1d.append(h_bhadron_pt_withDaugtherFilter)
h1d.append(h_bhadron_pt_withDaugther)
h1d.append(h_phi_mass)
h1d.append(h_phi_mass_frommu)
h1d.append(h_phi_lxy)
h1d.append(acc_parent_pt_eta_level1)
h1d.append(acc_nonparent_pt_eta_level1)
h1d.append(acc_parent_pt_eta_level2)
h1d.append(acc_nonparent_pt_eta_level2)
h1d.append(acc_parent_pt_eta_level3)
h1d.append(acc_nonparent_pt_eta_level3)
h1d.append(acc_summary)

#### Write histograms
thisdir = os.environ.get("PWD")
if args.output=='':
    outdir = ("%s/plotsGeneration_"%(thisdir))+today
else:
    outdir = args.output
if not os.path.exists(outdir):
    os.makedirs(outdir)
foname = "%s/histograms_GEN_%s_%i_%i"%(outdir, mass, nmin, nmax)
fout = ROOT.TFile(foname+".root","RECREATE")
fout.cd()
for h in h1d:
    h.Write()
#for h in h2d:
#    h.Write()
fout.Close()


#### Control plots
hep.style.use("CMS")
for h in h1d:
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    hep.cms.label("", data=False, year='', com='13.6', ax=ax)
    hist, edges = getValues(h)
    hep.histplot(hist, edges, color='b', histtype="step", ax=ax)
    fig.savefig("%s/%s.png"%(outdir,h.GetName()), dpi=140)

