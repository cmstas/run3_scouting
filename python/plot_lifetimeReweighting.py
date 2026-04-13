import ROOT
import numpy
import copy
import math
import os,sys
from datetime import date
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#import plotUtils

def getValues(histo):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins)

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")
NORMCONST = 0.01 # To get a 10 fb
doInclusivePlot = False


# Options:
doLimitValidation = False

# Parameters:
sigModel = "BToPhi" # HTo2ZdTo2mu2x  ScenarioB1 BToPhi
thisDir = os.environ.get("PWD")
outDir = ("%s/ctauReweightingValidation_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)

dNames = []
if doInclusivePlot:
    dNames.append("d_FourMu_sep")
    dNames.append("d_FourMu_osv")
    dNames.append("d_Dimuon_lxy0p0to0p2_inclusive")
    dNames.append("d_Dimuon_lxy0p2to1p0_inclusive")
    dNames.append("d_Dimuon_lxy1p0to2p4_inclusive")
    dNames.append("d_Dimuon_lxy2p4to3p1_inclusive")
    dNames.append("d_Dimuon_lxy3p1to7p0_inclusive")
    dNames.append("d_Dimuon_lxy7p0to11p0_inclusive")
    dNames.append("d_Dimuon_lxy11p0to16p0_inclusive")
    dNames.append("d_Dimuon_lxy16p0to70p0_inclusive")
else:
    dNames.append("d_FourMu_sep")
    dNames.append("d_FourMu_osv")
    dNames.append("d_Dimuon_lxy0p0to0p2_iso1_pthigh")
    dNames.append("d_Dimuon_lxy0p2to1p0_iso1_pthigh")
    dNames.append("d_Dimuon_lxy1p0to2p4_iso1_pthigh")
    dNames.append("d_Dimuon_lxy2p4to3p1_iso1_pthigh")
    dNames.append("d_Dimuon_lxy3p1to7p0_iso1_pthigh")
    dNames.append("d_Dimuon_lxy7p0to11p0_iso1_pthigh")
    dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
    dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
    dNames.append("d_Dimuon_lxy0p0to0p2_iso1_ptlow")
    dNames.append("d_Dimuon_lxy0p2to1p0_iso1_ptlow")
    dNames.append("d_Dimuon_lxy1p0to2p4_iso1_ptlow")
    dNames.append("d_Dimuon_lxy2p4to3p1_iso1_ptlow")
    dNames.append("d_Dimuon_lxy3p1to7p0_iso1_ptlow")
    dNames.append("d_Dimuon_lxy7p0to11p0_iso1_ptlow")
    dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow")
    dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow")
    dNames.append("d_Dimuon_lxy0p0to0p2_iso0_pthigh")
    dNames.append("d_Dimuon_lxy0p2to1p0_iso0_pthigh")
    dNames.append("d_Dimuon_lxy1p0to2p4_iso0_pthigh")
    dNames.append("d_Dimuon_lxy2p4to3p1_iso0_pthigh")
    dNames.append("d_Dimuon_lxy3p1to7p0_iso0_pthigh")
    dNames.append("d_Dimuon_lxy7p0to11p0_iso0_pthigh")
    dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh")
    dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh")
    dNames.append("d_Dimuon_lxy0p0to0p2_iso0_ptlow")
    dNames.append("d_Dimuon_lxy0p2to1p0_iso0_ptlow")
    dNames.append("d_Dimuon_lxy1p0to2p4_iso0_ptlow")
    dNames.append("d_Dimuon_lxy2p4to3p1_iso0_ptlow")
    dNames.append("d_Dimuon_lxy3p1to7p0_iso0_ptlow")
    dNames.append("d_Dimuon_lxy7p0to11p0_iso0_ptlow")
    dNames.append("d_Dimuon_lxy11p0to16p0_iso0_ptlow")
    dNames.append("d_Dimuon_lxy16p0to70p0_iso0_ptlow")
    dNames.append("d_Dimuon_lxy0p0to0p2_non-pointing")
    dNames.append("d_Dimuon_lxy0p2to1p0_non-pointing")
    dNames.append("d_Dimuon_lxy1p0to2p4_non-pointing")
    dNames.append("d_Dimuon_lxy2p4to3p1_non-pointing")
    dNames.append("d_Dimuon_lxy3p1to7p0_non-pointing")
    dNames.append("d_Dimuon_lxy7p0to11p0_non-pointing")
    dNames.append("d_Dimuon_lxy11p0to16p0_non-pointing")
    dNames.append("d_Dimuon_lxy16p0to70p0_non-pointing")

years = []
#years.append("2022")
years.append("2023")

ROOT.gStyle.SetOptStat(0)

# Inputs:
#inDir  = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Nov-11-2024_ctauReweighting_fixed/" # 2022
#inDir  = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/"
inDir  = "/home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Final/run3_scouting/"
#
tocompare = {}

if sigModel == "BToPhi":
    tocompare["1.25GeV_1.0mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-1.00mm_2023BPix_2023_0.root",
                                            ],
                                    "name": "Signal_BToPhi_MPhi-1p25_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-1p25_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-1p25_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-1p25_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-1p25_ctau-1.00mm",
                                    "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                    "color" : "r"
                                },
                        ]
    tocompare["1.25GeV_0.1mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-0.10mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-0.10mm_2023BPix_2023_0.root",
                                            ],
                                    "name": "Signal_BToPhi_MPhi-1p25_ctau-0.10mm",
                                    "legend" : r"$c\tau$ = 0.1 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-1p25_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-1p25_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-1p25_ctau-0.10mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-1p25_ctau-0.10mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-1p25_ctau-0.10mm",
                                    "legend" : r"$c\tau'$ = 0.1 mm (reweighted from $c\tau$ = 1 mm)",
                                    "color" : "r"
                                },
                        ]

    tocompare["2.00GeV_1.0mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-1.00mm_2023BPix_2023_0.root",
                                            ],
                                    "name": "Signal_BToPhi_MPhi-2p00_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-2p00_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-2p00_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-2p00_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-2p00_ctau-1.00mm",
                                    "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                    "color" : "r"
                                },
                        ]
    tocompare["2.00GeV_0.1mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-0.10mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-0.10mm_2023BPix_2023_0.root",
                                            ],
                                    "name": "Signal_BToPhi_MPhi-2p00_ctau-0.10mm",
                                    "legend" : r"$c\tau$ = 0.1 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_original/histograms_Signal_BToPhi_MPhi-2p00_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-2p00_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-2p00_ctau-0.10mm_2023_2023_0.root",
                                            "outputHistograms_Oct-1-2025_2023_BToPhi_reweighted/histograms_Signal_BToPhi_MPhi-2p00_ctau-0.10mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_BToPhi_MPhi-2p00_ctau-0.10mm",
                                    "legend" : r"$c\tau'$ = 0.1 mm (reweighted from $c\tau$ = 1 mm)",
                                    "color" : "r"
                                },
                        ]


if sigModel == "ScenarioA":

    tocompare["10.00GeV_2.00GeV_1.0mm"] = [   
                                {
                                    "file" :  [
    #                                        "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
    #                                        "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
    #                                        "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-10_MA-2p00_ctau-1.00mm",
                                    "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                    "color" : "r"
                                },
                        ]
    tocompare["10.00GeV_2.00GeV_10.0mm"] = [   
                                {
                                    "file" :  [
    #                                        "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
    #                                        "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-100.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-100.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-100.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-100.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-100.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-10_MA-2p00_ctau-100.00mm",
                                    "legend" : r"$c\tau$ = 100 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
    #                                        "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-10_MA-2p00_ctau-10.00mm",
                                    "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                                    "color" : "r"
                                },
                        ]

    tocompare["2.00GeV_0.67GeV_1.0mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1.0 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm",
                                    "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                    "color" : "r"
                                },
                        ]
    tocompare["2.00GeV_0.67GeV_10.0mm"] = [   
                                {
                                    "file" :  [
#                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
#                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-100.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-100.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-100.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-100.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-100.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-2_MA-0p67_ctau-100.00mm",
                                    "legend" : r"$c\tau$ = 100 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
#                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2023_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm",
                                    "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                                    "color" : "r"
                                },
                        ]
    tocompare["4.00GeV_1.33GeV_1.0mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2022_2022_0.root",
#                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2022postEE_2022_0.root",
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2023_2023_0.root"
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm",
                                    "legend" : r"$c\tau$ = 1.0 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022_2022_0.root",
#                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022postEE_2022_0.root",
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2023_2023_0.root"
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2022_2022_0.root",
#                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2022postEE_2022_0.root",
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2023_2023_0.root"
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-4_MA-1p33_ctau-1.00mm",
                                    "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                    "color" : "r"
                                },
                        ]

    tocompare["4.00GeV_1.33GeV_10.0mm"] = [   
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2023_2023_0.root"
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm",
                                    "legend" : r"$c\tau$ = 10 mm (original)",
                                    "color" : "b"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-100.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-100.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-100.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-100.00mm_2023_2023_0.root"
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_original/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-100.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-4_MA-1p33_ctau-100.00mm",
                                    "legend" : r"$c\tau$ = 100 mm (original)",
                                    "color" : "g"
                                },
                                {
                                    "file" :  [
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2022_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022postEE_2022_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2022postEE_2023_0.root",
                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2023_2023_0.root"
#                                            "outputHistograms_Jun-21-2025_2023_DQCD_reweighting/histograms_Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm_2023BPix_2023_0.root"
                                            ],
                                    "name": "Signal_ScenarioA_Mpi-4_MA-1p33_ctau-10.00mm",
                                    "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                                    "color" : "r"
                                },
                        ]


#tocompare["4.90GeV_1.0mm"] = [   
#                            {
#                                "file" :  [
#                                        "ScenarioA-original/histograms_Signal_ScenarioA_Mpi-10_MA-4p90_ctau-1.00mm_2023_2023_0.root"
#                                        ],
#                                "name": "Signal_ScenarioA_Mpi-10_MA-4p90_ctau-1mm",
#                                "legend" : r"$c\tau$ = 1.0 mm (original)",
#                                "color" : "b"
#                            },
#                            {
#                                "file" :  [
#                                        "ScenarioA-original/histograms_Signal_ScenarioA_Mpi-10_MA-4p90_ctau-10.00mm_2023_2023_0.root"
#                                        ],
#                                "name": "Signal_ScenarioA_Mpi-10_MA-4p90_ctau-10mm",
#                                "legend" : r"$c\tau$ = 10 mm (original)",
#                                "color" : "g"
#                            },
#                            {
#                                "file" :  [
#                                        "ScenarioA-reweight/histograms_Signal_ScenarioA_Mpi-10_MA-4p90_ctau-1.00mm_2023_2023_0.root"
#                                        ],
#                                "name": "Signal_ScenarioA_Mpi-10_MA-4p90_ctau-1mm",
#                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
#                                "color" : "r"
#                            },
#                    ]
#
#tocompare["2.0GeV_1mm"] = [   
#                            {
#                                "file" :  [
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2022_2022_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2022postEE_2022_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2022postEE_2023_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2023_2023_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2023BPix_2023_0.root"
#                                        ],
#                                "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1mm",
#                                "legend" : r"$c\tau$ = 1 mm (original)",
#                                "color" : "b"
#                            },
#                            {
#                                "file" :  [
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10.00mm_2022_2022_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10.00mm_2022postEE_2022_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10.00mm_2022postEE_2023_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10.00mm_2023_2023_0.root",
#                                        "mass2-original/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10.00mm_2023BPix_2023_0.root"
#                                        ],
#                                "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm",
#                                "legend" : r"$c\tau$ = 10 mm (original)",
#                                "color" : "g"
#                            },
#                            {
#                                "file" :  [
#                                        "mass2-reweight/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2022_2022_0.root",
#                                        "mass2-reweight/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2022postEE_2022_0.root",
#                                        "mass2-reweight/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2022postEE_2023_0.root",
#                                        "mass2-reweight/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2023_2023_0.root",
#                                        "mass2-reweight/histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1.00mm_2023BPix_2023_0.root"
#                                        ],
#                                "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1mm",
#                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
#                                "color" : "r"
#                            },
#                    ]
"""
tocompare["1.5GeV_1mm"] = [   
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1mm",
                                "legend" : r"$c\tau$ = 1 mm (original)",
                                "color" : "b"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm",
                                "legend" : r"$c\tau$ = 10 mm (original)",
                                "color" : "g"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1mm",
                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                "color" : "r"
                            },
                    ]
tocompare["5GeV_1mm"] = [   
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1mm",
                                "legend" : r"$c\tau$ = 1 mm (original)",
                                "color" : "b"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10mm",
                                "legend" : r"$c\tau$ = 10 mm (original)",
                                "color" : "g"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-1mm",
                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                "color" : "r"
                            },
                    ]
tocompare["8GeV_1mm"] = [   
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1mm",
                                "legend" : r"$c\tau$ = 1 mm (original)",
                                "color" : "b"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm",
                                "legend" : r"$c\tau$ = 10 mm (original)",
                                "color" : "g"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1mm",
                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                "color" : "r"
                            },
                    ]
tocompare["14GeV_1mm"] = [   
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm",
                                "legend" : r"$c\tau$ = 1 mm (original)",
                                "color" : "b"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm",
                                "legend" : r"$c\tau$ = 10 mm (original)",
                                "color" : "g"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm",
                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                "color" : "r"
                            },
                    ]
tocompare["22GeV_1mm"] = [   
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1mm",
                                "legend" : r"$c\tau$ = 1 mm (original)",
                                "color" : "b"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm",
                                "legend" : r"$c\tau$ = 10 mm (original)",
                                "color" : "g"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1mm",
                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                "color" : "r"
                            },
                    ]
tocompare["40GeV_1mm"] = [   
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1mm",
                                "legend" : r"$c\tau$ = 1 mm (original)",
                                "color" : "b"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-10.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-10.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_or/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-10.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-10mm",
                                "legend" : r"$c\tau$ = 10 mm (original)",
                                "color" : "g"
                            },
                            {
                                "file" :  [
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm_2022postEE_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm_2023_2023_0.root",
                                        "outputHistograms_Dec-18-2024_2023_40GeV_reweighting_re/histograms_Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1.00mm_2023BPix_2023_0.root"
                                        ],
                                "name": "Signal_HTo2ZdTo2mu2x_MZd-40p0_ctau-1mm",
                                "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                                "color" : "r"
                            },
                    ]
########
tocompare["1.5GeV_1mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1mm",
                        "legend" : r"$c\tau$ = 1 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-1.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10To1.0mm",
                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                        "color" : "r"}
                    ]
tocompare["1.5GeV_10mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-100mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-100mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-100mm",
                        "legend" : r"$c\tau$ = 100 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-10.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-1p5_ctau-100To10.0mm",
                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                        "color" : "r"}
                    ]
#
tocompare["6GeV_1mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1mm",
                        "legend" : r"$c\tau$ = 1 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10To1.0mm",
                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                        "color" : "r"}
                    ]
tocompare["6GeV_10mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100mm",
                        "legend" : r"$c\tau$ = 100 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100To10.0mm",
                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                        "color" : "r"}
                    ]
#
tocompare["8GeV_1mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1mm",
                        "legend" : r"$c\tau$ = 1 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-1.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10To1.0mm",
                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                        "color" : "r"}
                    ]
tocompare["8GeV_10mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-100mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-100mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-100mm",
                        "legend" : r"$c\tau$ = 100 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-10.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-8p0_ctau-100To10.0mm",
                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                        "color" : "r"}
                    ]
#
tocompare["14GeV_1mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm",
                        "legend" : r"$c\tau$ = 1 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10To1.0mm",
                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                        "color" : "r"}
                    ]
tocompare["14GeV_10mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100mm",
                        "legend" : r"$c\tau$ = 100 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100To10.0mm",
                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                        "color" : "r"}
                    ]
#
tocompare["22GeV_1mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1mm",
                        "legend" : r"$c\tau$ = 1 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-1.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10To1.0mm",
                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
                        "color" : "r"}
                    ]
tocompare["22GeV_10mm"] = [   {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm_2022postEE_2022_0.root",
                                          "histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10mm",
                        "legend" : r"$c\tau$ = 10 mm (original)",
                        "color" : "b"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-100mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-100mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-100mm",
                        "legend" : r"$c\tau$ = 100 mm (original)",
                        "color" : "g"},
                        {"file" : ["histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10.00mm_2022postEE_2022_0.root",
                                   "histograms_Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-10.00mm_2022_2022_0.root"],
                        "name": "Signal_HTo2ZdTo2mu2x_MZd-22p0_ctau-100To10.0mm",
                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
                        "color" : "r"}
                    ]
"""
#
#tocompare["2GeV_10mm"] = [   {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm",
#                        "legend" : r"$c\tau$ = 10 mm (original)",
#                        "color" : "b"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-100mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-100mm",
#                        "legend" : r"$c\tau$ = 100 mm (original)",
#                        "color" : "g"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-100To10.0mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-100To10.0mm",
#                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
#                        "color" : "r"}
#                    ]
#tocompare["2GeV_1mm"] = [   {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-1mm",
#                        "legend" : r"$c\tau$ = 1 mm (original)",
#                        "color" : "b"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm",
#                        "legend" : r"$c\tau$ = 10 mm (original)",
#                        "color" : "g"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10To1.0mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10To1.0mm",
#                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
#                        "color" : "r"}
#                    ]
#tocompare["6GeV_10mm"] = [   {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm",
#                        "legend" : r"$c\tau$ = 10 mm (original)",
#                        "color" : "b"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100mm",
#                        "legend" : r"$c\tau$ = 100 mm (original)",
#                        "color" : "g"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10.00mm_2022postEE_2022_fixed2.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-100To10.0mm",
#                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
#                        "color" : "r"}
#                    ]
#tocompare["6GeV_1mm"] = [   {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-1mm",
#                        "legend" : r"$c\tau$ = 1 mm (original)",
#                        "color" : "b"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10mm",
#                        "legend" : r"$c\tau$ = 10 mm (original)",
#                        "color" : "g"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10To1.0mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-6p0_ctau-10To1.0mm",
#                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
#                        "color" : "r"}
#                    ]
#tocompare["14GeV_10mm"] = [   {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm",
#                        "legend" : r"$c\tau$ = 10 mm (original)",
#                        "color" : "b"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100mm",
#                        "legend" : r"$c\tau$ = 100 mm (original)",
#                        "color" : "g"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100To10.0mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100To10.0mm",
#                        "legend" : r"$c\tau'$ = 10 mm (reweighted from $c\tau$ = 100 mm)",
#                        "color" : "r"}
#                    ]
#tocompare["14GeV_1mm"] = [   {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1mm",
#                        "legend" : r"$c\tau$ = 1 mm (original)",
#                        "color" : "b"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10mm",
#                        "legend" : r"$c\tau$ = 10 mm (original)",
#                        "color" : "g"},
#                        {"file" : "histograms_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10To1.0mm_2022postEE_2022_0.root",
#                        "name": "Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10To1.0mm",
#                        "legend" : r"$c\tau'$ = 1 mm (reweighted from $c\tau$ = 10 mm)",
#                        "color" : "r"}
#                    ]
#
# (Only for limit validation)
limitDir = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Nov-11-2024_2022_reweightingValidation/'
limit = {} # 0 = original, 1 = reweighted
limit[r"m = 1.5 GeV, $c\tau = 1$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m1.500_ctau1.00_2022.txt',
                                         limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m1.500_ctau91.00_2022.txt']
limit[r"m = 1.5 GeV, $c\tau = 10$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m1.500_ctau10.00_2022.txt',
                                          limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m1.500_ctau910.00_2022.txt']
limit[r"m = 6.0 GeV, $c\tau = 1$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m6.000_ctau1.00_2022.txt',
                                         limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m6.000_ctau91.00_2022.txt']
limit[r"m = 6.0 GeV, $c\tau = 10$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m6.000_ctau10.00_2022.txt',
                                          limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m6.000_ctau910.00_2022.txt']
limit[r"m = 8.0 GeV, $c\tau = 1$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m8.000_ctau1.00_2022.txt',
                                         limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m8.000_ctau91.00_2022.txt']
limit[r"m = 8.0 GeV, $c\tau = 10$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m8.000_ctau10.00_2022.txt',
                                          limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m8.000_ctau910.00_2022.txt']
limit[r"m = 14.0 GeV, $c\tau = 1$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m14.000_ctau1.00_2022.txt',
                                          limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m14.000_ctau91.00_2022.txt']
limit[r"m = 14.0 GeV, $c\tau = 10$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m14.000_ctau10.00_2022.txt',
                                           limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m14.000_ctau910.00_2022.txt']
limit[r"m = 22.0 GeV, $c\tau = 1$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m22.000_ctau1.00_2022.txt',
                                          limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m22.000_ctau91.00_2022.txt']
limit[r"m = 22.0 GeV, $c\tau = 10$ mm"] = [limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m22.000_ctau10.00_2022.txt',
                                           limitDir + 'lim_asymptotic_HTo2ZdTo2mu2x_m22.000_ctau910.00_2022.txt']



## Loop to make the plots
for y in years:
    #
    for plot in tocompare.keys():
        hsigs = []
        hsigsRaw = []
        legLabels = []
        colors = []
        #
        for signal in tocompare[plot]:
            #legLabels.append(r"$h\rightarrow Z_{D}Z_{D}$, $m_{Z_D} = $%s GeV, $c\tau =$ %s mm"%(str(m), str(t)))
            hsigs.append(ROOT.TH1F(signal["name"], "", len(dNames), 0, len(dNames)))
            hsigsRaw.append(ROOT.TH1F(signal["name"]+"_raw", "", len(dNames), 0, len(dNames)))
            colors.append(signal["color"])
            legLabels.append(signal["legend"])
            for f in signal["file"]:
                file_ = ROOT.TFile.Open("%s/%s"%(inDir,f))
                #
                for d_,d in enumerate(dNames):               
                    #print("Analyzing %s, in region %s"%(signal["name"], d))
                    dataset = file_.Get(d)
                    binidx=-1
                    if d=="d_FourMu_sep":
                        binidx=1
                    elif d=="d_FourMu_osv":
                        binidx=2
                    elif d=="d_Dimuon_lxy0p0to0p2_iso0_ptlow":
                        binidx=3
                    elif d=="d_Dimuon_lxy0p0to0p2_iso0_pthigh":
                        binidx=4
                    elif d=="d_Dimuon_lxy0p0to0p2_iso1_ptlow":
                        binidx=5
                    elif d=="d_Dimuon_lxy0p0to0p2_iso1_pthigh":
                        binidx=6
                    elif d=="d_Dimuon_lxy0p2to1p0_iso0_ptlow":
                        binidx=7
                    elif d=="d_Dimuon_lxy0p2to1p0_iso0_pthigh":
                        binidx=8
                    elif d=="d_Dimuon_lxy0p2to1p0_iso1_ptlow":
                        binidx=9
                    elif d=="d_Dimuon_lxy0p2to1p0_iso1_pthigh":
                        binidx=10
                    elif d=="d_Dimuon_lxy1p0to2p4_iso0_ptlow":
                        binidx=11
                    elif d=="d_Dimuon_lxy1p0to2p4_iso0_pthigh":
                        binidx=12
                    elif d=="d_Dimuon_lxy1p0to2p4_iso1_ptlow":
                        binidx=13
                    elif d=="d_Dimuon_lxy1p0to2p4_iso1_pthigh":
                        binidx=14
                    elif d=="d_Dimuon_lxy2p4to3p1_iso0_ptlow":
                        binidx=15
                    elif d=="d_Dimuon_lxy2p4to3p1_iso0_pthigh":
                        binidx=16
                    elif d=="d_Dimuon_lxy2p4to3p1_iso1_ptlow":
                        binidx=17
                    elif d=="d_Dimuon_lxy2p4to3p1_iso1_pthigh":
                        binidx=18
                    elif d=="d_Dimuon_lxy3p1to7p0_iso0_ptlow":
                        binidx=19
                    elif d=="d_Dimuon_lxy3p1to7p0_iso0_pthigh":
                        binidx=20
                    elif d=="d_Dimuon_lxy3p1to7p0_iso1_ptlow":
                        binidx=21
                    elif d=="d_Dimuon_lxy3p1to7p0_iso1_pthigh":
                        binidx=22
                    elif d=="d_Dimuon_lxy7p0to11p0_iso0_ptlow":
                        binidx=23
                    elif d=="d_Dimuon_lxy7p0to11p0_iso0_pthigh":
                        binidx=24
                    elif d=="d_Dimuon_lxy7p0to11p0_iso1_ptlow":
                        binidx=25
                    elif d=="d_Dimuon_lxy7p0to11p0_iso1_pthigh":
                        binidx=26
                    elif d=="d_Dimuon_lxy11p0to16p0_iso0_ptlow":
                        binidx=27
                    elif d=="d_Dimuon_lxy11p0to16p0_iso0_pthigh":
                        binidx=28
                    elif d=="d_Dimuon_lxy11p0to16p0_iso1_ptlow":
                        binidx=29
                    elif d=="d_Dimuon_lxy11p0to16p0_iso1_pthigh":
                        binidx=30
                    elif d=="d_Dimuon_lxy16p0to70p0_iso0_ptlow":
                        binidx=31
                    elif d=="d_Dimuon_lxy16p0to70p0_iso0_pthigh":
                        binidx=32
                    elif d=="d_Dimuon_lxy16p0to70p0_iso1_ptlow":
                        binidx=33
                    elif d=="d_Dimuon_lxy16p0to70p0_iso1_pthigh":
                        binidx=34
                    elif d=="d_Dimuon_lxy0p0to0p2_non-pointing":
                        binidx=35
                    elif d=="d_Dimuon_lxy0p2to1p0_non-pointing":
                        binidx=36
                    elif d=="d_Dimuon_lxy1p0to2p4_non-pointing":
                        binidx=37
                    elif d=="d_Dimuon_lxy2p4to3p1_non-pointing":
                        binidx=38
                    elif d=="d_Dimuon_lxy3p1to7p0_non-pointing":
                        binidx=39
                    elif d=="d_Dimuon_lxy7p0to11p0_non-pointing":
                        binidx=40
                    elif d=="d_Dimuon_lxy11p0to16p0_non-pointing":
                        binidx=41
                    elif d=="d_Dimuon_lxy16p0to70p0_non-pointing":
                        binidx=42
                    nSig = NORMCONST * dataset.sumEntries()
                    nSigRaw = dataset.numEntries()
                    #print(d, nSig, nSigRaw)
                    hsigs[-1].SetBinContent(d_+1, hsigs[-1].GetBinContent(d_+1) + nSig)
                    hsigsRaw[-1].SetBinContent(d_+1, hsigsRaw[-1].GetBinContent(d_+1) + nSigRaw)
                file_.Close()

        ## Plot        
        print(len(hsigs), len(legLabels))
        plt.style.use(hep.style.CMS)
        #colors = ['#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd']
        #fig, ax = plt.subplots(figsize=(16, 5))
        fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3.5, 1.5], 'hspace': 0.07}, sharex=True, figsize=(16, 7))
        fig.subplots_adjust(bottom=0.2, left = 0.1, right=0.78)
        luminosity = 35 if y=='2022' else 27
        luminosity = 62 # hardcoded and to be removed
        hep.cms.label("Preliminary", data=False, lumi=luminosity, com='13.6', ax=ax)
        #fig.text(0.35, 0.9, r'$m_{4\mu} = $125 GeV, $m_{2\mu} =$ %s GeV'%(str(m)), color='black', fontsize = 13)
        ax.set_ylabel(r'Events / Search Region', fontsize=20)
        ### Signal
        for h_,h in enumerate(hsigs):
            print(colors[h_], legLabels[h_], h.GetName())
            mh, mbins = getValues(h)
            mhr, mrbins = getValues(hsigsRaw[h_])
            if "To" in h.GetName().split('ctau')[1]:
                linestyle = '--'
            else:
                linestyle = '-'
            hep.histplot(
                mh,
                bins=mbins,
                color=colors[h_],
                histtype="step",
                label=legLabels[h_],
                linestyle=linestyle,
                ax=ax
            )
            bin_centers = 0.5 * (mbins[1:] + mbins[:-1])
            errors = np.sqrt(mhr)/mhr*mh
            ax.errorbar(bin_centers, mh, yerr=errors, fmt='', linestyle='none', color=colors[h_])
            if h_==0:
                den = mh
                denErr = errors
            if h_==2:
                num = mh
                numErr = errors
        ax.set_xlim(0, 42)
        # Ratio
        ratio = num/den
        eratio = ratio * np.sqrt((denErr / den) ** 2 + (numErr / num) ** 2)
        ax_ratio.errorbar(bin_centers, ratio, yerr=eratio, fmt='o', linestyle='none', color='k')
        ax_ratio.axhline(y=1, color='gray', linestyle='-', linewidth=1)
        ax_ratio.set_ylim(0.5, 1.5)
        # If we want it in log scale
        #ax.set_ylim(max(0.8*min(mh), 0.1), 30.0*max(mh))
        #ax.set_yscale('log')
        if doInclusivePlot:
            print("not doing anything")
            ax.set_xlim(0, 10)
        else:
            ax.axvline(x=2, color='gray', linestyle='--', linewidth=1)
            ax.axvline(x=10, color='gray', linestyle='--', linewidth=1)
            ax.axvline(x=18, color='gray', linestyle='--', linewidth=1)
            ax.axvline(x=26, color='gray', linestyle='--', linewidth=1)
            ax.axvline(x=34, color='gray', linestyle='--', linewidth=1)
            ax.text(0.6, 1.4*max(mh), r'$4\mu$', color='gray', fontsize = 9)
            ax.text(2.5, 1.4*max(mh), r'Pointing, isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
            ax.text(10.5, 1.4*max(mh), r'Pointing, isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
            ax.text(18.5, 1.4*max(mh), r'Pointing, non-isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
            ax.text(26.5, 1.4*max(mh), r'Pointing, non-isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
            ax.text(34.5, 1.4*max(mh), r'Non-pointing', color='gray', fontsize = 8)
        ax.set_ylim(0, 1.5*max(mh))
        ## x axis:
        nCategories = 1 if doInclusivePlot else 5
        ax.set_xlabel('')
        x_ticks = [0.0, 1.0]
        x_labels = ['Multivertex', 'Overlapping']
        for x in range(0, nCategories):
            x_ticks.append(x*8+0.+2)
            x_ticks.append(x*8+0.+3)
            x_ticks.append(x*8+0.+4)
            x_ticks.append(x*8+0.+5)
            x_ticks.append(x*8+0.+6)
            x_ticks.append(x*8+0.+7)
            x_ticks.append(x*8+0.+8)
            x_ticks.append(x*8+0.+9)
            x_labels.append(r'$l_{xy} \in [0.0, 0.2]$ cm')
            x_labels.append(r'$l_{xy} \in [0.2, 1.0]$ cm')
            x_labels.append(r'$l_{xy} \in [1.0, 2.4]$ cm')
            x_labels.append(r'$l_{xy} \in [2.4, 3.1]$ cm')
            x_labels.append(r'$l_{xy} \in [3.1, 7.0]$ cm')
            x_labels.append(r'$l_{xy} \in [7.0, 11.0]$ cm')
            x_labels.append(r'$l_{xy} \in [11.0, 16.0]$ cm')
            x_labels.append(r'$l_{xy} \in [16.0, 70.0]$ cm')
        ax.set_xticks(x_ticks)
        ax_ratio.set_xticks(x_ticks)
        ax_ratio.set_xticklabels(x_labels, ha = 'left', rotation=-45, fontsize = 10)
        #ax.xaxis.set_minor_locator(MultipleLocator(0.0))
        ax.minorticks_off()
        ## Legend
        if "HTo2ZdTo2mu2x" in sigModel:
            mass = float(plot.split("GeV")[0])
        if "BToPhi" in sigModel:
            mass = float(plot.split("GeV")[0])
        elif "Scenario" in sigModel:
            mass = float(plot.split("GeV")[0])
            mass4 = float(plot.split("GeV")[1][1:])
        if "HTo2ZdTo2mu2x" in sigModel:
            legend = ax.legend(loc='upper left', fontsize = 10, frameon = True, bbox_to_anchor=(1.02, 1), borderaxespad=0., title=r'$h\rightarrow Z_D Z_D$,  $m_{Z_D} = $%.1f GeV  ($\sigma = %i$ fb)'%(mass, 1000*NORMCONST), title_fontsize=11)
        elif "ScenarioA" in sigModel:
            legend = ax.legend(loc='upper left', fontsize = 10, frameon = True, bbox_to_anchor=(1.02, 1), borderaxespad=0., title=r'Scenario A,  $m_{\pi} = $%.1f GeV, $m_{A} = $%.1f GeV  ($\sigma = %i$ fb)'%(mass4, mass, 1000*NORMCONST), title_fontsize=11)
        elif "BToPhi" in sigModel:
            legend = ax.legend(loc='upper left', fontsize = 10, frameon = True, bbox_to_anchor=(1.02, 1), borderaxespad=0., title=r'$B\rightarrow\phi X$,  $m_{\phi} = $%.2f GeV'%(mass), title_fontsize=11)
        legend.get_title().set_ha('left') 
        legend.get_title().set_weight('bold')
        ## Save
        fig.savefig('%s/ctVal_%s_%s.png'%(outDir, plot, y), dpi=140)

if doLimitValidation:
    ros = []
    rosup = []
    rosdown = []
    rws = []
    rwsup = []
    rwsdown = []
    for lim in limit.keys():
        with open(limit[lim][0], 'r') as f:
            for ll in f.readlines():
                if "Expected 50" in ll:
                    ros.append( float(ll.split()[len(ll.split())-1]) )
                if "Expected 84" in ll:
                    rosup.append( float(ll.split()[len(ll.split())-1]) )
                if "Expected 16" in ll:
                    rosdown.append( float(ll.split()[len(ll.split())-1]) )
        with open(limit[lim][1], 'r') as f:
            for ll in f.readlines():
                if "Expected 50" in ll:
                    rws.append( float(ll.split()[len(ll.split())-1]) )
                if "Expected 84" in ll:
                    rwsup.append( float(ll.split()[len(ll.split())-1]) )
                if "Expected 16" in ll:
                    rwsdown.append( float(ll.split()[len(ll.split())-1]) )
    #fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.07}, sharex=True, figsize=(10, 10))
    fig, ax = plt.subplots(1, figsize=(10, 8))
    hep.cms.label("Preliminary", data=True, lumi=luminosity, year=y, com='13.6', ax=ax)
    axis = np.linspace(0, len(limit)-1, len(limit.keys())) + 0.5
    #
    ax.set_ylabel("95% CL upper limit on r")
    #ax.errorbar(axis, np.array(ros), fmt='o', xerr=0.5, yerr=[rosdown,rosup], linestyle='none', color='b', label='Original')
    ax.errorbar(axis, np.array(ros), fmt='o', xerr=0.5, linestyle='none', color='b', label='Original')
    ax.fill_between(np.arange(len(limit)+1), np.append(np.array(ros) - np.array(rosdown),np.array(ros)[-1]), np.append(np.array(ros) + np.array(rosup),np.array(ros)[-1]), color='b', alpha=0.2, label="$\pm 1\sigma$ (original)", step="post")
    #ax.errorbar(axis, np.array(rws), fmt='o', xerr=0.5, yerr=[rwsdown,rwsup], linestyle='none', color='r', label='Reweighted')
    ax.errorbar(axis, np.array(rws), fmt='o', xerr=0.5, linestyle='none', color='r', label='Reweighted')
    ax.fill_between(np.arange(len(limit)+1), np.append(np.array(rws) - np.array(rwsdown),np.array(rws)[-1]), np.append(np.array(rws) + np.array(rwsup),np.array(rws)[-1]), color='r', alpha=0.2, label="$\pm 1\sigma$ (reweighted)", step="post")
    ax.set_ylim(0, 2.5)
    ax.legend(loc='best', fontsize = 14, frameon = True)
    #ax.set_xlim(0, axis[-1]+0.5)
    ax.set_xticks(axis - 0.5)
    ax.minorticks_off()
    ax.set_xticklabels(len(limit)*[' '], ha = 'center', rotation=-10, fontsize = 15)
    for x_,xv in enumerate(axis):
        ax.text(xv, -0.1, list(limit.keys())[x_].split(', ')[0].split('= ')[1], fontsize = 9, ha='center')
        ax.text(xv, -0.2, list(limit.keys())[x_].split(', ')[1].split('= ')[1].replace('$', ''), fontsize = 9, ha='center')
    #
    #ax_ratio.set_xlim(0, axis[-1]+0.5)
    #ax_ratio.set_xticks(axis)
    #ax_ratio.minorticks_off()
    #ax_ratio.set_xticklabels(limit.keys(), ha = 'center', rotation=-10, fontsize = 14)
    fig.savefig('%s/validation.png'%(outDir), dpi=140)
