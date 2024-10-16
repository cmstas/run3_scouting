#include "../CMSSW_13_3_0/src/HiggsAnalysis/CombinedLimit/interface/RooDoubleCBFast.h"
#include "../CMSSW_13_3_0/src/HiggsAnalysis/CombinedLimit/interface/RooBernsteinFast.h"
#include "../CMSSW_13_3_0/src/HiggsAnalysis/CombinedLimit/interface/RooMultiPdf.h"

#include "RooCategory.h"
#include "RooWorkspace.h"
#include "RooFitResult.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooRealVar.h"
#include "RooHist.h"
#include "RooCurve.h"
#include "RooPlot.h"
#include "RooBinning.h"
#include "RooAddPdf.h"
#include "RooFFTConvPdf.h"
#include "RooGaussian.h"
#include "RooVoigtian.h"
#include "RooBreitWigner.h"
#include "RooCBShape.h"
#include "RooBernstein.h"
#include "RooChebychev.h"
#include "RooPolynomial.h"
#include "RooExponential.h"
#include "RooGenericPdf.h"
#include "RooExtendPdf.h"
#include "RooUniform.h"

#include "TCanvas.h"
#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TH1F.h"
#include "TF1.h"
#include "TSpline.h"
#include "TMath.h"
#include "TSystem.h"

#include "Math/ProbFunc.h"
#include "Math/QuantFunc.h"

#include <map>
#include <iostream>
#include <iomanip>
#include <sys/stat.h>
#include <filesystem>
#include <string>

//#include "../NanoCORE/Tools/widths.h"

using namespace std;
using namespace RooFit;

bool doBinnedFit = false;
//bool refitSignal = false;
bool categorizeSignal = true;
bool categorizeBackground = true; 
bool useFixedSigma = false;
bool addBernsteinOrders = false;
//bool saveFitResult = true;
bool saveFitResult = false;
bool drawFits = false;
bool drawResidual = false;
//
bool useOnlyExponential = false;
bool useOnlyPowerLaw = false;
bool useOnlyBernstein = false;
bool doNotUseMultiPDF = ( useOnlyExponential || useOnlyPowerLaw || useOnlyBernstein ) ? true : false;

void fitmass(RooDataSet mmumuAll, TString sample, bool isData, bool isSignal, bool isSignalMC, TString sigmodel, float samplemass, float mass, float ctau, RooWorkspace &wfit, bool fourmu, TString period, TString sigshape="dcbfastg", const char* outDir = "fitResults")
{
  cout << "WE ARE FITTING: " << isSignal << endl;
  //TString outDir = outDirPrefix+"_"+year;
  //TString outDir = Form("%s_%s",outDirPrefix.Data(), year.Data());
  int mdir = mkdir(outDir,0755);

  double minmass = 0.4;
  double maxmass = 140.;
  double minMforFit = minmass;

  bool refitSignal = true;
  TString datasetname(mmumuAll.GetName());

  // Get the lxy range to obtain the initial fit parameters
  //
  TString lxyString;
  if ( datasetname.Contains("d_FourMu_sep") ) lxyString = "d_FourMu_sep";
  else if ( datasetname.Contains("d_FourMu_osv") ) lxyString = "d_FourMu_sep";
  else if ( datasetname.Contains("lxy0p0to0p2") ) lxyString = "d_Dimuon_lxy0p0to0p2_inclusive";
  else if ( datasetname.Contains("lxy0p2to1p0") ) lxyString = "d_Dimuon_lxy0p2to1p0_inclusive";
  else if ( datasetname.Contains("lxy1p0to2p4") ) lxyString = "d_Dimuon_lxy1p0to2p4_inclusive";
  else if ( datasetname.Contains("lxy2p4to3p1") ) lxyString = "d_Dimuon_lxy2p4to3p1_inclusive";
  else if ( datasetname.Contains("lxy3p1to7p0") ) lxyString = "d_Dimuon_lxy3p1to7p0_inclusive";
  else if ( datasetname.Contains("lxy7p0to11p0") ) lxyString = "d_Dimuon_lxy7p0to11p0_inclusive";
  else if ( datasetname.Contains("lxy11p0to16p0") ) lxyString = "d_Dimuon_lxy11p0to16p0_inclusive";
  else if ( datasetname.Contains("lxy16p0to70p0") ) lxyString = "d_Dimuon_lxy16p0to70p0_inclusive";

  bool useSpline = true; 
  double minMforSpline =  200.0;
  double maxMforSpline = 2000.0;
  //if ( mass < (minMforSpline - 0.001) || mass > (maxMforSpline + 0.001) )
  //  useSpline = false;
  //TFile *ffitParams = TFile::Open("utils/signalFitParameters_default.root", "READ");
  TFile *ffitParams = TFile::Open("utils/signalFitParameters_lxybins_2022_v3.root", "READ");
  // Provisional: m = 0.5 doesn't have MC to have a defined peak, so we take initial fit parameters from 0.7:
  if (samplemass < 0.7) samplemass = 0.7;
  
  //////Set starting standard deviation (sigma)
  double stddev = 0.018*mass; // Updated, before 2%
  double minstddev = 0.01*mass;
  double maxstddev = 0.25*mass;
  double stddev_window = 0.018*mass; // Updated, before 2%
  double minstddev_window = 0.01*mass;
  double maxstddev_window = 0.25*mass;
  //
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *fstddev = (TSpline5 *) ffitParams->Get(Form("splines_%s", lxyString.Data()));
      stddev = fstddev->Eval(samplemass);
    }
    else {
      TF1 *fstddev = (TF1 *) ffitParams->Get("fsigma");
      stddev = fstddev->Eval(mass);
    }
    stddev = std::max(1.0e-6, stddev);
    minstddev = 0.75*stddev;
    maxstddev = 1.25*stddev;      
  }
  double binsize = 0.1*stddev_window;
  double binsizePlot = 1.0*stddev_window;

  // For Four muon regions there is not a proper spline that works for sigma at every mass, so we take 1.8%
  if ( datasetname.Contains("d_FourMu_")) {
    stddev = stddev_window;
    minstddev = 0.75*stddev;
    maxstddev = 1.25*stddev;
  }

  // Always use as starting point the hypothesis mass
  double meanm = mass;
  /*
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *fmean = (TSpline5 *) ffitParams->Get(Form("splinem_%s", lxyString.Data()));
      //TSpline5 *fmean = (TSpline5 *) ffitParams->Get("splinem", lxyString.Data()));
      meanm = fmean->Eval(mass);
    }
    else {
      TF1 *fmean = (TF1 *) ffitParams->Get("fmean");
      meanm = fmean->Eval(mass);
    }
  }
  */

  //////Set starting alphaR
  double alphaR = 1.0;
  double minalphaR = 0.1;
  double maxalphaR = 10.0;
  //
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *falphaR = (TSpline5 *) ffitParams->Get(Form("splineaR_%s", lxyString.Data()));
      alphaR = falphaR->Eval(samplemass);
    }
    else {
      TF1 *falphaR = (TF1 *) ffitParams->Get("faR");
      alphaR = falphaR->Eval(mass);
    }
    alphaR = std::max(1.0e-3, alphaR);
    minalphaR = 0.75*alphaR;
    maxalphaR = 1.25*alphaR;
  }

  //////Set starting alphaL
  double alphaL = 1.0;
  double minalphaL = 0.1;
  double maxalphaL = 10.0;
  //
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *falphaL = (TSpline5 *) ffitParams->Get(Form("splineaL_%s", lxyString.Data()));
      alphaL = falphaL->Eval(samplemass);
    }
    else {
      TF1 *falphaL = (TF1 *) ffitParams->Get("faL");
      alphaL = falphaL->Eval(mass);
    }
    alphaL = std::max(1.0e-3, alphaL);
    minalphaL = 0.75*alphaL;
    maxalphaL = 1.25*alphaL;
  }

  //////Set starting nR
  double nR = 6.0;
  double minnR = 1.0;
  double maxnR = 15.0;
  //
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *fnR = (TSpline5 *) ffitParams->Get(Form("splinenR_%s", lxyString.Data()));
      nR = fnR->Eval(samplemass);
    }
    else {
      TF1 *fnR = (TF1 *) ffitParams->Get("fnR");
      nR = fnR->Eval(mass);
    }
    nR = std::max(1.25, nR); // Making 1.23 instead of 1.0 to give extra estability to the function
    minnR = 0.75*nR;
    maxnR = 1.25*nR;
  }
  //////Set starting nL
  double nL = 2.0;
  double minnL = 1.0;
  double maxnL = 5.0;
  //
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *fnL = (TSpline5 *) ffitParams->Get(Form("splinenL_%s", lxyString.Data()));
      nL = fnL->Eval(samplemass);
    }
    else {
      TF1 *fnL = (TF1 *) ffitParams->Get("fnL");
      nL = fnL->Eval(mass);
    }
    nL = std::max(1.0, nL);
    minnL = 0.75*nL;
    maxnL = 1.25*nL;
  }

  //////Set starting frac
  double frac = 0.5;
  double minfrac = 0.0;
  double maxfrac = 1.0;
  //
  if ( !useFixedSigma ) {
    if ( useSpline ) { 
      TSpline5 *ffrac = (TSpline5 *) ffitParams->Get(Form("splinef_%s", lxyString.Data()));
      frac = ffrac->Eval(samplemass);
    }
    else {
      TF1 *ffrac = (TF1 *) ffitParams->Get("ff");
      frac = ffrac->Eval(mass);
    }
    frac = std::max(1.0e-03, frac);
    minfrac = 0.75*frac;
    maxfrac = std::max(1.0, 1.25*frac);
  }

  ffitParams->Close();

  std::cout  << " >>> Initial value of signal fit parameters: " << std::endl;
  std::cout << "- mean: " << meanm << std::endl;
  std::cout << "- sigma: " << stddev << std::endl;
  std::cout << "- nL: " << nL << std::endl;
  std::cout << "- nR: " << nR << std::endl;
  std::cout << "- alphaL: " << alphaL << std::endl;
  std::cout << "- alphaR: " << alphaR << std::endl;
  std::cout << "- mcfrac: " << frac << std::endl;

  // Veto of SM resonances: leave the workspace empty if hitting SM resonance boundaries for the background
  // Signal is kept for interpolation purposes
  // We use the sample mass: If dimuons fall within the window, we are out...
  double lowBound = samplemass-5.0*0.018*samplemass;
  double upBound = samplemass+5.0*0.018*samplemass;
  cout << isSignal << "Before veto: " << lowBound << "  " << upBound << endl;
  if ( !isSignal ) {
    if ( (( lowBound < 0.49 ) && (samplemass > 0.49)) || (( upBound > 0.43 ) && (samplemass < 0.43)) || ((samplemass > 0.43) && (samplemass < 0.49)) ) // Ks
      return;
    if ( (( lowBound < 0.58 ) && (samplemass > 0.58)) || (( upBound > 0.52 ) && (samplemass < 0.52)) || ((samplemass > 0.52) && (samplemass < 0.58)) ) // eta
      return;
    if ( (( lowBound < 0.84) && (samplemass > 0.84)) || (( upBound > 0.73 ) && (samplemass < 0.73)) || ((samplemass > 0.73) && (samplemass < 0.84)) ) // rho / w
      return;
    if ( (( lowBound < 1.08 ) && (samplemass > 1.08)) || (( upBound > 0.96 ) && (samplemass < 0.96)) || ((samplemass > 0.96) && (samplemass < 1.08)) ) // phi 1020
      return;
    if ( (( lowBound < 3.27 ) && (samplemass > 3.27)) || (( upBound > 2.91 ) && (samplemass < 2.91)) || ((samplemass > 2.91) && (samplemass < 3.27)) ) // Jpsi
      return;
    if ( (( lowBound < 3.89 ) && (samplemass > 3.89)) || (( upBound > 3.47 ) && (samplemass < 3.47)) || ((samplemass > 3.47) && (samplemass < 3.89)) ) // Psi 2S
      return;
    if ( (( lowBound < 9.87 ) && (samplemass > 9.87)) || (( upBound > 8.99 ) && (samplemass < 8.99)) || ((samplemass > 8.99) && (samplemass < 9.87)) ) // Upsilon 1S
      return;
    if ( (( lowBound < 10.39 ) && (samplemass > 10.39)) || (( upBound > 9.61 ) && (samplemass < 9.61)) || ((samplemass > 9.61) && (samplemass < 10.39)) ) // Upsilon 2S
      return;
    if ( (( lowBound < 10.77 ) && (samplemass > 10.77)) || (( upBound > 9.87 ) && (samplemass < 9.87)) || ((samplemass > 9.87) && (samplemass < 10.77)) ) // Upsilon 3S
      return;
  }


  if ( isSignal ) {

    if ( !(isSignalMC) ) {
      refitSignal = false;
      saveFitResult = false;
      drawFits = false;
      drawResidual = false;
    }

    double gamma = 0.001*mass;

    TString fitRange;
    TString varname;
    if (fourmu) {
      fitRange = Form("%f < m4fit && m4fit < %f",std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
      varname = "m4fit";
    } else { 
      fitRange = Form("%f < mfit && mfit < %f",std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
      varname = "mfit";
    }

    //////Get RooRealVar from RooDataSet
    RooRealVar mfit(varname, varname, std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
    std::cout << ">>> INITIAL SIGNAL NORMALIZATION: " << mmumuAll.numEntries() << " " << mmumuAll.sumEntries() << " " << mmumuAll.sumEntries(fitRange.Data()) << std::endl;
    std::unique_ptr<RooDataSet> mmumu{static_cast<RooDataSet*>(mmumuAll.reduce(RooArgSet(mfit),fitRange))};
    (*mmumu).Print();
    RooRealVar* xref = nullptr;
    if (fourmu)
      xref = (RooRealVar*) (*mmumu).get()->find("m4fit");
    else 
      xref = (RooRealVar*) (*mmumu).get()->find("mfit");
    RooRealVar &x = *xref;
    x.Print();
    x.setRange("fitRange",std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
    int nBins = (mass+5.0*stddev_window - std::max(minMforFit,mass-5.0*stddev_window))/binsize;
    int nBinsPlot = (mass+5.0*stddev_window - std::max(minMforFit,mass-5.0*stddev_window))/(0.5*binsizePlot);
    if ( doBinnedFit )
      x.setBins(nBins);
    RooBinning binningPlot(nBinsPlot,std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);

    RooPlot *frame = x.frame(std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
    frame->SetTitle("");//Signal dimuon mass fit");
    frame->SetMinimum(0.0);
    //////Plot RooDataSet onto frame
    (*mmumu).plotOn(frame, DataError(RooAbsData::SumW2), Binning(binningPlot));

    //////Define fit-related variables
    int nMaxFitAttempts = 5;
    int nFitParams = 0;
    RooFitResult *r = new RooFitResult();

    //////Define index over event categories
    ////// binidx=0: nB>0
    ////// binidx=1: nB=1
    ////// binidx=2: nB>1    
    int binidx=-1;
    TString datasetname((*mmumu).GetName());
    if ( datasetname.Contains("d_FourMu_sep") ) binidx=1;
    else if ( datasetname.Contains("d_FourMu_osv") ) binidx=2;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso0_ptlow") ) binidx=3;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso0_pthigh") ) binidx=4;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso1_ptlow") ) binidx=5;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso1_pthigh") ) binidx=6;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso0_ptlow") ) binidx=7;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso0_pthigh") ) binidx=8;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso1_ptlow") ) binidx=9;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso1_pthigh") ) binidx=10;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso0_ptlow") ) binidx=11;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso0_pthigh") ) binidx=12;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso1_ptlow") ) binidx=13;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso1_pthigh") ) binidx=14;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso0_ptlow") ) binidx=15;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso0_pthigh") ) binidx=16;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso1_ptlow") ) binidx=17;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso1_pthigh") ) binidx=18;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso0_ptlow") ) binidx=19;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso0_pthigh") ) binidx=20;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso1_ptlow") ) binidx=21;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso1_pthigh") ) binidx=22;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso0_ptlow") ) binidx=23;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso0_pthigh") ) binidx=24;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso1_ptlow") ) binidx=25;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso1_pthigh") ) binidx=26;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso0_ptlow") ) binidx=27;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso0_pthigh") ) binidx=28;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso1_ptlow") ) binidx=29;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso1_pthigh") ) binidx=30;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso0_ptlow") ) binidx=31;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso0_pthigh") ) binidx=32;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso1_ptlow") ) binidx=33;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso1_pthigh") ) binidx=34;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_non-pointing") ) binidx=35;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_non-pointing") ) binidx=36;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_non-pointing") ) binidx=37;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_non-pointing") ) binidx=38;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_non-pointing") ) binidx=39;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_non-pointing") ) binidx=40;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_non-pointing") ) binidx=41;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_non-pointing") ) binidx=42;
    TString catExt = "";
    if ( categorizeSignal ) 
      catExt = Form("_ch%d_%s",binidx, period.Data());
    mmumu->SetName(Form("signalRooDataSet%s",catExt.Data()));    
    double sigNormalization =-1.0;
    double sigRawEntries = -1.0;
    if ( isSignalMC ) {
      sigNormalization = (*mmumu).sumEntries(fitRange.Data());
      sigRawEntries = (*mmumu).numEntries();
      if (sigNormalization < 1e-6) {
        sigNormalization = 1e-6;
      }
      if (sigRawEntries < 1e-6) {
        sigRawEntries = 1e-6;
      }
      if (sigRawEntries < 10) {
        refitSignal = false;
      }
      std::cout << ">>> SIGNAL NORMALIZATION: " << (*mmumu).numEntries() << " " << (*mmumu).sumEntries() << " " << (*mmumu).sumEntries(fitRange.Data()) << std::endl;
    }
    else {
      TFile *facc = TFile::Open("../data/acceptanceSplines_2022.root");
      TSpline3 *acceff = (TSpline3 *) facc->Get(Form("spline_acceptance_%s_%.0f_%s",sigmodel.Data(),ctau,datasetname.Data()));
      double tacceff  = acceff->Eval(samplemass);
      facc->Close();
      int sigRawAll = 1e6; // Random for now... But will have to include it for the systematics...
      if (period.Contains("2022"))
        sigNormalization = tacceff*1000*35;
      else
        sigNormalization = tacceff*1000*27;
      sigRawEntries = (int) (sigNormalization/(tacceff*1000*35)*sigRawAll);
    }
    std::cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Import of the signal " << std::endl;
    std::cout << "Refitting signal? " << refitSignal << std::endl;
    RooRealVar nSig(Form("signalNorm%s",catExt.Data()),Form("signalNorm%s",catExt.Data()),sigNormalization);
    RooRealVar nSigRaw(Form("signalRawNorm%s",catExt.Data()),Form("signalRawNorm%s",catExt.Data()),sigRawEntries);
    wfit.import(*(mmumu));
    wfit.import(nSig);
    wfit.import(nSigRaw);

    if (sigshape=="gaus"){
      RooRealVar mean(Form("mean%s",catExt.Data()),Form("mean%s",catExt.Data()),meanm,meanm-stddev,meanm+stddev);
      RooRealVar sigma(Form("sigma%s",catExt.Data()),Form("sigma%s",catExt.Data()),stddev,minstddev,maxstddev);
      RooGaussian signal(Form("signal%s",catExt.Data()),Form("signal%s",catExt.Data()),x,mean,sigma);
      nFitParams = 2;
      //////Fit
      int nFits = 0;
      if ( refitSignal ) {
	while ( nFits < nMaxFitAttempts ) {
	  //r = signal.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), /*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
	  r = signal.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), SumW2Error(kTRUE), PrintLevel(-1), PrintEvalErrors(-1));
	  ++nFits;
	  if ( r->status()==0 )
	    break;
	}
      }
      signal.plotOn(frame,Name("signal"),Range("fitRange"),RooFit::NormRange("fitRange"));
      //////Import model and all its components into the workspace      
      mean.removeError();
      sigma.removeError();
      wfit.import(signal);
    }
    else if (sigshape=="voigt"){
      RooRealVar mean(Form("mean%s",catExt.Data()),Form("mean%s",catExt.Data()),meanm,meanm-stddev,meanm+stddev);
      //RooRealVar width(Form("width%s",catExt.Data()),Form("width%s",catExt.Data()),gamma,0.75*gamma,1.25*gamma);
      RooRealVar width(Form("width%s",catExt.Data()),Form("width%s",catExt.Data()),gamma);
      RooRealVar sigma(Form("sigma%s",catExt.Data()),Form("sigma%s",catExt.Data()),stddev,minstddev,maxstddev);
      RooVoigtian signal(Form("signal%s",catExt.Data()),Form("signal%s",catExt.Data()),x,mean,width,sigma);
      //nFitParams = 3;
      nFitParams = 2;
      //////Fit
      int nFits = 0;
      if ( refitSignal ) {
	while ( nFits < nMaxFitAttempts ) {
	  //r = signal.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), /*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
	  r = signal.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), SumW2Error(kTRUE), PrintLevel(-1), PrintEvalErrors(-1));
	  ++nFits;
	  if ( r->status()==0 )
	    break;
	}
      }
      signal.plotOn(frame,Name("signal"),Range("fitRange"),RooFit::NormRange("fitRange"));
      //////Import model and all its components into the workspace
      mean.removeError();
      width.removeError();
      sigma.removeError();
      wfit.import(signal);
    }
    else if (sigshape=="dcbfast"){
      RooRealVar mean(Form("mean%s",catExt.Data()),Form("mean%s",catExt.Data()),meanm,meanm-stddev,meanm+stddev);
      RooRealVar sigma(Form("sigma%s",catExt.Data()),Form("sigma%s",catExt.Data()),stddev,minstddev,maxstddev);
      RooRealVar alpha_1(Form("alphaR%s",catExt.Data()),Form("alphaR%s",catExt.Data()),alphaR, minalphaR, maxalphaR);
      RooRealVar alpha_2(Form("alphaL%s",catExt.Data()),Form("alphaL%s",catExt.Data()),alphaL, minalphaL, maxalphaL);
      RooRealVar n_1(Form("nR%s",catExt.Data()),Form("nR%s",catExt.Data()), nR, minnR, maxnR);
      RooRealVar n_2(Form("nL%s",catExt.Data()),Form("nL%s",catExt.Data()), nL, minnL, maxnL);
      RooDoubleCBFast signal_(Form("signal_%s",catExt.Data()),Form("signal_%s",catExt.Data()),x,mean,sigma,alpha_2,n_2,alpha_1,n_1);
      nFitParams = 6;
      ////Fit
      int nFits = 0;
      if ( refitSignal ) {
	while ( nFits < nMaxFitAttempts ) {
	  //r = signal_.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), /*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
	  r = signal_.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), SumW2Error(kTRUE), PrintLevel(-1), PrintEvalErrors(-1));
	  ++nFits;
	  if ( r->status()==0 )
	    break;
	}
      }
      signal_.plotOn(frame,Name("signal_"),Range("fitRange"),RooFit::NormRange("fitRange"));
      //////Import model and all its components into the workspace
      mean.removeError();
      sigma.removeError();
      alpha_1.removeError();
      alpha_2.removeError();
      n_1.removeError();
      n_2.removeError();
      RooRealVar mean_(Form("mean%s",catExt.Data()),Form("mean%s",catExt.Data()),mean.getValV()); mean_.setConstant(true);
      RooRealVar sigma_(Form("sigma%s",catExt.Data()),Form("sigma%s",catExt.Data()),sigma.getValV()); sigma_.setConstant(true);
      RooRealVar alpha_1_(Form("alphaR%s",catExt.Data()),Form("alphaR%s",catExt.Data()),alpha_1.getValV()); alpha_1_.setConstant(true);
      RooRealVar alpha_2_(Form("alphaL%s",catExt.Data()),Form("alphaL%s",catExt.Data()),alpha_2.getValV()); alpha_2_.setConstant(true);
      RooRealVar n_1_(Form("nR%s",catExt.Data()),Form("nR%s",catExt.Data()), n_1.getValV()); n_1_.setConstant(true);
      RooRealVar n_2_(Form("nL%s",catExt.Data()),Form("nL%s",catExt.Data()), n_2.getValV()); n_2_.setConstant(true);
      RooDoubleCBFast signal(Form("signal%s",catExt.Data()),Form("signal%s",catExt.Data()),x,mean_,sigma_,alpha_2_,n_2_,alpha_1_,n_1_);
      signal.plotOn(frame,Name("signal"),Range("fitRange"),RooFit::NormRange("fitRange"));
      wfit.import(signal);
    }
    else if (sigshape=="dcbfastg"){
      RooRealVar mean(Form("mean%s",catExt.Data()),Form("mean%s",catExt.Data()),meanm,meanm-stddev,meanm+stddev);
      RooRealVar sigma(Form("sigma%s",catExt.Data()),Form("sigma%s",catExt.Data()),stddev,minstddev,maxstddev);
      RooGaussian gaus(Form("gauss%s",catExt.Data()),Form("gauss%s",catExt.Data()),x,mean,sigma);
      RooRealVar alpha_1(Form("alphaR%s",catExt.Data()),Form("alphaR%s",catExt.Data()),alphaR, minalphaR, maxalphaR);
      RooRealVar alpha_2(Form("alphaL%s",catExt.Data()),Form("alphaL%s",catExt.Data()),alphaL, minalphaL, maxalphaL);
      RooRealVar n_1(Form("nR%s",catExt.Data()),Form("nR%s",catExt.Data()), nR, minnR, maxnR);
      RooRealVar n_2(Form("nL%s",catExt.Data()),Form("nL%s",catExt.Data()), nL, minnL, maxnL);
      RooDoubleCBFast dcb(Form("dcb%s",catExt.Data()),Form("dcb%s",catExt.Data()),x,mean,sigma,alpha_2,n_2,alpha_1,n_1);
      RooRealVar mc_frac(Form("mcfrac%s",catExt.Data()),Form("mcfrac%s",catExt.Data()), frac, minfrac, maxfrac);
      RooAddPdf signal_(Form("signal_%s",catExt.Data()),Form("signal_%s",catExt.Data()), RooArgList(gaus,dcb), RooArgList(mc_frac), true);
      nFitParams = 7;
      ////Fit
      int nFits = 0;
      if ( refitSignal ) {
	while ( nFits < nMaxFitAttempts ) {
	  //r = signal_.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), /*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
	  r = signal_.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), SumW2Error(kTRUE), PrintLevel(-1), PrintEvalErrors(-1));
	  ++nFits;
	  if ( r->status()==0 )
	    break;
	}
      }
      signal_.plotOn(frame,Name("signal_"),Range("fitRange"),RooFit::NormRange("fitRange"));
      //////Import model and all its components into the workspace
      mean.removeError(); 
      sigma.removeError();
      alpha_1.removeError();
      alpha_2.removeError();
      n_1.removeError();
      n_2.removeError();
      RooRealVar mean_(Form("mean%s",catExt.Data()),Form("mean%s",catExt.Data()),mean.getValV(),mean.getMin(),mean.getMax()); mean_.setConstant(true);
      RooRealVar sigma_(Form("sigma%s",catExt.Data()),Form("sigma%s",catExt.Data()),sigma.getValV(),sigma.getMin(),sigma.getMax()); sigma_.setConstant(true);
      RooGaussian gaus_(Form("gauss%s",catExt.Data()),Form("gauss%s",catExt.Data()),x,mean_,sigma_);
      RooRealVar alpha_1_(Form("alphaR%s",catExt.Data()),Form("alphaR%s",catExt.Data()),alpha_1.getValV(),alpha_1.getMin(),alpha_1.getMax()); alpha_1_.setConstant(true);
      RooRealVar alpha_2_(Form("alphaL%s",catExt.Data()),Form("alphaL%s",catExt.Data()),alpha_2.getValV(),alpha_2.getMin(),alpha_2.getMax()); alpha_2_.setConstant(true);
      RooRealVar n_1_(Form("nR%s",catExt.Data()),Form("nR%s",catExt.Data()), n_1.getValV(),n_1.getMin(),n_1.getMax()); n_1_.setConstant(true);
      RooRealVar n_2_(Form("nL%s",catExt.Data()),Form("nL%s",catExt.Data()), n_2.getValV(),n_2.getMin(),n_2.getMax()); n_2_.setConstant(true);
      RooDoubleCBFast dcb_(Form("dcb%s",catExt.Data()),Form("dcb%s",catExt.Data()),x,mean_,sigma_,alpha_2_,n_2_,alpha_1_,n_1_);
      RooRealVar mc_frac_(Form("mcfrac%s",catExt.Data()),Form("mcfrac%s",catExt.Data()), mc_frac.getValV(),mc_frac.getMin(),mc_frac.getMax()); mc_frac_.setConstant(true);
      RooAddPdf signal(Form("signal%s",catExt.Data()),Form("signal%s",catExt.Data()), RooArgList(gaus_,dcb_), RooArgList(mc_frac_), true);
      signal.plotOn(frame,Name("signal"),Range("fitRange"),RooFit::NormRange("fitRange"));
      wfit.import(signal);
    }
    else{
      cout << "Signal PDF is unknown. Exiting..." << endl;
      return;
    }

    double chi2 = 0.0;
    int nEmptyBins = 0;
    //////Construct histograms with residuals and pulls of the data w.r.t. the curve
    RooHist *hresid = frame->residHist();
    RooHist *hpull = frame->pullHist();
    RooCurve *fitcurve = frame->getCurve("signal");
    //////Determine range of curve 
    Double_t xstart,xstop,y;
    fitcurve->GetPoint(0,xstart,y);
    fitcurve->GetPoint(fitcurve->GetN()-1,xstop,y);
    int nPoints = hresid->GetN();
    cout << nPoints << endl;
    for (int i = 0; i < nPoints; i++) {
      double b, point;
      hpull->GetPoint(i,b,point);
      if (b<xstart || b>xstop) continue;
      if (point==0) {
    	++nEmptyBins;
      }
      else {
    	hresid->GetPoint(i,b,point);
    	chi2 += point*point / (fitcurve->interpolate(b));
      }
    }

    if ( refitSignal ) {
      //////Access fit result information
      //r->Print();
      //////Access basic information
      cout << "Status = " << r->status() << endl;
      cout << "EDM = " << r->edm() << endl;
      cout << "-log(L) at minimum = " << r->minNll() << endl;
      //////Access list of final fit parameter values
      cout << "Final value of floating parameters:" << endl;
      r->floatParsFinal().Print("s");
      //////Evaluate chi-square:
      cout << "chiSquare = " << frame->chiSquare(nFitParams) << endl;
      cout << "chiSquare (from residual histogram) / NDOF = " << chi2 << " / " << std::max(nFitParams,nPoints-nEmptyBins-nFitParams) << endl;
      cout << "p-value (chiSquare, NDOF) = " << ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams))) << endl;
    }

    if ( drawFits ) {
      //////Draw fit
      TCanvas *can = new TCanvas("can","",600,600);
      can->cd();
      frame->SetMinimum(0.0);
      frame->SetLabelSize(0.02,"Y");
      frame->SetTitleSize(0.025,"Y");
      frame->SetXTitle("Dimuon mass [GeV]");
      frame->Draw();
      //can->SaveAs(Form("%s/%s_fitSignal_%s_%s_M%.0f_ch%d.png",outDir,(*mmumu).GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx));
      can->SaveAs(Form("%s/%s_fitSignal_%s_%s_M%.0f_ch%d.png",outDir,mmumuAll.GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx));
      can->Update();
      can->Clear();
      can->Close();
    }
    
    if ( drawResidual ) {
      //Create a dedicated frame to draw the residual distribution and add the distribution to the frame
      RooPlot *frameres = x.frame(Title("Residual Distribution"));
      frameres->addPlotable(hresid, "P");
      frameres->SetXTitle("Dimuon mass [GeV]");
      TCanvas *can = new TCanvas("can","",600,600);
      can->cd();
      frameres->Draw();
      //can->SaveAs(Form("%s/%s_fitResidual_%s_%s_M%.0f_ch%d.png",outDir,(*mmumu).GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx));
      can->SaveAs(Form("%s/%s_fitResidual_%s_%s_M%.0f_ch%d.png",outDir,mmumuAll.GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx));
      can->Update();
      can->Clear();
    
      //Create a dedicated frame to draw the pull distribution and add the distribution to the frame
      RooPlot *framepull = x.frame(Title("Pull Distribution"));
      framepull->addPlotable(hpull, "P");
      framepull->SetXTitle("Dimuon mass [GeV]");
      can->cd();
      framepull->Draw();
      //can->SaveAs(Form("%s/%s_fitPull_%s_%s_M%.0f_ch%d.png",outDir,(*mmumu).GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx));
      can->SaveAs(Form("%s/%s_fitPull_%s_%s_M%.0f_ch%d.png",outDir,mmumuAll.GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx));
      can->Update();
      can->Clear();
      can->Close();
    }
    
    if ( saveFitResult ) {
      //////Save RooFitResult into a ROOT file
      TFile ffitresult(Form("%s/%s_fitResult_%s_%s_M%.0f_ch%d.root",outDir,(*mmumu).GetName(),sigshape.Data(),sigmodel.Data(),mass,binidx),"RECREATE");
      r->Write("fitResult");
      ffitresult.Close();
    }

  }
  else {

    //////Get RooRealVar from RooDataSet
    TString fitRange;
    TString varname;
    if (fourmu) {
      fitRange = Form("%f < m4fit && m4fit < %f",std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
      varname = "m4fit";
    } else { 
      fitRange = Form("%f < mfit && mfit < %f",std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
      varname = "mfit";
    }
    //////Get RooRealVar from RooDataSet
    RooRealVar mfit(varname, varname, std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
    std::unique_ptr<RooDataSet> mmumu{static_cast<RooDataSet*>(mmumuAll.reduce(RooArgSet(mfit),fitRange))};
    //if ((*mmumu).numEntries() < 1)
    //  return;
    RooRealVar* xref = nullptr;
    if (fourmu)
      xref = (RooRealVar*) (*mmumu).get()->find("m4fit");
    else
      xref = (RooRealVar*) (*mmumu).get()->find("mfit");
    RooRealVar &x = *xref;
    x.setRange("fitRange",std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
    int nBins = (mass+5.0*stddev_window - std::max(minMforFit,mass-5.0*stddev_window))/binsize;
    int nBinsPlot = (mass+5.0*stddev_window - std::max(minMforFit,mass-5.0*stddev_window))/binsizePlot;
    if ( doBinnedFit )
      x.setBins(nBins);
    RooBinning binningPlot(nBinsPlot,std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);

    RooDataSet *mmumuFit;
    double bgNormalizationForToy = (*mmumu).sumEntries(fitRange.Data());
    RooRealVar nBGForToy(Form("bgNormalizationForToy_%s_%.0f",(*mmumu).GetName(),mass),Form("bgNormalizationForToy_%s_%.0f",(*mmumu).GetName(),mass),bgNormalizationForToy);
    //////If using MC, fit RooDataSet with exponential PDF, then build MC toy dataset
    if ( !isData ) {
      TString thisname = (*mmumu).GetName();
      //////Exponential PDF
      RooRealVar expo_slope_forToy(Form("expo_slope_forToy_%s_mass%.0f",(*mmumu).GetName(),mass),Form("expo_slope_forToy_%s_mass%.0f",(*mmumu).GetName(),mass),-0.02,-0.1,-0.0001);
      RooExponential exponential_forToy(Form("background_exponential_forToy_%s_mass%.0f",(*mmumu).GetName(),mass),Form("background_exponential_forToy_%s_mass%.0f",(*mmumu).GetName(),mass),x,expo_slope_forToy);
      RooFitResult* r_forToy = exponential_forToy.fitTo((*mmumu), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"), SumW2Error(kTRUE), PrintLevel(-1), PrintEvalErrors(-1));
      RooDataSet mmumuTOY = *(exponential_forToy.generate(RooArgSet(x),(*mmumu),std::max(1,int(bgNormalizationForToy)), false, true, true));
      
      mmumuFit = (RooDataSet*) mmumuTOY.Clone((*mmumu).GetName());

      RooPlot *frame = x.frame(std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
      frame->SetTitle("");//BG dimuon mass fit");
      frame->SetMinimum(0.0);
      
      //////Plot RooDataSet onto frame
      (*mmumu).plotOn(frame/*, DataError(RooAbsData::SumW2)*/, Binning(binningPlot), LineColor(kMagenta), MarkerColor(kMagenta));
      (*mmumuFit).plotOn(frame/*, DataError(RooAbsData::SumW2)*/, Binning(binningPlot));
      if ( drawFits ) {
	exponential_forToy.plotOn(frame,Name("background_toy"),Range("fitRange"),RooFit::NormRange("fitRange"));
	//////Draw fit
	TCanvas *can = new TCanvas("can","",600,600);
	can->cd();
	frame->SetMinimum(0.0);
	frame->SetLabelSize(0.02,"Y");
	frame->SetTitleSize(0.025,"Y");
	frame->SetXTitle("Dimuon mass [GeV]");
	frame->Draw();
	//can->SaveAs(Form("%s/%s_fitBackgroundTOY_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->SaveAs(Form("%s/%s_fitBackgroundTOY_mass%.0f.png",outDir,mmumuAll.GetName(),mass));
	can->Update();
	can->Clear();
	can->Close();
      }
    }
    else {
      mmumuFit = (RooDataSet*) (*mmumu).Clone((*mmumu).GetName());
    }

    RooPlot *frame = x.frame(std::max(minMforFit,mass-5.0*stddev_window),mass+5.0*stddev_window);
    frame->SetTitle("");//BG dimuon mass fit");
    frame->SetMinimum(0.0);

    //////Plot RooDataSet onto frame
    (*mmumuFit).plotOn(frame/*, DataError(RooAbsData::SumW2)*/, Binning(binningPlot));

    //////Define index over event categories
    int binidx=-1;
    TString datasetname((*mmumuFit).GetName());
    if ( datasetname.Contains("d_FourMu_sep") ) binidx=1;
    else if ( datasetname.Contains("d_FourMu_osv") ) binidx=2;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso0_ptlow") ) binidx=3;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso0_pthigh") ) binidx=4;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso1_ptlow") ) binidx=5;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_iso1_pthigh") ) binidx=6;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso0_ptlow") ) binidx=7;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso0_pthigh") ) binidx=8;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso1_ptlow") ) binidx=9;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_iso1_pthigh") ) binidx=10;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso0_ptlow") ) binidx=11;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso0_pthigh") ) binidx=12;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso1_ptlow") ) binidx=13;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_iso1_pthigh") ) binidx=14;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso0_ptlow") ) binidx=15;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso0_pthigh") ) binidx=16;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso1_ptlow") ) binidx=17;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_iso1_pthigh") ) binidx=18;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso0_ptlow") ) binidx=19;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso0_pthigh") ) binidx=20;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso1_ptlow") ) binidx=21;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_iso1_pthigh") ) binidx=22;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso0_ptlow") ) binidx=23;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso0_pthigh") ) binidx=24;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso1_ptlow") ) binidx=25;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_iso1_pthigh") ) binidx=26;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso0_ptlow") ) binidx=27;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso0_pthigh") ) binidx=28;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso1_ptlow") ) binidx=29;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_iso1_pthigh") ) binidx=30;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso0_ptlow") ) binidx=31;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso0_pthigh") ) binidx=32;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso1_ptlow") ) binidx=33;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_iso1_pthigh") ) binidx=34;
    else if ( datasetname.Contains("d_Dimuon_lxy0p0to0p2_non-pointing") ) binidx=35;
    else if ( datasetname.Contains("d_Dimuon_lxy0p2to1p0_non-pointing") ) binidx=36;
    else if ( datasetname.Contains("d_Dimuon_lxy1p0to2p4_non-pointing") ) binidx=37;
    else if ( datasetname.Contains("d_Dimuon_lxy2p4to3p1_non-pointing") ) binidx=38;
    else if ( datasetname.Contains("d_Dimuon_lxy3p1to7p0_non-pointing") ) binidx=39;
    else if ( datasetname.Contains("d_Dimuon_lxy7p0to11p0_non-pointing") ) binidx=40;
    else if ( datasetname.Contains("d_Dimuon_lxy11p0to16p0_non-pointing") ) binidx=41;
    else if ( datasetname.Contains("d_Dimuon_lxy16p0to70p0_non-pointing") ) binidx=42;
    TString catExt = "";
    if ( categorizeBackground ) 
      catExt = Form("_ch%d_%s",binidx, period.Data());

    //////Define fit-related variables
    int nMaxFitAttempts = 5;
    int nFitParams = 0;
    RooFitResult *r = new RooFitResult();

    (*mmumuFit).Print();
    mmumuFit->SetName(Form("data_obs%s",catExt.Data()));
    wfit.import(*(mmumuFit));

    double alpha = 1.0-0.6827;
    double bgNormalization = (*mmumuFit).sumEntries(fitRange.Data());
    double minNormalization = ROOT::Math::gamma_quantile(alpha/2.0, bgNormalization, 1);
    double maxNormalization = ROOT::Math::gamma_quantile_c(alpha/2.0, bgNormalization+1.0, 1);
    minNormalization = std::max(0.001,bgNormalization - 2.0*(bgNormalization-minNormalization));
    maxNormalization = bgNormalization + 2.0*(-bgNormalization+maxNormalization);
    if ( bgNormalization < 0.001 ) bgNormalization=0.001;

    RooRealVar nBG_exp(Form("background_exponential%s_norm",catExt.Data()),Form("background_exponential%s_norm",catExt.Data()),bgNormalization,minNormalization,maxNormalization);
    RooRealVar nBG_pow(Form("background_powerlaw%s_norm",catExt.Data()),Form("background_powerlaw%s_norm",catExt.Data()),bgNormalization,minNormalization,maxNormalization);
    RooRealVar nBG_pol(Form("background_bernstein%s_norm",catExt.Data()),Form("background_bernstein%s_norm",catExt.Data()),bgNormalization,minNormalization,maxNormalization);
    RooRealVar nBG(Form("roomultipdf%s_norm",catExt.Data()),Form("roomultipdf%s_norm",catExt.Data()),bgNormalization,minNormalization,maxNormalization);

    //////Exponential PDF
    //RooRealVar expo_slope(Form("expo_slope%s",catExt.Data()),Form("expo_slope%s",catExt.Data()),-0.02,-0.1,-0.0001); // decreasing slope
    RooRealVar expo_slope(Form("expo_slope%s",catExt.Data()),Form("expo_slope%s",catExt.Data()),-0.02,-20.0,20.0);
    RooExponential exponential(Form("background_exponential%s",catExt.Data()),Form("background_exponential%s",catExt.Data()),x,expo_slope);
    //////Fit
    std::cout << "Exponential fit................." << std::endl;
    nFitParams = 1;
    int nFits = 0;
    while ( nFits < nMaxFitAttempts) {
      r = exponential.fitTo((*mmumuFit), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"),/*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
      ++nFits;
      if ( r->status()==0 )
	break;
    }
    exponential.plotOn(frame,Name("background_exponential"),Range("fitRange"),RooFit::NormRange("fitRange"));

    double chi2 = 0.0;
    int nEmptyBins = 0;
    //////Construct histograms with residuals and pulls of the data w.r.t. the curve
    RooHist *hresid = frame->residHist();
    RooHist *hpull = frame->pullHist();
    RooCurve *fitcurve = frame->getCurve("background_exponential");
    //////Determine range of curve 
    Double_t xstart,xstop,y;
    fitcurve->GetPoint(0,xstart,y);
    fitcurve->GetPoint(fitcurve->GetN()-1,xstop,y);
    int nPoints = hresid->GetN();
    cout << nPoints << endl;
    for (int i = 0; i < nPoints; i++) {
      double b, point;
      hpull->GetPoint(i,b,point);
      if (b<xstart || b>xstop) continue;
      if (point==0) {
	++nEmptyBins;
      }
      else {
	hresid->GetPoint(i,b,point);
	chi2 += point*point / (fitcurve->interpolate(b));
      }
    }
    //////Access fit result information
    //r->Print();
    //////Access basic information
    cout << "Status = " << r->status() << endl;
    cout << "EDM = " << r->edm() << endl;
    cout << "-log(L) at minimum = " << r->minNll() << endl;
    //////Access list of final fit parameter values
    cout << "Final value of floating parameters:" << endl;
    r->floatParsFinal().Print("s");
    //////Evaluate chi-square:
    cout << "chiSquare = " << frame->chiSquare(nFitParams) << endl;
    cout << "chiSquare (from residual histogram) / NDOF = " << chi2 << " / " << std::max(nFitParams,nPoints-nEmptyBins-nFitParams) << endl;
    cout << "p-value (chiSquare, NDOF) = " << ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams))) << endl;

    if ( saveFitResult ) {
      //////Save RooFitResult into a ROOT file
      TFile ffitresult(Form("%s/%s_fitResult_exponential_mass%.0f.root",outDir,(*mmumuFit).GetName(),mass),"RECREATE");
      r->Write("fitResult");
      ffitresult.Close();
    }

    RooArgList bgPDFs;

    //////Select PDFs
    //////Chi2-based p-value
    int fitStatusExponential = r->status();
    double chi2ExponentialPvalue = ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams)));

    frame->remove("background_exponential");

    // If p-value is zero, fit does not converge, zero events, or less than 10 events and less than 0.1 events/GeV, do not include
    if ( chi2ExponentialPvalue > 0.01 &&
	 fitStatusExponential==0 &&
	 !( nBG.getVal() < 1 || ( nBG.getVal()/(mass+5.0*stddev_window-std::max(minMforFit,mass-5.0*stddev_window)) < 1e-1 && nBG.getVal() < 1e1 ) ) ) {
      bgPDFs.add(exponential);
      if ( useOnlyExponential ) 
	wfit.import(exponential);

      exponential.plotOn(frame,Name("background_exponential"),Range("fitRange"),RooFit::NormRange("fitRange"),LineColor(kRed));
      if ( drawFits ) {
	//////Draw fit
	TCanvas *can = new TCanvas("can","",600,600);
	can->cd();
	frame->SetMinimum(0.0);
	frame->SetLabelSize(0.02,"Y");
	frame->SetTitleSize(0.025,"Y");
	frame->SetXTitle("Dimuon mass [GeV]");
	frame->Draw();
	//can->SaveAs(Form("%s/%s_fitBackground_exponential_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->SaveAs(Form("%s/%s_fitBackground_exponential_mass%.0f.png",outDir,mmumuAll.GetName(),mass));
	can->Update();
	can->Clear();
	can->Close();
      }
      if ( drawResidual ) {
	//Create a dedicated frame to draw the residual distribution and add the distribution to the frame
	RooHist *hresid = frame->residHist();
	RooPlot *frameres = x.frame(Title("Residual Distribution"));
	frameres->addPlotable(hresid, "P");
	frameres->SetXTitle("Dimuon mass [GeV]");
	TCanvas *can = new TCanvas("can","",600,600);
	can->cd();
	frameres->Draw();
	can->SaveAs(Form("%s/%s_fitResidual_exponential_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->Update();
	can->Clear();
	
	//Create a dedicated frame to draw the pull distribution and add the distribution to the frame
	RooHist *hpull = frame->pullHist();
	RooPlot *framepull = x.frame(Title("Pull Distribution"));
	framepull->addPlotable(hpull, "P");
	framepull->SetXTitle("Dimuon mass [GeV]");
	can->cd();
	framepull->Draw();
	can->SaveAs(Form("%s/%s_fitPull_exponential_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->Update();
	can->Clear();
	can->Close();
      }
      frame->remove("background_exponential");
    }

    //////Power-law PDF
    std::cout << "Power-law fit................." << std::endl;
    //RooRealVar plaw_power(Form("plaw_power%s",catExt.Data()),Form("plaw_power%s",catExt.Data()),-3.0,-6.0,-0.0001); // Decreasing slope
    RooRealVar plaw_power(Form("plaw_power%s",catExt.Data()),Form("plaw_power%s",catExt.Data()),-3.0,-25.0,12.0);
    RooGenericPdf powerlaw(Form("background_powerlaw%s",catExt.Data()),"TMath::Power(@0,@1)",RooArgList(x,plaw_power));
    //////Fit
    nFitParams = 1;
    nFits = 0;
    while ( nFits < nMaxFitAttempts ) {
      r = powerlaw.fitTo((*mmumuFit), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"),/*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
      ++nFits;
      if ( r->status()==0 )
	break;
    }
    chi2 = 0.0;
    nEmptyBins = 0;
    if ((*mmumuFit).numEntries() > 0) {
      powerlaw.plotOn(frame,Name("background_powerlaw"),Range("fitRange"),RooFit::NormRange("fitRange"));

    //////Construct histograms with residuals and pulls of the data w.r.t. the curve
      hresid = frame->residHist();
      hpull = frame->pullHist();
      fitcurve = frame->getCurve("background_powerlaw");
      //////Determine range of curve 
      fitcurve->GetPoint(0,xstart,y);
      fitcurve->GetPoint(fitcurve->GetN()-1,xstop,y);
      nPoints = hresid->GetN();
      cout << nPoints << endl;
      for (int i = 0; i < nPoints; i++) {
        double b, point;
        hpull->GetPoint(i,b,point);
        if (b<xstart || b>xstop) continue;
        if (point==0) {
	  ++nEmptyBins;
        }
        else {
          hresid->GetPoint(i,b,point);
  	  chi2 += point*point / (fitcurve->interpolate(b));
        }
      }
    }
    //////Access fit result information
    //r->Print();
    //////Access basic information
    cout << "Status = " << r->status() << endl;
    cout << "EDM = " << r->edm() << endl;
    cout << "-log(L) at minimum = " << r->minNll() << endl;
    //////Access list of final fit parameter values
    cout << "Final value of floating parameters:" << endl;
    r->floatParsFinal().Print("s");
    //////Evaluate chi-square:
    cout << "chiSquare = " << frame->chiSquare(nFitParams) << endl;
    cout << "chiSquare (from residual histogram) / NDOF = " << chi2 << " / " << std::max(nFitParams,nPoints-nEmptyBins-nFitParams) << endl;
    cout << "p-value (chiSquare, NDOF) = " << ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams))) << endl;

    if ( saveFitResult ) {
      //////Save RooFitResult into a ROOT file
      TFile ffitresult(Form("%s/%s_fitResult_powerlaw_mass%.0f.root",outDir,(*mmumuFit).GetName(),mass),"RECREATE");
      r->Write("fitResult");
      ffitresult.Close();
    }

    //////Select PDFs
    //////Chi2-based p-value
    int fitStatusPowerlaw = r->status();
    double chi2PowerlawPvalue = ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams)));

    frame->remove("background_powerlaw");

    // If p-value is zero, fit does not converge, zero events, or less than 1 events and less than 0.1 events/GeV, do not include
    if ( chi2PowerlawPvalue > 0.01 &&
	 fitStatusPowerlaw==0 && 
	 !( nBG.getVal() < 1 || ( nBG.getVal()/(mass+5.0*stddev_window-std::max(minMforFit,mass-5.0*stddev_window)) < 1e-1 && nBG.getVal() < 10 ) ) ) {
      bgPDFs.add(powerlaw);
      if ( useOnlyPowerLaw )
	wfit.import(powerlaw);

      powerlaw.plotOn(frame,Name("background_powerlaw"),Range("fitRange"),RooFit::NormRange("fitRange"),LineColor(kRed));
      if ( drawFits ) {
	//////Draw fit
	TCanvas *can = new TCanvas("can","",600,600);
	can->cd();
	frame->SetMinimum(0.0);
	frame->SetLabelSize(0.02,"Y");
	frame->SetTitleSize(0.025,"Y");
	frame->SetXTitle("Dimuon mass [GeV]");
	frame->Draw();
	//can->SaveAs(Form("%s/%s_fitBackground_powerlaw_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->SaveAs(Form("%s/%s_fitBackground_powerlaw_mass%.0f.png",outDir,mmumuAll.GetName(),mass));
	can->Update();
	can->Clear();
	can->Close();
      }
      if ( drawResidual ) {
	//Create a dedicated frame to draw the residual distribution and add the distribution to the frame
	RooHist *hresid = frame->residHist();
	RooPlot *frameres = x.frame(Title("Residual Distribution"));
	frameres->addPlotable(hresid, "P");
	frameres->SetXTitle("Dimuon mass [GeV]");
	TCanvas *can = new TCanvas("can","",600,600);
	can->cd();
	frameres->Draw();
	can->SaveAs(Form("%s/%s_fitResidual_powerlaw_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->Update();
	can->Clear();
	
	//Create a dedicated frame to draw the pull distribution and add the distribution to the frame
	RooHist *hpull = frame->pullHist();
	RooPlot *framepull = x.frame(Title("Pull Distribution"));
	framepull->addPlotable(hpull, "P");
	framepull->SetXTitle("Dimuon mass [GeV]");
	can->cd();
	framepull->Draw();
	can->SaveAs(Form("%s/%s_fitPull_powerlaw_mass%.0f.png",outDir,(*mmumuFit).GetName(),mass));
	can->Update();
	can->Clear();
	can->Close();
      }
      frame->remove("background_powerlaw");
    }

    //////Bernstein polynomials
    std::cout << "Bernstein fit................." << std::endl;
    int maxpolyorder = 5; // up to 5
    //if (nBG.getVal() < 1)
    //    maxpolyorder = 0;
    int bestBernsteinOrder = -1;
    double lastnll = 0.0;
    vector<RooArgList> parListBernstein;
    RooArgList bgBernsteinPDFs;
    vector<double> chi2BernsteinPvalue;
    vector<RooFitResult> fitResultBernstein;
    vector<int> fitStatusBernstein;
    for (int to=0; to<maxpolyorder+1; to++) { 
      RooArgList parList(Form("bernstein_order%d%s",to+1,catExt.Data()));
      RooRealVar par0(Form("pbern0_order%d%s",to+1,catExt.Data()),Form("pbern0_order%d%s",to+1,catExt.Data()),0.0,10.0);
      RooRealVar par1(Form("pbern1_order%d%s",to+1,catExt.Data()),Form("pbern1_order%d%s",to+1,catExt.Data()),0.0,10.0);
      RooRealVar par2(Form("pbern2_order%d%s",to+1,catExt.Data()),Form("pbern2_order%d%s",to+1,catExt.Data()),0.0,10.0);
      RooRealVar par3(Form("pbern3_order%d%s",to+1,catExt.Data()),Form("pbern3_order%d%s",to+1,catExt.Data()),0.0,10.0);
      RooRealVar par4(Form("pbern4_order%d%s",to+1,catExt.Data()),Form("pbern4_order%d%s",to+1,catExt.Data()),0.0,10.0);
      RooRealVar par5(Form("pbern5_order%d%s",to+1,catExt.Data()),Form("pbern5_order%d%s",to+1,catExt.Data()),0.0,10.0);
      RooAbsPdf *background;
      if ( to<=0 ) {
	parList.add(par0);
	background = new RooBernsteinFast<1>(Form("background_bernstein_order%d%s",to+1,catExt.Data()),Form("background_bernstein_order%d%s",to+1,catExt.Data()),x,parList);
      }
      else if ( to<=1 ) {
	parList.add(par0);
	parList.add(par1);
	background = new RooBernsteinFast<2>(Form("background_bernstein_order%d%s",to+1,catExt.Data()),Form("background_bernstein_order%d%s",to+1,catExt.Data()),x,parList);
      }
      else if ( to<=2 ) {
	parList.add(par0);
	parList.add(par1);
	parList.add(par2);
	background = new RooBernsteinFast<3>(Form("background_bernstein_order%d%s",to+1,catExt.Data()),Form("background_bernstein_order%d%s",to+1,catExt.Data()),x,parList);
      }
      else if ( to<=3 ) {
	parList.add(par0);
	parList.add(par1);
	parList.add(par2);
	parList.add(par3);
	background = new RooBernsteinFast<4>(Form("background_bernstein_order%d%s",to+1,catExt.Data()),Form("background_bernstein_order%d%s",to+1,catExt.Data()),x,parList);
      }
      else if ( to<=4 ) {
	parList.add(par0);
	parList.add(par1);
	parList.add(par2);
	parList.add(par3);
	parList.add(par4);
	background = new RooBernsteinFast<5>(Form("background_bernstein_order%d%s",to+1,catExt.Data()),Form("background_bernstein_order%d%s",to+1,catExt.Data()),x,parList);
      }
      else if ( to<=5 ) {
	parList.add(par0);
	parList.add(par1);
	parList.add(par2);
	parList.add(par3);
	parList.add(par4);
	parList.add(par5);
	background = new RooBernsteinFast<6>(Form("background_bernstein_order%d%s",to+1,catExt.Data()),Form("background_bernstein_order%d%s",to+1,catExt.Data()),x,parList);
      }
      else { 
	cout << "Bernsteain polynomials are only defined for order [0,6]; exiting." << endl;
	return;
      }
      //////Fit
      nFitParams = to+1;
      nFits = 0;
      while ( nFits < nMaxFitAttempts ) {
	r = background->fitTo((*mmumuFit), Range("fitRange"), Save(), Minimizer("Minuit2","Migrad"),/*SumW2Error(kTRUE), */PrintLevel(-1), PrintEvalErrors(-1));
	++nFits;
	if ( r->status()==0 )
	  break;
      }
      parListBernstein.push_back(*((RooArgSet*) parList.snapshot(kTRUE)));
      //if ( r->status()!=0 ) continue;
      chi2 = 0.0;
      nEmptyBins = 0;
      int nPoints = 0;
      if (false) {
        background->plotOn(frame,Name(Form("background_bernstein_order%d",to+1)),Range("fitRange"),RooFit::NormRange("fitRange"));

        //////Construct histograms with residuals and pulls of the data w.r.t. the curve
        RooHist *hresid = frame->residHist();
        RooHist *hpull = frame->pullHist();
        RooCurve *fitcurve = frame->getCurve(Form("background_bernstein_order%d",to+1));
        //////Determine range of curve 
        Double_t xstart,xstop,y;
        fitcurve->GetPoint(0,xstart,y);
        fitcurve->GetPoint(fitcurve->GetN()-1,xstop,y);
        nPoints = hresid->GetN();
        cout << nPoints << endl;
        for (int i = 0; i < nPoints; i++) {
  	  double b, point;
	  hpull->GetPoint(i,b,point);
	  if (b<xstart || b>xstop) continue;
	  if (point==0) {
	    ++nEmptyBins;
	  }
	  else {
	    hresid->GetPoint(i,b,point);
	    chi2 += point*point / (fitcurve->interpolate(b));
	  }
        }
      }
      //////Access fit result information
      //r->Print();
      //////Access basic information
      cout << "Status = " << r->status() << endl;
      cout << "EDM = " << r->edm() << endl;
      cout << "-log(L) at minimum = " << r->minNll() << endl;
      //////Access list of final fit parameter values
      cout << "Final value of floating parameters:" << endl;
      r->floatParsFinal().Print("s");
      //////Evaluate chi-square:
      cout << "chiSquare = " << frame->chiSquare(nFitParams) << endl;
      cout << "chiSquare (from residual histogram) / NDOF = " << chi2 << " / " << std::max(nFitParams,nPoints-nEmptyBins-nFitParams) << endl;
      cout << "p-value (chiSquare, NDOF) = " << ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams))) << endl;
      if ( saveFitResult ) {
	//////Save RooFitResult into a ROOT file
	TFile ffitresult(Form("%s/%s_fitResult_bernstein_order%d_mass%.0f.root",outDir,(*mmumuFit).GetName(),to+1,mass),"RECREATE");
	r->Write("fitResult");
	ffitresult.Close();
      }

      //////Select PDFs
      //////Chi2-based p-value
      fitResultBernstein.push_back(*r);
      fitStatusBernstein.push_back(r->status());
      chi2BernsteinPvalue.push_back(ROOT::Math::chisquared_cdf_c(chi2, (double)(std::max(nFitParams,nPoints-nEmptyBins-nFitParams))));
      //////Fisher test
      double thisnll = r->minNll();
      cout << thisnll << " " << lastnll << endl;
      double ftestChi2 = 2*(lastnll-thisnll);
      cout << endl << "Order= " << to+1 << "; ftestChi2=" << ftestChi2 << " p=" << TMath::Prob(ftestChi2,1) << endl;
      lastnll = thisnll;
      cout << thisnll << " " << lastnll << endl;
      if ( ftestChi2 < 0.0 ) ftestChi2 = 0.0;
      if ( (bestBernsteinOrder < 0 && fitStatusBernstein[to-1]==0 && TMath::Prob(ftestChi2,1) > 0.05 && to-1 >= 0) || to>maxpolyorder ) 
	bestBernsteinOrder = to-1;
      // If zero events, or less than 10 events and less than 0.1 events/GeV, only use lowest order
      if ( nBG.getVal() < 1 || ( nBG.getVal()/(mass+5.0*stddev_window-std::max(minMforFit,mass-5.0*stddev_window)) < 1e-1 && nBG.getVal() < 1e1 ) ) {
	   bestBernsteinOrder=0;
      }

      //frame->remove(Form("background_bernstein_order%d",to+1));
      if ( (bestBernsteinOrder >= 0 && to > bestBernsteinOrder) || to > maxpolyorder ) {
	RooAbsPdf *bernstein = nullptr;
	bool isUniform = false;
	vector<int> bernsteinPDFOrders;
	int minBernsteinOrder = (addBernsteinOrders) ? bestBernsteinOrder-1 : bestBernsteinOrder;
	int maxBernsteinOrder = (addBernsteinOrders) ? bestBernsteinOrder+1 : bestBernsteinOrder;
	for ( int tto = minBernsteinOrder; tto <= maxBernsteinOrder; tto++) {
          if (nBG.getVal() < 1 && tto==minBernsteinOrder) {
            bernstein = new RooUniform(Form("background_uniform%s",catExt.Data()),Form("background_uniform%s",catExt.Data()),x);
	    isUniform = true;
          } else {
            if (nBG.getVal() < 1)
              continue;
	  if ( tto < 0 ) continue;
	  // If zero events, or less than 10 events and less than 0.1 events/GeV, only use lowest order
	  if ( (nBG.getVal() < 1 || ( nBG.getVal()/(mass+5.0*stddev_window-std::max(minMforFit,mass-5.0*stddev_window)) < 1e-1 && nBG.getVal() < 1e1 ) ) && tto > 0 ) continue;
	  // If p-value is zero, fit does not converge, zero events, or less than 10 events and less than 0.1 events/GeV, do not include
	  if ( ( chi2BernsteinPvalue[tto] > 0.01 &&
		 fitStatusBernstein[tto]==0 )
	       || ( nBG.getVal() < 1 || ( nBG.getVal()/(mass+5.0*stddev_window-std::max(minMforFit,mass-5.0*stddev_window)) < 1e-1 && nBG.getVal() < 1e1 ) ) ) {
	    bernsteinPDFOrders.push_back(tto);
	    //RooAbsPdf *bernstein;
	    if (tto == 0) {
	      //if ( (*mmumuFit).sumEntries(Form("%s>=%.3f",varname.Data(),mass+3.0*stddev_window)) < (*mmumuFit).sumEntries(Form("%s<%.3f",varname.Data(),mass-3.0*stddev_window)) ) {
		bernstein = new RooBernsteinFast<1>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);
	      //} else {
	      //bernstein = new RooUniform(Form("background_uniform%s",catExt.Data()),Form("background_uniform%s",catExt.Data()),x);
	      //isUniform = true;
              //}
	    }
	    else if (tto == 1)
	      bernstein = new RooBernsteinFast<2>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);
	    else if (tto == 2)
	      bernstein = new RooBernsteinFast<3>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);
	    else if (tto == 3)
	      bernstein = new RooBernsteinFast<4>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);
	    else if (tto == 4)
	      bernstein = new RooBernsteinFast<5>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);
	    else if (tto == 5)
	      bernstein = new RooBernsteinFast<6>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);
	    else // dummy although it shouldn't be used
	      bernstein = new RooBernsteinFast<6>(Form("background_bernstein%s",catExt.Data()),Form("background_bernstein%s",catExt.Data()),x,parListBernstein[tto]);

	    if (tto == bestBernsteinOrder) {
	      bernstein->plotOn(frame,Name(Form("background_bernstein_order%d",tto+1)),Range("fitRange"),RooFit::NormRange("fitRange"),LineColor(kRed));
	    }
	    else {
	      bernstein->plotOn(frame,Name(Form("background_bernstein_order%d",tto+1)),Range("fitRange"),RooFit::NormRange("fitRange"),LineColor(kOrange));
	   
            }

	    if ( drawFits ) {
	      //////Draw fit
	      TCanvas *can = new TCanvas("can","",600,600);
	      can->cd();
	      frame->SetMinimum(0.0);
	      frame->SetLabelSize(0.02,"Y");
	      frame->SetTitleSize(0.025,"Y");
	      frame->SetXTitle("Dimuon mass [GeV]");
	      frame->Draw();
	      //can->SaveAs(Form("%s/%s_fitBackground_bernstein_order%d_mass%.0f.png",outDir,(*mmumuFit).GetName(),tto+1,mass));
	      can->SaveAs(Form("%s/%s_fitBackground_bernstein_order%d_mass%.0f.png",outDir,mmumuAll.GetName(),tto+1,mass));
	      can->Update();
	      can->Clear();
	      can->Close();
	    }

	    if ( drawResidual ) {
	      //Create a dedicated frame to draw the residual distribution and add the distribution to the frame
	      RooHist *hresid = frame->residHist();
	      RooPlot *frameres = x.frame(Title("Residual Distribution"));
	      frameres->addPlotable(hresid, "P");
	      frameres->SetXTitle("Dimuon mass [GeV]");
	      TCanvas *can = new TCanvas("can","",600,600);
	      can->cd();
	      frameres->Draw();
	      can->SaveAs(Form("%s/%s_fitResidual_bernstein_order%d_mass%.0f.png",outDir,(*mmumuFit).GetName(),tto+1,mass));
	      can->Update();
	      can->Clear();

	      //Create a dedicated frame to draw the pull distribution and add the distribution to the frame
	      RooHist *hpull = frame->pullHist();
	      RooPlot *framepull = x.frame(Title("Pull Distribution"));
	      framepull->addPlotable(hpull, "P");
	      framepull->SetXTitle("Dimuon mass [GeV]");
	      can->cd();
	      framepull->Draw();
	      can->SaveAs(Form("%s/%s_fitPull_bernstein_order%d_mass%.0f.png",outDir,(*mmumuFit).GetName(),tto+1,mass));
	      can->Update();
	      can->Clear();
	      can->Close();
	    }
	    frame->remove(Form("background_bernstein_order%d",tto+1));
            }
	    }
	    if (bernstein) {
	      if (!isUniform || bgPDFs.getSize()<1)
	        bgPDFs.add(*bernstein);
	      if ( useOnlyBernstein )
	        wfit.import(*bernstein);
	    }
	}
	break;
      }
    }

    //////Power-law PDF
    /*
    std::cout << "Uniform................." << std::endl;
    RooGenericPdf uniform(Form("background_uniform0%s",catExt.Data()),"@0*0.001",RooArgList(x));
    wfit.import(uniform);
    bgPDFs.add(uniform);
    */

    RooCategory *cat = new RooCategory(Form("pdf_index%s",catExt.Data()),Form("pdf_index%s",catExt.Data()));
    RooMultiPdf multipdf(Form("roomultipdf%s",catExt.Data()),Form("roomultipdf%s",catExt.Data()),*cat,bgPDFs);
    //wfit.import(*cat);
    if ( !(doNotUseMultiPDF) ) {
      wfit.import(multipdf);
      wfit.import(nBG);
    }
    else {
      if ( useOnlyExponential )
	wfit.import(nBG_exp);
      if ( useOnlyPowerLaw )
	wfit.import(nBG_pow);
      if ( useOnlyBernstein )
	wfit.import(nBG_pol);
    }
  }
}
