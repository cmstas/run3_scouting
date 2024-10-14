### No cuts
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noCuts --noDiMuonAngularSel --noMuonIPSel --noMuonHitSel --noMaterialVeto
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_materialVetoOnly --noDiMuonAngularSel --noMuonIPSel --noMuonHitSel
### All cuts
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_allCuts
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_allCuts
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p2_allCuts --lxySel 0.0 0.2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p2_allCuts --lxySel 0.0 0.2
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p2to1p0_allCuts --lxySel 0.2 1.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p2to1p0_allCuts --lxySel 0.2 1.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_1p0to2p4_allCuts --lxySel 1.0 2.4
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_1p0to2p4_allCuts --lxySel 1.0 2.4
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p4to3p1_allCuts --lxySel 2.4 3.1
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p4to3p1_allCuts --lxySel 2.4 3.1
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_3p1to7p0_allCuts --lxySel 3.1 7.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_3p1to7p0_allCuts --lxySel 3.1 7.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_7p0to11p0_allCuts --lxySel 7.0 11.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_7p0to11p0_allCuts --lxySel 7.0 11.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_allCuts --lxySel 11.0 16.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_allCuts --lxySel 11.0 16.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_allCuts --lxySel 16.0 70.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_allCuts --lxySel 16.0 70.0
## No Hits run 3 splitting
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p2_noHitSel --noMuonHitSel --lxySel 0.0 0.2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p2_noHitSel --noMuonHitSel --lxySel 0.0 0.2
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p2to1p0_noHitSel --noMuonHitSel --lxySel 0.2 1.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p2to1p0_noHitSel --noMuonHitSel --lxySel 0.2 1.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_1p0to2p4_noHitSel --noMuonHitSel --lxySel 1.0 2.4
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_1p0to2p4_noHitSel --noMuonHitSel --lxySel 1.0 2.4
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p4to3p1_noHitSel --noMuonHitSel --lxySel 2.4 3.1
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p4to3p1_noHitSel --noMuonHitSel --lxySel 2.4 3.1
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_3p1to7p0_noHitSel --noMuonHitSel --lxySel 3.1 7.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_3p1to7p0_noHitSel --noMuonHitSel --lxySel 3.1 7.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_7p0to11p0_noHitSel --noMuonHitSel --lxySel 7.0 11.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_7p0to11p0_noHitSel --noMuonHitSel --lxySel 7.0 11.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_noHitSel --noMuonHitSel --lxySel 11.0 16.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_noHitSel --noMuonHitSel --lxySel 11.0 16.0
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_noHitSel --noMuonHitSel --lxySel 16.0 70.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_noHitSel --noMuonHitSel --lxySel 16.0 70.0
### No angular cuts
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noDiMuonAngularSel --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noDiMuonAngularSel --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p5_noDiMuonAngularSel --lxySel 0.0 0.5 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p0_noDiMuonAngularSel --lxySel 0.0 0.5 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p5to2p7_noDiMuonAngularSel --lxySel 0.5 2.7 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p5to2p7_noDiMuonAngularSel --lxySel 0.5 2.7 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p7to6p5_noDiMuonAngularSel --lxySel 2.7 6.5 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p7to6p5_noDiMuonAngularSel --lxySel 2.7 6.5 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_6p5to11p0_noDiMuonAngularSel --lxySel 6.5 11.0 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_6p5to11p0_noDiMuonAngularSel --lxySel 6.5 11.0 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_noDiMuonAngularSel --lxySel 11.0 16.0 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_noDiMuonAngularSel --lxySel 11.0 16.0 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_noDiMuonAngularSel --lxySel 16.0 70.0 --noDiMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_noDiMuonAngularSel --lxySel 16.0 70.0 --noDiMuonAngularSel
### No IP cuts
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noMuonIPSel --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noMuonIPSel --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p5_noMuonIPSel --lxySel 0.0 0.5 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p5_noMuonIPSel --lxySel 0.0 0.5 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p5to2p7_noMuonIPSel --lxySel 0.5 2.7 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p5to2p7_noMuonIPSel --lxySel 0.5 2.7 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p7to6p5_noMuonIPSel --lxySel 2.7 6.5 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p7to6p5_noMuonIPSel --lxySel 2.7 6.5 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_6p5to11p0_noMuonIPSel --lxySel 6.5 11.0 --noMuonIPSel 
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_6p5to11p0_noMuonIPSel --lxySel 6.5 11.0 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to70p0_noMuonIPSel --lxySel 11.0 70.0 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to70p0_noMuonIPSel --lxySel 11.0 70.0 --noMuonIPSel
### No hit cuts
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noMuonHitSel --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noMuonHitSel --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p5_noMuonHitSel --lxySel 0.0 0.5 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p0to0p5_noMuonHitSel --lxySel 0.0 0.5 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p5to2p7_noMuonHitSel --lxySel 0.5 2.7 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_0p5to2p7_noMuonHitSel --lxySel 0.5 2.7 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p7to6p5_noMuonHitSel --lxySel 2.7 6.5 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2p7to6p5_noMuonHitSel --lxySel 2.7 6.5 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_6p5to11p0_noMuonHitSel --lxySel 6.5 11.0 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_6p5to11p0_noMuonHitSel --lxySel 6.5 11.0 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_noMuonHitSel --lxySel 11.0 16.0 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_11p0to16p0_noMuonHitSel --lxySel 11.0 16.0 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_noMuonHitSel --lxySel 16.0 70.0 --noMuonHitSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_16p0to70p0_noMuonHitSel --lxySel 16.0 70.0 --noMuonHitSel
## No four muon angular cut
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noFourMuonAngularSel --noFourMuonAngularSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noFourMuonAngularSel --noFourMuonAngularSel
## No four muon mass diff cut
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noFourMuonMassDiffSel --noFourMuonMassDiffSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_noFourMuonMassDiffSel --noFourMuonMassDiffSel
## Seeds study
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_allSeeds
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu_12_5 --noSeed L1_DoubleMu_12_5
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu_15_7 --noSeed L1_DoubleMu_15_7
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7 --noSeed L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18 --noSeed L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu4_SQ_OS_dR_Max1p2 --noSeed L1_DoubleMu4_SQ_OS_dR_Max1p2
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu4p5_SQ_OS_dR_Max1p2 --noSeed L1_DoubleMu4p5_SQ_OS_dR_Max1p2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_allSeeds 
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu_12_5 --noSeed L1_DoubleMu_12_5
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu_15_7 --noSeed L1_DoubleMu_15_7
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7 --noSeed L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18 --noSeed L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu4_SQ_OS_dR_Max1p2 --noSeed L1_DoubleMu4_SQ_OS_dR_Max1p2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu4p5_SQ_OS_dR_Max1p2 --noSeed L1_DoubleMu4p5_SQ_OS_dR_Max1p2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu0er1p4_SQ_OS_dR_Max1p4 --noSeed L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu0er1p5_SQ_OS_dR_Max1p4 --noSeed L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu8_SQ --noSeed L1_DoubleMu8_SQ
## Grouped
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu_A_B --noSeed L1_DoubleMu_12_5 L1_DoubleMu_15_7
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMu4p5er2p0_SQ_OS_Mass_X --noSeed L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7 L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2022_noL1_DoubleMuX_SQ_OS_dR_Max1p2 --noSeed L1_DoubleMu4_SQ_OS_dR_Max1p2 L1_DoubleMu4p5_SQ_OS_dR_Max1p2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu_A_B --noSeed L1_DoubleMu_12_5 L1_DoubleMu_15_7
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMu4p5er2p0_SQ_OS_Mass_X --noSeed L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7 L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMuX_SQ_OS_dR_Max1p2 --noSeed L1_DoubleMu4_SQ_OS_dR_Max1p2 L1_DoubleMu4p5_SQ_OS_dR_Max1p2
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Jul-04-2024_2022/ outputHistograms_Sep-19-2024_2023_noL1_DoubleMuAerB_SQ_OS_dR_Max1p4 --noSeed L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4 L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4
