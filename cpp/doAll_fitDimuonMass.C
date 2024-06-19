{
  gROOT->ProcessLine(".L ./cpp/fit_dimuon.C+");  // Macro that performs the selection

  bool useData = true;
  //bool useData = false;
  bool useSignalMC = true;
  //bool useSignalMC = true;
  bool mergeEras = true;
  bool writeWS = true;
  TString period = "2022"; // Either 2022 or 2023
  TString model = "HTo2ZdTo2mu2x";
  float mF = 350.0;
  float mL = 2000.0;
  

  // Dir with the RooDataSets
  TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_SRsOnly_2022"; // last 2022
  //TString inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_SRsOnly_2023"; // last 2023

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

  if ( useData ) {
    samples.push_back("Data");
  }

  // Signals (To be modified: Needs to be more general but this is provisional)
  //vector<float> sigMass = {0.5, 0.7, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0};
  if ( model=="HTo2ZdTo2mu2x" ) {
  vector<float> sigMass = {0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0};
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
      std::cout << Form("Reading signal sample: Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm",massString.Data(),ctauString.Data()) << std::endl;
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
 vector<RooDataSet> mmumu_bkgs = {};
 vector<vector<RooDataSet>> mmumu_sigs {{}}; 
 cout << "Preparing to read datasets..." << endl;
 for ( unsigned int d=0; d<dNames.size(); d++ ) {
   // Loop over datasets
   for ( unsigned int iera=0; iera<eras.size(); iera++ ) {
     std::cout << "Loading dataset: " << dNames[d] << std::endl;
     vector<TString> dataEras = {};
     TString era = eras[iera];
     TString year = "2022";
     if (era.Contains("2022"))
       year = "2022";
     // else if (era.Contains("2023"))
     else
       year = "2023";
     if (era=="2022") {
       dataEras.push_back("DataC"); dataEras.push_back("DataD"); dataEras.push_back("DataE");
     //} else if (year=="2022postEE") {
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
       //std::cout << "File: " << file->GetName() << std::endl;
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
         std::cout << "Appended: " << filename.Data() << std::endl;
       } else {
         RooDataSet *tds_other = (RooDataSet*) fin.Get(dNames[d])->Clone();
         mmumu_bkgs[iera].append( *tds_other );
         std::cout << "Appended: " << filename.Data() << std::endl;
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
           //tds_aux.push_back( *tds );
           mmumu_sigs.push_back( tds_aux );
           mmumu_sigs[isample].push_back( *tds );
         } else {
           mmumu_sigs[isample].push_back( *tds );
         }
         fin.Close();
       } //else {
       //  RooDataSet *tds = (RooDataSet*) mmumu_bkgs[iera].emptyClone(dNames[d]+"_"+sample+"_"+year, "");
       //  mmumu_sigs.push_back( *tds );
       //}
       cout << mmumu_sigs[isample][iera].numEntries() << endl;
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
     for (unsigned int isample=0; isample<sigsamples.size(); isample++ ) {
       // Create worksapce, import data and model
       std::cout << "Creating merged workspace" << std::endl;
       RooWorkspace wfit("wfit","workspace"); 
       for (unsigned int iera=0; iera<eras.size(); iera++ ) {
         if (iera==0)
           mmumu_sig_merged.push_back(mmumu_sigs[isample][iera]);
         else
           mmumu_sig_merged[isample].append(mmumu_sigs[isample][iera]);
       }  
       mmumu_sig_merged[isample].SetName(dNames[d]+"_"+sigsamples[isample]+"_"+period);
       cout << "Merged dataset for signal " << sigsamples[isample] << " with entries " << mmumu_sig_merged[isample].sumEntries() << endl;
       // Fit invariant mass
       std::cout << "Prepare to fit..." << std::endl;
       //if (dNames[d].BeginsWith("d_FourMu_osv")) {
       if (dNames[d].BeginsWith("d_FourMu_")) {
         fitmass(mmumu_sig_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_4mu[isample], wfit, true, period, "dcbfastg", outDir);
         fitmass(mmumu_bkg_merged, "Background", true, false, false, sigsamples[isample], sigmasses_4mu[isample], wfit, true, period, "", outDir); 
       } else {
         fitmass(mmumu_sig_merged[isample], "Signal", false, true, true, sigsamples[isample], sigmasses_2mu[isample], wfit, false, period, "dcbfastg", outDir);
         fitmass(mmumu_bkg_merged, "Background", true, false, false, sigsamples[isample], sigmasses_2mu[isample], wfit, false, period, "", outDir); 
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
         fws->Close();
       }
       cout<<endl;
     }
   }
   for ( int isample=0; isample<sigsamples.size(); isample++ ) {
     mmumu_sigs[isample].clear();
   }
   mmumu_sigs.clear();
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
