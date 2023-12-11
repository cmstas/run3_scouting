#!bin/bash

###

python3 plotHistosScouting.py --inSamples Data --inDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_all --relaxedSVSel --shape --logY --outSuffix all >& /dev/null &

python3 plotHistosScouting.py --inSamples Data --inDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_all --shape --logY --outSuffix all >& /dev/null &

#

python3 plotHistosScouting.py --inSamples Data --inDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMassDiff0p05AvgMass_onlyFourMuon --relaxedSVSel --shape --logY --outSuffix dimuonMassDiff0p05AvgMass_onlyFourMuon >& /dev/null &

python3 plotHistosScouting.py --inSamples Data --inDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMassDiff0p05AvgMass_onlyFourMuon --shape --logY --outSuffix dimuonMassDiff0p05AvgMass_onlyFourMuon >& /dev/null &

###
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy0p0to0p2_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy0p0to0p2 --lxySel 0.0 0.2 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy0p0to0p2_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy0p0to0p2 --lxySel 0.0 0.2 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy0p2to1p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy0p2to1p0 --lxySel 0.2 1.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy0p2to1p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy0p2to1p0 --lxySel 0.2 1.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy1p0to2p4_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy1p0to2p4 --lxySel 1.0 2.4 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy1p0to2p4_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy1p0to2p4 --lxySel 1.0 2.4 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy2p4to3p1_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy2p4to3p1 --lxySel 2.4 3.1 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy2p4to3p1_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy2p4to3p1 --lxySel 2.4 3.1 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy3p1to11p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy3p1to11p0 --lxySel 3.1 11.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy3p1to11p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy3p1to11p0 --lxySel 3.1 11.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy11p0to16p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy11p0to16p0 --lxySel 11.0 16.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy11p0to16p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy11p0to16p0 --lxySel 11.0 16.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy16p0to50p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy16p0to50p0 --lxySel 16.0 50.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy16p0to50p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy16p0to50p0 --lxySel 16.0 50.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy50p0to110p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy50p0to110p0 --lxySel 50.0 110.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy50p0to110p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi_lxy50p0to110p0 --lxySel 50.0 110.0 >& /dev/null &
#
##
#
###
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy0p0to0p2_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy0p0to0p2 --lxySel 0.0 0.2 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy0p0to0p2_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy0p0to0p2 --lxySel 0.0 0.2 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy0p2to1p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy0p2to1p0 --lxySel 0.2 1.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy0p2to1p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy0p2to1p0 --lxySel 0.2 1.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy1p0to2p4_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy1p0to2p4 --lxySel 1.0 2.4 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy1p0to2p4_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy1p0to2p4 --lxySel 1.0 2.4 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy2p4to3p1_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy2p4to3p1 --lxySel 2.4 3.1 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy2p4to3p1_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy2p4to3p1 --lxySel 2.4 3.1 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy3p1to11p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy3p1to11p0 --lxySel 3.1 11.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy3p1to11p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy3p1to11p0 --lxySel 3.1 11.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy11p0to16p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy11p0to16p0 --lxySel 11.0 16.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy11p0to16p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy11p0to16p0 --lxySel 11.0 16.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy16p0to50p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy16p0to50p0 --lxySel 16.0 50.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy16p0to50p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy16p0to50p0 --lxySel 16.0 50.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy50p0to110p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy50p0to110p0 --lxySel 50.0 110.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy50p0to110p0_onlyDiMuon/ --inMultiLeg "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 5.0 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix Upsilon_lxy50p0to110p0 --lxySel 50.0 110.0 >& /dev/null &
#
##
#
###
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy0p0to0p2_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy0p0to0p2 --lxySel 0.0 0.2 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy0p0to0p2_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy0p0to0p2_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy0p0to0p2 --lxySel 0.0 0.2 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy0p2to1p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy0p2to1p0 --lxySel 0.2 1.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy0p2to1p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy0p2to1p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy0p2to1p0 --lxySel 0.2 1.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy1p0to2p4_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy1p0to2p4 --lxySel 1.0 2.4 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy1p0to2p4_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy1p0to2p4_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy1p0to2p4 --lxySel 1.0 2.4 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy2p4to3p1_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy2p4to3p1 --lxySel 2.4 3.1 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy2p4to3p1_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy2p4to3p1_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy2p4to3p1 --lxySel 2.4 3.1 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy3p1to11p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy3p1to11p0 --lxySel 3.1 11.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy3p1to11p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy3p1to11p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy3p1to11p0 --lxySel 3.1 11.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy11p0to16p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy11p0to16p0 --lxySel 11.0 16.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy11p0to16p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy11p0to16p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy11p0to16p0 --lxySel 11.0 16.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy16p0to50p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy16p0to50p0 --lxySel 16.0 50.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy16p0to50p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy16p0to50p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy16p0to50p0 --lxySel 16.0 50.0 >& /dev/null &
#
##
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p95to3p25_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass2p5to2p95-3p25to3p4_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass9p0to11p0_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_relaxedSVselection_dimuonMass5p0to9p0-11p0to15p0_lxy50p0to110p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --relaxedSVSel --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy50p0to110p0 --lxySel 50.0 110.0 >& /dev/null &
#
#python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass9p0to11p0_lxy50p0to110p0_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass5p0to9p0-11p0to15p0_lxy50p0to110p0_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" "#Upsilon(nS)" "#Upsilon(nS) sidebands" --dimuonMassSel 2.5 15.0 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi-Upsilon_lxy50p0to110p0 --lxySel 50.0 110.0 >& /dev/null &
#
##
#
###
