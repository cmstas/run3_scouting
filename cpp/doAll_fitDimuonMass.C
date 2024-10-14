{
  gROOT->ProcessLine(".L ./cpp/fit_dimuon.C+");  // Macro that performs the fitting
  gROOT->ProcessLine(".L ./cpp/helper.C+");  // Helper with handles 

  bool useData = true;
  bool useSignalMC = false;
  bool mergeEras = true;
  bool writeWS = true;
  bool doUpAndDownVariations = true;
  if (!useSignalMC)
    doUpAndDownVariations = false;
  TString period = "2022"; // Either 2022 or 2023
  TString model = "HTo2ZdTo2mu2x";
  //TString model = "ScenarioB1";
  

  // Dir with the RooDataSets
  //TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jul-02-2024_2022_SRsOnly"; // last 2022
  //TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_SRsOnly_2023"; // last 2023
  TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Sep-25-2024_RooDatasets_unblind"; // last 2022 (unblinded)

  // Names of the search regions
  vector<TString> dNames = { };
  dNames.push_back("d_FourMu_sep");
  dNames.push_back("d_FourMu_osv");
  dNames.push_back("d_Dimuon_lxy0p0to0p2_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy0p0to0p2_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy0p0to0p2_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy0p0to0p2_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy0p2to1p0_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy0p2to1p0_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy0p2to1p0_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy0p2to1p0_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy1p0to2p4_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy1p0to2p4_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy1p0to2p4_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy1p0to2p4_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy2p4to3p1_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy2p4to3p1_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy2p4to3p1_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy2p4to3p1_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy3p1to7p0_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy3p1to7p0_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy3p1to7p0_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy3p1to7p0_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy7p0to11p0_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy7p0to11p0_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy7p0to11p0_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy7p0to11p0_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy11p0to16p0_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy11p0to16p0_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy11p0to16p0_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy11p0to16p0_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy16p0to70p0_iso0_ptlow");
  dNames.push_back("d_Dimuon_lxy16p0to70p0_iso0_pthigh");
  dNames.push_back("d_Dimuon_lxy16p0to70p0_iso1_ptlow");
  dNames.push_back("d_Dimuon_lxy16p0to70p0_iso1_pthigh");
  dNames.push_back("d_Dimuon_lxy0p0to0p2_non-pointing");
  dNames.push_back("d_Dimuon_lxy0p2to1p0_non-pointing");
  dNames.push_back("d_Dimuon_lxy1p0to2p4_non-pointing");
  dNames.push_back("d_Dimuon_lxy2p4to3p1_non-pointing");
  dNames.push_back("d_Dimuon_lxy3p1to7p0_non-pointing");
  dNames.push_back("d_Dimuon_lxy7p0to11p0_non-pointing");
  dNames.push_back("d_Dimuon_lxy11p0to16p0_non-pointing");
  dNames.push_back("d_Dimuon_lxy16p0to70p0_non-pointing");
  //dNames.push_back("");

  // Eras (to be uncommented when adding 2023 and splitting in eras)
  vector<TString> eras;
  if (period=="2022") {
    eras.push_back("2022");
    eras.push_back("2022postEE");
  } else if (period=="2023") {
    eras.push_back("2023");
    eras.push_back("2023BPix");
  } else if (period=="allEras") {
    eras.push_back("2022");
    eras.push_back("2022postEE");
    eras.push_back("2023");
    eras.push_back("2023BPix");
  }

  vector<TString> samples = { };
  vector<TString> sigmodels = { };
  vector<TString> sigsamples = { };
  vector<float> sigmasses_2mu = { };
  vector<float> sigmasses_4mu = { };
  vector<float> sigmasses_ctau = { };

  if ( useData ) {
    samples.push_back("Data");
  }

  // Signals (Should include sigMass, sigCtau and a proper definition for sigmasses_4mu)
  //vector<float> sigMass = {0.5, 0.7, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0};
  if ( model=="HTo2ZdTo2mu2x" ) {
    if ( useSignalMC ) {
      vector<float> sigMass = {0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0};
      vector<float> sigCtau = {1, 10, 100, 1000};
      for ( unsigned int m=0; m<sigMass.size(); m++ ) {
        TString massString = Form("%.1f",sigMass[m]); 
        massString.ReplaceAll(".", "p");
        for ( unsigned int t=0; t<sigCtau.size(); t++ ) {
          if ( (sigMass[m] < 1.0 && sigCtau[t] > 10) || (sigMass[m] < 30.0 && sigCtau[t] > 100) )
            continue;
          TString ctauString = Form("%.0f",sigCtau[t]); 
          sigsamples.push_back(Form("Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm",massString.Data(),ctauString.Data()));
          sigmasses_2mu.push_back(sigMass[m]);
          sigmasses_4mu.push_back(125.); // Mass of the higgs
          sigmasses_ctau.push_back(sigCtau[t]); // Lifetime
          std::cout << Form("Reading signal sample: Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm",massString.Data(),ctauString.Data()) << std::endl;
        }
      }
    } else {
      vector<float> sigCtau = {1, 10, 100, 1000};
      float lastmass = 0.5;
      while (lastmass < 50.0)
      {
        lastmass = 1.04*lastmass;
        if (!passMassVeto(lastmass))
          continue;
        float intpmass = lastmass;
        for ( unsigned int t=0; t<sigCtau.size(); t++ ) {
          if ( (intpmass < 1.0 && sigCtau[t] > 10) || (intpmass < 30.0 && sigCtau[t] > 100) )
            continue;
          TString ctauString = Form("%.1f",sigCtau[t]);
          TString massString = Form("%.3f",intpmass); 
          sigsamples.push_back(Form("Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm",massString.Data(),ctauString.Data()));
          sigmasses_2mu.push_back(intpmass);
          sigmasses_4mu.push_back(125.);
          sigmasses_ctau.push_back(sigCtau[t]);
          std::cout << Form("Interpolating signal sample: Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm",massString.Data(),ctauString.Data()) << std::endl;
        }
      }
    }
  } else if (model=="ScenarioB1") {
    vector<float> sigMass = {1.33};
    vector<float> sigCtau = {0.1, 1, 10, 100};
    for ( unsigned int m=0; m<sigMass.size(); m++ ) {
      TString massString = Form("%.2f",sigMass[m]); 
      massString.ReplaceAll(".", "p");
      for ( unsigned int t=0; t<sigCtau.size(); t++ ) {
        if ( (sigMass[m] < 1.0 && sigCtau[t] > 10) || (sigMass[m] < 30.0 && sigCtau[t] > 100) )
          continue;
        TString ctauString;
        if (sigCtau[t]<1.0) {
          ctauString = Form("%.1f",sigCtau[t]);
          ctauString.ReplaceAll(".", "p");
        } else {
          ctauString = Form("%.0f",sigCtau[t]);
        }
        sigsamples.push_back(Form("Signal_ScenarioB1_mpi-4_mA-%s_ctau-%smm",massString.Data(),ctauString.Data()));
        sigmasses_2mu.push_back(sigMass[m]);
        sigmasses_4mu.push_back(4.); // Mass of the mother particle
        std::cout << Form("Reading signal sample: Signal_ScenarioB1_mpi-4_mA-%s_ctau-%smm",massString.Data(),ctauString.Data()) << std::endl;
      }
    }
  }

  /*
  if ( !(useSignalMC) ) {
    sigMass = {mF};
    float tm = mF;
    while ( tm < mL ) {
      if(tm<400.00) tm+=5.0;
      else if(tm<700) tm+=10.0;
      else if(tm<1000.0) tm+=15.0;
      else if (tm<1500.0) tm+=25.0;
      else tm+=50.0;
      sigMass.push_back(tm);
    }
  }
  */

 // Loop over datasets
 TSystemDirectory dir(inDir, inDir);
 TList* files = dir.GetListOfFiles(); 
 if (!files) {
   std::cerr << "Error: List of files can't be listed" << inDir << std::endl;
   return;
 }
 vector<RooDataSet> mmumu_bkgs = {};
 vector<vector<RooDataSet>> mmumu_sigs {{}}; 
 vector<vector<RooDataSet>> mmumu_sigs_trg_up {{}}; 
 vector<vector<RooDataSet>> mmumu_sigs_trg_down {{}}; 
 vector<vector<RooDataSet>> mmumu_sigs_sel_up {{}}; 
 vector<vector<RooDataSet>> mmumu_sigs_sel_down {{}}; 
 cout << "Preparing to read datasets..." << endl;
 for ( unsigned int d=0; d<dNames.size(); d++ ) {
   // Loop over datasets
   for ( unsigned int iera=0; iera<eras.size(); iera++ ) {
     //std::cout << "Loading dataset: " << dNames[d] << std::endl;
     vector<TString> dataEras = {};
     TString era = eras[iera];
     TString year = "2022";
     if (era.Contains("2022"))
       year = "2022";
     else
       year = "2023";
     if (era=="2022") {
       dataEras.push_back("DataC"); dataEras.push_back("DataD"); dataEras.push_back("DataE");
     } else if (era=="2022postEE") {
       dataEras.push_back("DataF"); dataEras.push_back("DataG");
     } else if (era=="2023") {
       dataEras.push_back("DataC");
     } else if (era=="2023BPix") {
       dataEras.push_back("DataD");
     }
     // Loop over data files
     int idata = 0;
     for (const auto& file : *files) {
       TString filename = file->GetName();
       if (!filename.BeginsWith("histograms_Data") || filename.EndsWith("all.root"))
         continue;
       bool toRead = false;
       for ( unsigned int jera=0; jera<dataEras.size(); jera++ ) {
         if (filename.Contains(year) && filename.Contains(dataEras[jera])) {
           toRead = true; break;
         }
       }
       if (!toRead)
         continue;
       TString inFile = Form("%s/%s",inDir.Data(),filename.Data());
       TFile fin(inFile, "READ");
       std::cout << inFile << std::endl;
       if (idata == 0) {
         RooDataSet *tds = (RooDataSet*) fin.Get(dNames[d])->Clone();
         mmumu_bkgs.push_back( *tds );
         //std::cout << "Appended: " << filename.Data() << std::endl;
       } else {
         RooDataSet *tds_other = (RooDataSet*) fin.Get(dNames[d])->Clone();
         mmumu_bkgs[iera].append( *tds_other );
         //std::cout << "Appended: " << filename.Data() << std::endl;
       }
       fin.Close();
       idata++;
     }
     mmumu_bkgs[iera].SetName(dNames[d]+"_data_"+year+"_"+era);

     // Loop over signals 
     for ( int isample=0; isample<sigsamples.size(); isample++ ) {
       TString sample = sigsamples[isample];
       cout<<"Sample: "<< sample << endl;
       if ( useSignalMC ) {
         TString inFile = Form("%s/histograms_%s_%s_%s_0.root",inDir.Data(),sample.Data(),era.Data(),year.Data());
         TFile fin(inFile);
         RooDataSet *tds = (RooDataSet*) fin.Get(dNames[d])->Clone();
         tds->SetName(dNames[d]+"_"+sample+"_"+year+"_"+era);
         std::cout << "Reading signal file: " <<  inFile << ", with dataset with entries: " << tds->sumEntries() << std::endl;
         if (iera == 0) {
           vector<RooDataSet> tds_aux{};
           mmumu_sigs.push_back( tds_aux );
         }
         mmumu_sigs[isample].push_back( *tds );
         if (doUpAndDownVariations) {
           RooDataSet *tds_trg_up = (RooDataSet*) fin.Get(dNames[d]+"_trg_up")->Clone();
           RooDataSet *tds_trg_down = (RooDataSet*) fin.Get(dNames[d]+"_trg_down")->Clone();
           RooDataSet *tds_sel_up = (RooDataSet*) fin.Get(dNames[d]+"_sel_up")->Clone();
           RooDataSet *tds_sel_down = (RooDataSet*) fin.Get(dNames[d]+"_sel_down")->Clone();
           tds_trg_up->SetName(dNames[d]+"_"+sample+"_"+year+"_"+era+"_trg_up");
           tds_trg_down->SetName(dNames[d]+"_"+sample+"_"+year+"_"+era+"_trg_down");
           tds_sel_up->SetName(dNames[d]+"_"+sample+"_"+year+"_"+era+"_sel_up");
           tds_sel_down->SetName(dNames[d]+"_"+sample+"_"+year+"_"+era+"_sel_down");
           if (iera == 0) {
             vector<RooDataSet> tds_aux_trg_up{};
             vector<RooDataSet> tds_aux_trg_down{};
             vector<RooDataSet> tds_aux_sel_up{};
             vector<RooDataSet> tds_aux_sel_down{};
             mmumu_sigs_trg_up.push_back( tds_aux_trg_up );
             mmumu_sigs_trg_down.push_back( tds_aux_trg_down );
             mmumu_sigs_sel_up.push_back( tds_aux_sel_up );
             mmumu_sigs_sel_down.push_back( tds_aux_sel_down );
           }
           mmumu_sigs_trg_up[isample].push_back( *tds_trg_up );
           mmumu_sigs_trg_down[isample].push_back( *tds_trg_down );
           mmumu_sigs_sel_up[isample].push_back( *tds_sel_up );
           mmumu_sigs_sel_down[isample].push_back( *tds_sel_down );
         }
         fin.Close();
         cout << "Number of entries for the mmumu_sigs RooDataSet: " << mmumu_sigs[isample][iera].numEntries() << endl;
       } //else {
       //  RooDataSet *tds = (RooDataSet*) mmumu_bkgs[iera].emptyClone(dNames[d]+"_"+sample+"_"+year, "");
       //  mmumu_sigs.push_back( *tds );
       //}
     }
   }
   
   if (mergeEras) {
     TString outDir = "fitResults_"+period;
     RooDataSet mmumu_bkg_merged = mmumu_bkgs[0];
     for ( int iera=1; iera<eras.size(); iera++ ) {
         mmumu_bkg_merged.append(mmumu_bkgs[iera]);
     }
     mmumu_bkg_merged.SetName(dNames[d]+"_Data_"+period);
     cout << "Merged dataset for background has entries: " << mmumu_bkg_merged.sumEntries() << endl;
     vector<RooDataSet> mmumu_sig_merged = {};
     vector<RooDataSet> mmumu_sig_trg_up_merged = {};
     vector<RooDataSet> mmumu_sig_trg_down_merged = {};
     vector<RooDataSet> mmumu_sig_sel_up_merged = {};
     vector<RooDataSet> mmumu_sig_sel_down_merged = {};
     for (unsigned int isample=0; isample<sigsamples.size(); isample++ ) {
       // Create worksapce, import data and model
       std::cout << "Creating merged workspace" << std::endl;
       RooWorkspace wfit("wfit","workspace"); 
       RooWorkspace wfit_trg_up("wfit_trg_up","workspace_trg_up");
       RooWorkspace wfit_trg_down("wfit_trg_down","workspace_trg_down");
       RooWorkspace wfit_sel_up("wfit_sel_up","workspace_sel_up");
       RooWorkspace wfit_sel_down("wfit_sel_down","workspace_sel_down");
       if (useSignalMC) {
         for (unsigned int iera=0; iera<eras.size(); iera++ ) {
           if (iera==0)
             mmumu_sig_merged.push_back(mmumu_sigs[isample][iera]);
           else
             mmumu_sig_merged[isample].append(mmumu_sigs[isample][iera]);
         }
       } else {
         RooDataSet *tds = (RooDataSet*) mmumu_bkg_merged.emptyClone(dNames[d]+"_"+sigsamples[isample]+"_"+period, "");
         mmumu_sig_merged.push_back( *tds );
       }
       mmumu_sig_merged[isample].SetName(dNames[d]+"_"+sigsamples[isample]+"_"+period);
       if (doUpAndDownVariations) {
         for (unsigned int iera=0; iera<eras.size(); iera++ ) {
           if (iera==0) {
             mmumu_sig_trg_up_merged.push_back(mmumu_sigs_trg_up[isample][iera]);
             mmumu_sig_trg_down_merged.push_back(mmumu_sigs_trg_down[isample][iera]);
             mmumu_sig_sel_up_merged.push_back(mmumu_sigs_sel_up[isample][iera]);
             mmumu_sig_sel_down_merged.push_back(mmumu_sigs_sel_down[isample][iera]);
           } else {
             mmumu_sig_trg_up_merged[isample].append(mmumu_sigs_trg_up[isample][iera]);
             mmumu_sig_trg_down_merged[isample].append(mmumu_sigs_trg_down[isample][iera]);
             mmumu_sig_sel_up_merged[isample].append(mmumu_sigs_sel_up[isample][iera]);
             mmumu_sig_sel_down_merged[isample].append(mmumu_sigs_sel_down[isample][iera]);
           }
         }  
         mmumu_sig_trg_up_merged[isample].SetName(dNames[d]+"_"+sigsamples[isample]+"_"+period+"_trg_up");
         mmumu_sig_trg_down_merged[isample].SetName(dNames[d]+"_"+sigsamples[isample]+"_"+period+"_trg_down");
         mmumu_sig_sel_up_merged[isample].SetName(dNames[d]+"_"+sigsamples[isample]+"_"+period+"_sel_up");
         mmumu_sig_sel_down_merged[isample].SetName(dNames[d]+"_"+sigsamples[isample]+"_"+period+"_sel_down");
       }
       cout << "Merged dataset for signal " << sigsamples[isample] << " with entries " << mmumu_sig_merged[isample].sumEntries() << endl;
       // Fit invariant mass
       std::cout << "Prepare to fit..." << std::endl;
       if (dNames[d].BeginsWith("d_FourMu_")) {
         fitmass(mmumu_sig_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_4mu[isample], sigmasses_ctau[isample], wfit, true, period, "dcbfastg", outDir);
         fitmass(mmumu_bkg_merged, "Background", true, false, false, sigsamples[isample], sigmasses_2mu[isample], sigmasses_4mu[isample], sigmasses_ctau[isample], wfit, true, period, "", outDir); 
       } else {
         fitmass(mmumu_sig_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_2mu[isample], sigmasses_ctau[isample], wfit, false, period, "dcbfastg", outDir);
         fitmass(mmumu_bkg_merged, "Background", true, false, false, sigsamples[isample], sigmasses_2mu[isample], sigmasses_2mu[isample], sigmasses_ctau[isample], wfit, false, period, "", outDir); 
       }
       if (doUpAndDownVariations) { 
         if (dNames[d].BeginsWith("d_FourMu_")) {
           fitmass(mmumu_sig_trg_up_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_4mu[isample], sigmasses_ctau[isample], wfit_trg_up, true, period, "dcbfastg", outDir);
           fitmass(mmumu_sig_trg_down_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_4mu[isample], sigmasses_ctau[isample], wfit_trg_down, true, period, "dcbfastg", outDir);
           fitmass(mmumu_sig_sel_up_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_4mu[isample], sigmasses_ctau[isample], wfit_sel_up, true, period, "dcbfastg", outDir);
           fitmass(mmumu_sig_sel_down_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_4mu[isample], sigmasses_ctau[isample], wfit_sel_down, true, period, "dcbfastg", outDir);
         } else {
           fitmass(mmumu_sig_trg_up_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_2mu[isample], sigmasses_ctau[isample], wfit_trg_up, false, period, "dcbfastg", outDir);
           fitmass(mmumu_sig_trg_down_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_2mu[isample], sigmasses_ctau[isample], wfit_trg_down, false, period, "dcbfastg", outDir);
           fitmass(mmumu_sig_sel_up_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_2mu[isample], sigmasses_ctau[isample], wfit_sel_up, false, period, "dcbfastg", outDir);
           fitmass(mmumu_sig_sel_down_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], sigmasses_2mu[isample], sigmasses_ctau[isample], wfit_sel_down, false, period, "dcbfastg", outDir);
         }
       }
       
    
       // Print workspace contents
       std::cout << "Workspace contents: " << std::endl;
       wfit.Print();

       // Save the workspace into a ROOT file
       if ( writeWS ) {
         TString fwsname = Form("%s/%s_workspace.root",outDir.Data(),mmumu_sig_merged[isample].GetName());
         TFile *fws = new TFile(fwsname, "RECREATE");
         fws->cd();
         cout << "Writing workspace..." << endl;
         wfit.Write();
         if (doUpAndDownVariations) { 
           wfit_trg_up.Write();
           wfit_trg_down.Write();
           wfit_sel_up.Write();
           wfit_sel_down.Write();
         }
         fws->Close();
       }
       cout<<endl;
     }
   }
   std::cout << "Cleaning the workspace containers..." << std::endl;
   for ( int isample=0; isample<sigsamples.size(); isample++ ) {
     if (useSignalMC)
       mmumu_sigs[isample].clear();
     if (doUpAndDownVariations) { 
       mmumu_sigs_trg_up[isample].clear();
       mmumu_sigs_trg_down[isample].clear();
       mmumu_sigs_sel_up[isample].clear();
       mmumu_sigs_sel_down[isample].clear();
     }
   }
   if (useSignalMC)
     mmumu_sigs.clear();
   if (doUpAndDownVariations) { 
     mmumu_sigs_trg_up.clear();
     mmumu_sigs_trg_down.clear();
     mmumu_sigs_sel_up.clear();
     mmumu_sigs_sel_down.clear();
   }
   mmumu_bkgs.clear();
 }

  /*
  if ( !mergeYears ) {
    for ( int iyear=0; iyear<years.size(); iyear++ ) {
	for ( int isample=0; isample<sigsamples.size(); isample++ ) {
	  TString sample = sigsamples[isample];
	  cout<<"Sample: "<<sample<<endl;
	  if ( useSignalMC ) {
	    TString inFile = Form("%s/output_%s_%s.root",inDir.Data(),sample.Data(),year.Data());
	    TFile fin(inFile);
	    RooDataSet *tds = (RooDataSet*) fin.Get(dNames[d])->Clone();
	    tds->SetName(dNames[d]+"_"+sample+"_"+year);
	    mmumu_sig.push_back( *tds );
	    fin.Close();
	  }
	  else {
	    RooDataSet *tds = (RooDataSet*) mmumu_bkg->emptyClone(dNames[d]+"_"+sample+"_"+year, "");
	    mmumu_sig.push_back( *tds );
	  }
	  // Create workspace, import data and model
	  TString outDir = "fitResults";
	  RooWorkspace wfit("wfit","workspace");

	  fitmass(mmumu_sig[isample], sample, false, true, false, sigmodels[isample], sigmasses[isample], wfit, "dcbfastg", outDir);
	  if ( samples.size() > 0 ) {
	    if ( useData )
	      fitmass(*mmumu_bkg, "Background", true, false, false, sigmodels[isample], sigmasses[isample], wfit, "", outDir);
	    else
	      fitmass(*mmumu_bkg, "Background", false, false, false, sigmodels[isample], sigmasses[isample], wfit, "", outDir);
	  }

	  // Print workspace contents
	  wfit.Print();

	  if ( writeWS ) {
	    // Save the workspace into a ROOT file
	    TString fwsname = Form("%s/%s_workspace.root",outDir.Data(),mmumu_sig[isample].GetName());
	    TFile *fws = new TFile(fwsname, "RECREATE");
	    fws->cd();
	    cout << "Writing workspace..." << endl;
	    wfit.Write();
	    fws->Close();
	  }
	  cout<<endl;
	}
      }
    }
  }
  else {
    for ( unsigned int d=0; d<dNames.size(); d++ ) {  
      RooDataSet *mmumu_bkg;
      cout<<endl;
      cout<<"Dataset: "<<d<<endl;
      cout<<"------------"<<endl;
      for ( int isample=0; isample<samples.size(); isample++ ) {
      	TString sample = samples[isample];
      	cout<<"Sample: "<<sample<<endl;
      	for ( int iyear=0; iyear<years.size(); iyear++ ) {
      	  TString year = years[iyear];
      	  cout<<endl;
      	  cout<<"Year: "<<year<<endl;
      	  TString inFile = Form("%s/output_%s_%s.root",inDir.Data(),sample.Data(),year.Data());
      	  TFile fin(inFile);
      	  if ( isample==0 && iyear==0 ) {
      	    mmumu_bkg = (RooDataSet*) fin.Get(dNames[d])->Clone();
      	  }
      	  else {
      	    RooDataSet *tds_other = (RooDataSet*) fin.Get(dNames[d])->Clone();
      	    mmumu_bkg->append( *tds_other );
      	  }
      	  fin.Close();
      	}
      }
      if ( useData )
      	mmumu_bkg->SetName(dNames[d]+"_data_allyears");
      else
      	mmumu_bkg->SetName(dNames[d]+"_BGMC_allyears");
      vector<RooDataSet*> mmumu_sig = { };
      for ( int isample=0; isample<sigsamples.size(); isample++ ) {
	TString sample = sigsamples[isample];
	cout<<"Sample: "<<sample<<endl;
	if ( useSignalMC ) {
	  for ( int iyear=0; iyear<years.size(); iyear++ ) {
	    TString year = years[iyear];
	    cout<<endl;
	    cout<<"Year: "<<year<<endl;
	    TString inFile = Form("%s/output_%s_%s.root",inDir.Data(),sample.Data(),year.Data());
	    TFile fin(inFile);
	    RooDataSet *tds;
	    if ( iyear==0 ) {
	      tds = (RooDataSet*) fin.Get(dNames[d])->Clone();
	      mmumu_sig.push_back(tds);
	    }
	    else {
	      RooDataSet *tds_other = (RooDataSet*) fin.Get(dNames[d])->Clone();
	      mmumu_sig[isample]->append( *tds_other );
	    }
	    fin.Close();
	  }
	  mmumu_sig[isample]->SetName(dNames[d]+"_"+sample+"_allyears");
	}
	else { 
	  mmumu_sig.push_back( (RooDataSet*) mmumu_bkg->emptyClone(dNames[d]+"_"+sample+"_allyears", "") );
	}
	// Create workspace, import data and model
	TString outDir = "fitResults_fullRange";
	RooWorkspace wfit("wfit","workspace");

	fitmass(*mmumu_sig[isample], sample, false, true, false, sigmodels[isample], sigmasses[isample], wfit, "dcbfastg", outDir);
	if ( samples.size() > 0 ) {
	  if ( useData )
	    fitmass(*mmumu_bkg, "Background", true, false, false, sigmodels[isample], sigmasses[isample], wfit, "", outDir);
	  else
	    fitmass(*mmumu_bkg, "Background", false, false, false, sigmodels[isample], sigmasses[isample], wfit, "", outDir);
	}

	// Print workspace contents
	wfit.Print();

	if ( writeWS ) {
	  // Save the workspace into a ROOT file
	  TString fwsname = Form("%s/%s_workspace.root",outDir.Data(),mmumu_sig[isample]->GetName());
	  TFile *fws = new TFile(fwsname, "RECREATE");
	  fws->cd();
	  cout << "Writing workspace..." << endl;
	  wfit.Write();
	  fws->Close();
	}
	cout<<endl;
      }
    }
  }
  */
}
