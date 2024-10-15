{
  gROOT->ProcessLine(".L ./cpp/fit_dimuon.C+");  // Macro that performs the fits
  gROOT->ProcessLine(".L ./cpp/tools/param.C+");  // Macro that handles the spline

  bool useData = true;
  bool useSignalMC = true;
  bool mergeEras = true;
  bool writeWS = false;
  bool mergeLifetimes = true;
  TString model = "HTo2ZdTo2mu2x";
  
  // Dir with the RooDataSets
  //TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Apr-03-2024_onlySignal";
  //TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Mar-26-2024_allCuts";
  //TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_SRsOnly_2022";
  TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jul-10-2024_2022_allCuts_full";

  // Names of the search regions we want to parametrize
  vector<TString> dNames = { };
  //dNames.push_back("d_Dimuon_full_inclusive");
  dNames.push_back("d_FourMu_sep");
  dNames.push_back("d_Dimuon_lxy0p0to0p2_inclusive");
  dNames.push_back("d_Dimuon_lxy0p2to1p0_inclusive");
  dNames.push_back("d_Dimuon_lxy1p0to2p4_inclusive");
  dNames.push_back("d_Dimuon_lxy2p4to3p1_inclusive");
  dNames.push_back("d_Dimuon_lxy3p1to7p0_inclusive");
  dNames.push_back("d_Dimuon_lxy7p0to11p0_inclusive");
  dNames.push_back("d_Dimuon_lxy11p0to16p0_inclusive");
  dNames.push_back("d_Dimuon_lxy16p0to70p0_inclusive");

  // Eras (to be uncommented when adding 2023 and splitting in eras)
  vector<TString> eras;
  eras.push_back("2022");
  eras.push_back("2022postEE");
  //eras.push_back("2023"); // Currently not available
  //eras.push_back("2023BPix"); // Currently not available

  TString sigTemplate;
  //vector<TString> sigsamples = { };


  // Signals (To be modified: Needs to be more general but this is provisional)
  vector<float> sigMass;
  vector<float> sigCtau;
  vector<float> selectedPoint;
  if ( model=="HTo2ZdTo2mu2x" ) {
    sigMass = {0.5, 0.7, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0};
    sigCtau = {1, 10, 100, 1000};
    sigTemplate = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm";
    for (unsigned int t=0; t<sigCtau.size(); t++) {
      for (unsigned int m=0; m<sigMass.size(); m++) {
        if ( (sigMass[m] < 1.0 && sigCtau[t] > 10) || (sigMass[m] < 30.0 && sigCtau[t] > 100))
           selectedPoint.push_back(false);
        else
           selectedPoint.push_back(true);
      }
    }
  }

  // Loop over signals 
  for ( unsigned int d=0; d<dNames.size(); d++ ) {
    vector<vector<RooDataSet>> mmumu_sigs {{}};
    TString outfile = Form("utils/signalFitParameters_%s.root", dNames[d].Data());
    std::cout << outfile << std::endl;
    TFile *finit = new TFile(outfile.Data(), "RECREATE");
    finit->Close();
    for ( unsigned int iera=0; iera<eras.size(); iera++ ) {
      TString era = eras[iera];
      TString year = "2022"; // hardcoded
      if (mergeLifetimes) {
        for (unsigned int m=0; m<sigMass.size(); m++) {
          if (iera == 0) {
            vector<RooDataSet> tds_aux{};
            mmumu_sigs.push_back( tds_aux );
          }
          TString massString = Form("%.1f",sigMass[m]);
          massString.ReplaceAll(".", "p");
          std::cout << "For mass: " <<  massString << std::endl;
          for (unsigned int t=0; t<sigCtau.size(); t++) {
            unsigned int isample = t*sigMass.size() + m;
            if (!selectedPoint[isample])
              continue;
            TString ctauString = Form("%.0f",sigCtau[t]);
            std::cout << "For ctau: " << ctauString << std::endl;
            TString sample = Form(sigTemplate.Data(), massString.Data(),ctauString.Data());
            TString inFile = Form("%s/histograms_%s_%s_%s_0.root",inDir.Data(),sample.Data(),era.Data(),year.Data());
            TFile fin(inFile);
            if (t==0) {
              RooDataSet *tds = (RooDataSet*) fin.Get(dNames[d])->Clone();
              std::cout << tds->numEntries() << std::endl;
              tds->SetName(dNames[d]+"_"+sample.Data()+"_"+year+"_"+era);
              mmumu_sigs[m].push_back( *tds );
            } else {
              RooDataSet *tds_t = (RooDataSet*) fin.Get(dNames[d])->Clone();
              mmumu_sigs[m][iera].append( *tds_t );
            }
            fin.Close();
            cout << mmumu_sigs[m][iera].numEntries() << endl;
          }
        } 
      } else {
        for (unsigned int t=0; t<sigCtau.size(); t++) {
          for (unsigned int m=0; m<sigMass.size(); m++) {
            unsigned int isample = t*sigMass.size() + m;
            if (iera == 0) {
              vector<RooDataSet> tds_aux{};
              mmumu_sigs.push_back( tds_aux );
            }
            if (!selectedPoint[isample])
              continue;
            TString massString = Form("%.1f",sigMass[m]);
            massString.ReplaceAll(".", "p");
            TString ctauString = Form("%.0f",sigCtau[t]);
            TString sample = Form(sigTemplate.Data(), massString.Data(),ctauString.Data());
            TString inFile = Form("%s/histograms_%s_%s_%s_0.root",inDir.Data(),sample.Data(),era.Data(),year.Data());
            TFile fin(inFile);
            RooDataSet *tds = (RooDataSet*) fin.Get(dNames[d])->Clone();
            tds->SetName(dNames[d]+"_"+sample.Data()+"_"+year+"_"+era);
            mmumu_sigs[isample].push_back( *tds );
            std::cout << "For isample: " <<  isample << std::endl;
            std::cout << "Reading signal file: " <<  inFile << ", with dataset with entries: " << tds->sumEntries() << std::endl;
            fin.Close();
            cout << mmumu_sigs[isample][iera].numEntries() << endl;
          }
	} 
      } // end mergeLifetimes
    }

   if (mergeEras) {

     TString outDir = "paramResults_allEras";
     vector<TSpline3> splineList;
     vector<TGraph> graphList;
     vector<RooDataSet> mmumu_sig_merged = {};

     if (mergeLifetimes) {

       TString ctau_label = "allctaus";
       TGraph *gsigma = new TGraph();
       TGraph *gnL = new TGraph();
       TGraph *gnR = new TGraph();
       TGraph *gaL = new TGraph();
       TGraph *gaR = new TGraph();
       TGraph *gmean = new TGraph();
       TGraph *gmcfrac = new TGraph();
       gsigma->SetName("gsigma_"+dNames[d]);
       gnL->SetName("gnL_"+dNames[d]);
       gnR->SetName("gnR_"+dNames[d]);
       gaL->SetName("gaL_"+dNames[d]);
       gaR->SetName("gaR_"+dNames[d]);
       gmean->SetName("gmean_"+dNames[d]);
       gmean->SetName("gmcfrac_"+dNames[d]);

       for (unsigned int m=0; m<sigMass.size(); m++) {

         // Create worksapce, import data and model
         std::cout << "Creating container workspace" << std::endl;
         RooWorkspace wfit("wfit","workspace"); 
         int idx = 0;
         for (unsigned int iera=0; iera<eras.size(); iera++ ) {
           if (iera==0) {
             mmumu_sig_merged.push_back(mmumu_sigs[m][iera]);
           } else {
             idx = mmumu_sig_merged.size() - 1;
             mmumu_sig_merged[idx].append(mmumu_sigs[m][iera]);
           }
           cout << iera << " ...filling...  "<< mmumu_sigs[m][iera].GetName() << endl;
         }  

         TString massString = Form("%.1f",sigMass[m]);
         TString sample = Form(sigTemplate.Data(), massString.Data(),ctau_label.Data());
         mmumu_sig_merged[idx].SetName(dNames[d]+"_"+sample.Data()+"_allEras");
         cout << "Merged dataset for signal " << sample.Data() << " with entries " << mmumu_sig_merged[idx].sumEntries() << endl;
         // Fit invariant mass
         std::cout << "Prepare to fit..." << std::endl;
         if (dNames[d].BeginsWith("d_FourMu_")) {
           fitmass(mmumu_sig_merged[idx], "Signal", false, true, true, sample , sigMass[m], 125., wfit, true, "allEras", "dcbfastg", outDir);
         } else {
           fitmass(mmumu_sig_merged[idx], "Signal", false, true, true, sample, sigMass[m], sigMass[m], wfit, false, "allEras", "dcbfastg", outDir);
         }

         // Print workspace contents
         std::cout << "Temporal workspace contents: " << std::endl;
         wfit.Print();

         // Get the values
         RooRealVar *sigma;
         RooRealVar *nL;
         RooRealVar *nR;
         RooRealVar *aL;
         RooRealVar *aR;
         RooRealVar *mean;
         RooRealVar *mcfrac;
         if (dNames[d].BeginsWith("d_FourMu_")) {
           sigma = wfit.var("sigma_ch1_allEras");
           nL = wfit.var("nL_ch1_allEras");
           nR = wfit.var("nR_ch1_allEras");
           aL = wfit.var("alphaL_ch1_allEras");
           aR = wfit.var("alphaR_ch1_allEras");
           mean = wfit.var("mean_ch1_allEras");
           mcfrac = wfit.var("mcfrac_ch1_allEras");
         } else {
           sigma = wfit.var("sigma_ch-1_allEras");
           nL = wfit.var("nL_ch-1_allEras");
           nR = wfit.var("nR_ch-1_allEras");
           aL = wfit.var("alphaL_ch-1_allEras");
           aR = wfit.var("alphaR_ch-1_allEras");
           mean = wfit.var("mean_ch-1_allEras");
           mcfrac = wfit.var("mcfrac_ch-1_allEras");
         }
	 
         // Fill graphs
         gsigma->AddPoint(sigMass[m], sigma->getVal());
         gnL->AddPoint(sigMass[m], nL->getVal());
         gnR->AddPoint(sigMass[m], nR->getVal());
         gaL->AddPoint(sigMass[m], aL->getVal());
         gaR->AddPoint(sigMass[m], aR->getVal());
         gmean->AddPoint(sigMass[m], mean->getVal());
         gmcfrac->AddPoint(sigMass[m], mcfrac->getVal());
       }

       // Create the Tspline's for the parameters
       std::cout << gsigma->GetN() << std::endl;
       TSpline3 *splines = new TSpline3("splines",gsigma->GetX(), gsigma->GetY(), gsigma->GetN(), "b2e2", 0, 0); 
       splines->SetName(Form("splines_%s", dNames[d].Data()));
       TSpline3 *splinenL = new TSpline3("splinenL",gnL->GetX(), gnL->GetY(), gnL->GetN(), "b2e2", 0, 0); 
       splinenL->SetName(Form("splinenL_%s", dNames[d].Data()));
       TSpline3 *splinenR = new TSpline3("splinenR",gnR->GetX(), gnR->GetY(), gnR->GetN(), "b2e2", 0, 0); 
       splinenR->SetName(Form("splinenR_%s", dNames[d].Data()));
       TSpline3 *splineaL = new TSpline3("splineaL",gaL->GetX(), gaL->GetY(), gaL->GetN(), "b2e2", 0, 0); 
       splineaL->SetName(Form("splineaL_%s", dNames[d].Data()));
       TSpline3 *splineaR = new TSpline3("splineaR",gaR->GetX(), gaR->GetY(), gaR->GetN(), "b2e2", 0, 0); 
       splineaR->SetName(Form("splineaR_%s", dNames[d].Data()));
       TSpline3 *splinem = new TSpline3("splinem", gmean->GetX(), gmean->GetY(), gmean->GetN(), "b2e2", 0, 0); 
       splinem->SetName(Form("splinem_%s", dNames[d].Data()));
       TSpline3 *splinef = new TSpline3("splinef", gmcfrac->GetX(), gmcfrac->GetY(), gmcfrac->GetN(), "b2e2", 0, 0); 
       splinef->SetName(Form("splinef_%s", dNames[d].Data()));
       std::cout << "Finished building the splines" << std::endl;

       // Write splines
       TFile *fs = new TFile(outfile.Data(), "UPDATE");
       fs->cd();
       splines->Write();
       splinem->Write();
       splinenL->Write();
       splinenR->Write();
       splineaL->Write();
       splineaR->Write();
       splinef->Write();
       gsigma->Write();
       gmean->Write();
       gnL->Write();
       gnR->Write();
       gaL->Write();
       gaR->Write();
       gmcfrac->Write();
       fs->Close();
       std::cout << "Finished saving the splines" << std::endl;

       //for ( int isample=0; isample<sigMass.size()+sigCtau.size(); isample++ ) {
       //  mmumu_sigs[isample].clear();
       //} 
       //mmumu_sigs.clear();

     } else {
       for (unsigned int t=0; t<sigCtau.size(); t++) {

         // Graphs
         TGraph *gsigma = new TGraph();
         TGraph *gnL = new TGraph();
         TGraph *gnR = new TGraph();
         TGraph *gaL = new TGraph();
         TGraph *gaR = new TGraph();
         TGraph *gmean = new TGraph();

         TString ctauString = Form("%.0f",sigCtau[t]);
         gsigma->SetName(Form("gsigma_%smm",ctauString.Data()));
         gnL->SetName(Form("gnL_%smm",ctauString.Data()));
         gnR->SetName(Form("gnR_%smm",ctauString.Data()));
         gaL->SetName(Form("gaL_%smm",ctauString.Data()));
         gaR->SetName(Form("gaR_%smm",ctauString.Data()));
         gmean->SetName(Form("gmean_%smm",ctauString.Data()));

         for (unsigned int m=0; m<sigMass.size(); m++) {

           unsigned int isample = t*sigMass.size() + m;
           TString massString = Form("%.1f",sigMass[m]);
           TString sample = Form(sigTemplate.Data(), massString.Data(),ctauString.Data());
           if (!selectedPoint[isample])
             continue;
           // Create worksapce, import data and model
           std::cout << "Creating container workspace" << std::endl;
           RooWorkspace wfit("wfit","workspace"); 
           int idx = 0;
           for (unsigned int iera=0; iera<eras.size(); iera++ ) {
             if (iera==0) {
               mmumu_sig_merged.push_back(mmumu_sigs[isample][iera]);
             } else {
               idx = mmumu_sig_merged.size() - 1;
               mmumu_sig_merged[idx].append(mmumu_sigs[isample][iera]);
             }
             cout << iera << " ...filling...  "<< mmumu_sigs[isample][iera].GetName() << endl;
           }  
           mmumu_sig_merged[idx].SetName(dNames[d]+"_"+sample+"_allEras");
           cout << "Merged dataset for signal " << sample << " with entries " << mmumu_sig_merged[idx].sumEntries() << endl;
           // Fit invariant mass
           std::cout << "Prepare to fit..." << std::endl;
           if (dNames[d].BeginsWith("d_FourMu_")) {
             fitmass(mmumu_sig_merged[idx], "Signal", false, true, true, sample , 125., wfit, true, "2022", "dcbfastg", outDir);
           } else {
             fitmass(mmumu_sig_merged[idx], "Signal", false, true, true, sample, sigMass[m], wfit, false, "2022", "dcbfastg", outDir);
           }
    
           // Print workspace contents
           std::cout << "Temporal workspace contents: " << std::endl;
           wfit.Print();

           // Get the values
           RooRealVar *sigma = wfit.var("sigma_ch-1_allEras");
           RooRealVar *nL = wfit.var("nL_ch-1_allEras");
           RooRealVar *nR = wfit.var("nR_ch-1_allEras");
           RooRealVar *aL = wfit.var("alphaL_ch-1_allEras");
           RooRealVar *aR = wfit.var("alphaR_ch-1_allEras");
           RooRealVar *mean = wfit.var("mean_ch-1_allEras");

           // Fill graphs
           gsigma->AddPoint(sigMass[m], sigma->getVal());
           gnL->AddPoint(sigMass[m], nL->getVal());
           gnR->AddPoint(sigMass[m], nR->getVal());
           gaL->AddPoint(sigMass[m], aL->getVal());
           gaR->AddPoint(sigMass[m], aR->getVal());
           gmean->AddPoint(sigMass[m], mean->getVal());

         }

         // Create the Tspline's for the parameters
         TSpline3 *splines = new TSpline3("splines",gsigma->GetX(), gsigma->GetY(), gsigma->GetN(), "b2e2", 0, 0); 
         splines->SetName(Form("splines_%smm", ctauString.Data()));
         TSpline3 *splinenL = new TSpline3("splinenL",gnL->GetX(), gnL->GetY(), gnL->GetN(), "b2e2", 0, 0); 
         splinenL->SetName(Form("splinenL_%smm", ctauString.Data()));
         TSpline3 *splinenR = new TSpline3("splinenR",gnR->GetX(), gnR->GetY(), gnR->GetN(), "b2e2", 0, 0); 
         splinenR->SetName(Form("splinenR_%smm", ctauString.Data()));
         TSpline3 *splineaL = new TSpline3("splineaL",gaL->GetX(), gaL->GetY(), gaL->GetN(), "b2e2", 0, 0); 
         splineaL->SetName(Form("splineaL_%smm", ctauString.Data()));
         TSpline3 *splineaR = new TSpline3("splineaR",gaR->GetX(), gaR->GetY(), gaR->GetN(), "b2e2", 0, 0); 
         splineaR->SetName(Form("splineaR_%smm", ctauString.Data()));
         TSpline3 *splinem = new TSpline3("splinem", gmean->GetX(), gmean->GetY(), gmean->GetN(), "b2e2", 0, 0); 
         splinem->SetName(Form("splinem_%smm", ctauString.Data()));

          // Write splines
          TFile *fs = new TFile("utils/signalFitParameters.root", "UPDATE");
          fs->cd();
          splines->Write();
          splinem->Write();
          splinenL->Write();
          splinenR->Write();
          splineaL->Write();
          splineaR->Write();
          gsigma->Write();
          gmean->Write();
          gnL->Write();
          gnR->Write();
          gaL->Write();
          gaR->Write();
          fs->Close();

       }
       for ( int isample=0; isample<sigMass.size()+sigCtau.size(); isample++ ) {
         mmumu_sigs[isample].clear();
       } 
       mmumu_sigs.clear();
     } // end mergeLifetimes
   }

   
 }

}
