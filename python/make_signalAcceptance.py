import ROOT
import numpy
import copy
import os,sys,csv
from datetime import date
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator, FixedFormatter
import plotly.graph_objects as go
import pickle
#import plotUtils

def getValues(histo):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins)

legData = {}
legData["d_Dimuon_full_inclusive"] = r'Inclusive'
legData["d_Dimuon_lxy0p0to0p2_inclusive"] = r'$0.0 < l_{xy} < 0.2 $ cm'
legData["d_Dimuon_lxy0p2to1p0_inclusive"] = r'$0.2 < l_{xy} < 1.0 $ cm'
legData["d_Dimuon_lxy1p0to2p4_inclusive"] = r'$1.0 < l_{xy} < 2.4 $ cm'
legData["d_Dimuon_lxy2p4to3p1_inclusive"] = r'$2.4 < l_{xy} < 3.1 $ cm'
legData["d_Dimuon_lxy3p1to7p0_inclusive"] = r'$3.1 < l_{xy} < 7 $ cm'
legData["d_Dimuon_lxy7p0to11p0_inclusive"] = r'$7.0 < l_{xy} < 11.0 $ cm'
legData["d_Dimuon_lxy11p0to16p0_inclusive"] = r'$11.0 < l_{xy} < 16.0 $ cm'
legData["d_Dimuon_lxy16p0to70p0_inclusive"] = r'$16.0 < l_{xy} < 70.0 $ cm'
legData["d_Dimuon_lxy0p0to0p2_iso1_pthigh"] = r'$0.0 < l_{xy} < 0.2 $ cm (isohigh)'
legData["d_Dimuon_lxy0p2to1p0_iso1_pthigh"] = r'$0.2 < l_{xy} < 1.0 $ cm (isohigh)'
legData["d_Dimuon_lxy1p0to2p4_iso1_pthigh"] = r'$1.0 < l_{xy} < 2.4 $ cm (isohigh)'
legData["d_Dimuon_lxy2p4to3p1_iso1_pthigh"] = r'$2.4 < l_{xy} < 3.1 $ cm (isohigh)'
legData["d_Dimuon_lxy3p1to7p0_iso1_pthigh"] = r'$3.1 < l_{xy} < 7 $ cm (isohigh)'
legData["d_Dimuon_lxy7p0to11p0_iso1_pthigh"] = r'$7.0 < l_{xy} < 11.0 $ cm (isohigh)'
legData["d_Dimuon_lxy11p0to16p0_iso1_pthigh"] = r'$11.0 < l_{xy} < 16.0 $ cm (isohigh)'
legData["d_Dimuon_lxy16p0to70p0_iso1_pthigh"] = r'$16.0 < l_{xy} < 70.0 $ cm (isohigh)'
legData["d_Dimuon_lxy0p0to0p2_iso0_pthigh"] = r'$0.0 < l_{xy} < 0.2 $ cm (noisohigh)'
legData["d_Dimuon_lxy0p2to1p0_iso0_pthigh"] = r'$0.2 < l_{xy} < 1.0 $ cm (noisohigh)'
legData["d_Dimuon_lxy1p0to2p4_iso0_pthigh"] = r'$1.0 < l_{xy} < 2.4 $ cm (noisohigh)'
legData["d_Dimuon_lxy2p4to3p1_iso0_pthigh"] = r'$2.4 < l_{xy} < 3.1 $ cm (noisohigh)'
legData["d_Dimuon_lxy3p1to7p0_iso0_pthigh"] = r'$3.1 < l_{xy} < 7 $ cm (noisohigh)'
legData["d_Dimuon_lxy7p0to11p0_iso0_pthigh"] = r'$7.0 < l_{xy} < 11.0 $ cm (noisohigh)'
legData["d_Dimuon_lxy11p0to16p0_iso0_pthigh"] = r'$11.0 < l_{xy} < 16.0 $ cm (noisohigh)'
legData["d_Dimuon_lxy16p0to70p0_iso0_pthigh"] = r'$16.0 < l_{xy} < 70.0 $ cm (noisohigh)'
legData["d_Dimuon_lxy0p0to0p2_non-pointing"] = r'$0.0 < l_{xy} < 0.2 $ cm (np)'
legData["d_Dimuon_lxy0p2to1p0_non-pointing"] = r'$0.2 < l_{xy} < 1.0 $ cm (np)'
legData["d_Dimuon_lxy1p0to2p4_non-pointing"] = r'$1.0 < l_{xy} < 2.4 $ cm (np)'
legData["d_Dimuon_lxy2p4to3p1_non-pointing"] = r'$2.4 < l_{xy} < 3.1 $ cm (np)'
legData["d_Dimuon_lxy3p1to7p0_non-pointing"] = r'$3.1 < l_{xy} < 7 $ cm (np)'
legData["d_Dimuon_lxy7p0to11p0_non-pointing"] = r'$7.0 < l_{xy} < 11.0 $ cm (np)'
legData["d_Dimuon_lxy11p0to16p0_non-pointing"] = r'$11.0 < l_{xy} < 16.0 $ cm (np)'
legData["d_Dimuon_lxy16p0to70p0_non-pointing"] = r'$16.0 < l_{xy} < 70.0 $ cm (np)'
legData["d_FourMu_sep"] = r'Four-muon multivertex'
legData["d_FourMu_osv"] = r'Four-muon overlapping'

#########################

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

doRel = True

wsname = "wfit"
thisDir = os.environ.get("PWD")

is1D = True
useCategorizedSignal = True
useCategorizedBackground = True
doPaperPlot = True
useSignalMC = True
doSystVariations = False
sigModel = "HTo2ZdTo2mu2x" # HTo2ZdTo2mu2x : BToPhi
correctByFilter = False
hepdata_input = True

# Output definition
outDir = ("%s/plotsAcceptance_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)
#
y = 2022
#

# Signal Regions
dNames = []
if doPaperPlot:
    #dNames.append("d_Dimuon_full_inclusive")
    #dNames.append("d_FourMu_sep")
    #dNames.append("d_FourMu_osv")
    dNames.append("d_Dimuon_lxy0p0to0p2_inclusive")
    dNames.append("d_Dimuon_lxy0p2to1p0_inclusive")
    dNames.append("d_Dimuon_lxy1p0to2p4_inclusive")
    dNames.append("d_Dimuon_lxy2p4to3p1_inclusive")
    dNames.append("d_Dimuon_lxy3p1to7p0_inclusive")
    dNames.append("d_Dimuon_lxy7p0to11p0_inclusive")
    dNames.append("d_Dimuon_lxy11p0to16p0_inclusive")
    dNames.append("d_Dimuon_lxy16p0to70p0_inclusive")
    #
    #dNames.append("d_Dimuon_lxy0p0to0p2_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy0p2to1p0_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy1p0to2p4_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy2p4to3p1_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy3p1to7p0_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy7p0to11p0_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
    #dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
    #
    #dNames.append("d_Dimuon_lxy0p0to0p2_non-pointing")
    #dNames.append("d_Dimuon_lxy0p2to1p0_non-pointing")
    #dNames.append("d_Dimuon_lxy1p0to2p4_non-pointing")
    #dNames.append("d_Dimuon_lxy2p4to3p1_non-pointing")
    #dNames.append("d_Dimuon_lxy3p1to7p0_non-pointing")
    #dNames.append("d_Dimuon_lxy7p0to11p0_non-pointing")
    #dNames.append("d_Dimuon_lxy11p0to16p0_non-pointing")
    #dNames.append("d_Dimuon_lxy16p0to70p0_non-pointing")
    correctByFilter = True
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
    correctByFilter = False

# Years
years = []
years.append(2022)
years.append(2023)

eras = {}
eras[2022] = ['2022', '2022postEE']
eras[2023] = ['2023', '2022postEE', '2023BPix']
#eras[2023] = ['2023', '2023BPix']

# Style settings
ROOT.gStyle.SetOptStat(0)
# Colors : ['#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd']
colors = {}
colors['0']     = 'k'
colors['0.1']   = '#832db6'
colors['1']     = '#3f90da'
colors['10']    = '#ffa90e'
colors['100']   = '#bd1f01'
colors['1000']  = '#94a4a2'

# Signals
sigMasses = []
sigCTaus = []
if sigModel=="HTo2ZdTo2mu2x":
    if doPaperPlot:
        sigMasses = [2.0, 5.0, 7.0, 14.0, 20.0, 30.0, 40.0, 50.0]
        sigMasses = [0.5, 0.7, 1.5, 2.0, 5.0, 7.0, 8.0]
        sigMasses = [2.0, 5.0, 12.0, 20.0]
        sigCTaus = [0.1, 0.16, 0.25, 0.40, 0.63, 1.00, 1.60, 2.50, 4.00, 6.30, 10.00, 16.00, 25.00, 40.00, 63.00, 100.00]
        sigCTaus += [160.00, 250.00, 400.00, 630.00, 1000.0]
    else:
        #sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 24.0, 30.0, 40.0, 50.0]
        sigCTaus = [1, 10, 100, 1000]

if sigModel=="BToPhi":
    sigMasses = [0.3, 0.5, 0.6, 0.7, 0.9, 1.25, 1.5, 2.0, 2.85, 3.35, 4.6]
    sigCTaus = [1000]

#
#
## Loop to make the plots
nSignal_perYear = {}
for y in years:
    outFileName = ("%s/plotsAcceptance_"%(thisDir))+today + "/acceptanceSplines_%s_%i.root"%(sigModel,y) # Year is hardcoded
    outFile = ROOT.TFile(outFileName, "RECREATE")
    outFile.Close()
    sy = str(y)
    nSignal_perYear[sy] = {}
    splines = []
    for d_,d in enumerate(dNames):
        #
        nSignal_perYear[sy][d] = np.zeros((len(sigMasses),len(sigCTaus)))
        #
        #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Nov-13-2024_ctauReweighting"
        #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Dec-03-2024_2023_complete"
        #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Dec-03-2024_2022_complete"
        #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Feb-20-2025_2022"
        if y==2022:
            #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Feb-23-2025_2022_HToZdZd_lifetimeReweighting"
            inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Feb-25-2025_allYears"
            #inDir = "/ceph/cms/store/user/fernance/EXO-24-016/BToPhi/Splines/outputHistograms_Sep-22-2025_2022_BToPhi_wB_wPU_RooOnly"
            #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jan-28-2026_allCuts_BToPhi_2022/"
        else:
            #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Feb-23-2025_2023_HToZdZd_lifetimeReweighting"
            inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Feb-25-2025_allYears"
            #inDir = "/ceph/cms/store/user/fernance/EXO-24-016/BToPhi/Splines/outputHistograms_Sep-22-2025_2023_BToPhi_wB_wPU_RooOnly"
            #inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jan-28-2026_allCuts_BToPhi_2023/"
        #
        # Identify bin index
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
        catExtS = ""
        if useCategorizedSignal:
            catExtS = "_ch%d_%i"%(binidx, y)
        #
        # Start making the plot
        plt.style.use(hep.style.CMS)
        fig, ax = plt.subplots(figsize=(11, 10))
        ax.set_ylabel(r'Acceptance $\times$ Efficiency (%)', fontsize=24)
        ax.set_xlabel(r'LLP mass (GeV)', fontsize=24)
        ax.set_xscale('log')
        if y==2022:
            hep.cms.label("Preliminary", data=True, lumi=34.6, year=y, com='13.6')
        else:
            hep.cms.label("Preliminary", data=True, lumi=27.8, year=y, com='13.6')
        title = ''
        if "FourMu_sep" in d:
            fig.text(0.15, 0.7, 'Multivertex four-muon region', color='black', fontsize = 16)
            title = 'Multivertex four-muon region'
        elif "FourMu_osv" in d:
            fig.text(0.15, 0.7, 'Overlapping four-muon vertex region', color='black', fontsize = 16)
            title = 'Overlapping four-muon vertex region'
        else:
            if "non-pointing" in d:
                fig.text(0.15, 0.67, r'Non-pointing dimuons: $0.02 < |\Delta\Phi| < \pi/2$', color='black', fontsize = 16)
                title = r'Non-pointing'
            elif "inclusive" not in d:
                fig.text(0.15, 0.67, r'Pointing dimuons: $|\Delta\Phi| < 0.02$', color='black', fontsize = 16)
                title = r'Pointing'
            if "lxy0p0to0p2" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [0.0, 0.2]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [0.0, 0.2]$ cm'
            elif "lxy0p2to1p0" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [0.2, 1.0]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [0.2, 1,0]$ cm'
            elif "lxy1p0to2p4" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [1.0, 2.4]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [1.0, 2.4]$ cm'
            elif "lxy2p4to3p1" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [2.4, 3.1]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [2.4, 3.1]$ cm'
            elif "lxy3p1to7p0" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [3.1, 7.0]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [3.1, 7.0]$ cm'
            elif "lxy7p0to11p0" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [7.0, 11.0]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [7.0, 11.0]$ cm'
            elif "lxy11p0to16p0" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [11.0, 16.0]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [11.0, 16.0]$ cm'
            elif "lxy16p0to70p0" in d:
                fig.text(0.15, 0.64, r'$l_{xy} \in [16.0, 70.0]$ cm', color='black', fontsize = 16)
                title += r', $l_{xy} \in [16.0, 70.0]$ cm'
            if "iso1" in d:
                fig.text(0.15, 0.61, r'Isolated muons', color='black', fontsize = 16)
                title += r', isolated'
            elif "iso0" in d:
                fig.text(0.15, 0.61, r'Non-isolated muons', color='black', fontsize = 16)
                title += r', non-isolated'
            if "pthigh" in d:
                fig.text(0.15, 0.58, r'$p_{T}^{\mu\mu} > 25$ GeV', color='black', fontsize = 16)
                title += r', $p_{T}^{\mu\mu} > 25$ GeV'
            elif "ptlow" in d:
                fig.text(0.15, 0.58, r'$p_{T}^{\mu\mu} < 25$ GeV', color='black', fontsize = 16)
                title += r', $p_{T}^{\mu\mu} < 25$ GeV'
            if "inclusive" in d:
                title = title[1:]
        if is1D:
            for _t,t in enumerate(sigCTaus):
                acceptance = []
                masses = []
                for _m,m in enumerate(sigMasses):
                    if (sigModel=="HTo2ZdTo2mu2x" and ((m < 1.0 and t > 10) or (m < 1.99 and t > 100))):
                            continue
                    if (sigModel=="HTo2ZdTo2mu2x"):
                        sigTag = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm"%(str(m).replace('.','p'), t)
                    if (sigModel=="BToPhi"):
                        sigTag = "Signal_BToPhi_MPhi-%s_ctau-%.2fmm"%(("%.2f"%(m)).replace('.','p'), t)
                    print("Analyzing %s, in region %s"%(sigTag, d))
                    for e,era in enumerate(eras[y]):
                        finame = "%s/histograms_%s_%s_%i_0.root"%(inDir,sigTag,era,y)
                        # Open input file with workspace
                        f = ROOT.TFile(finame)
                        # Retrieve workspace from file
                        if e==0:
                            dataset = f.Get(d)
                        else:
                            dataset.append(f.Get(d))
                        # Close input file with workspace
                        f.Close()
                    # Retrieve signal normalization
                    print(d)
                    if 'FourMu' not in d:
                        nSig = dataset.sumEntries("%f < mfit && mfit < %f"%(m-0.018*5.0*m, m+0.018*5.0*m))
                        print(dataset.sumEntries("%f < mfit && mfit < %f"%(m-0.018*5.0*m, m+0.018*5.0*m)))
                        #print(dataset.numEntries("%f < mfit && mfit < %f"%(m-0.018*5.0*m, m+0.018*5.0*m)))
                    else:
                        nSig = dataset.sumEntries("%f < m4fit && m4fit < %f"%(125-0.018*5.0*125., 125+0.018*5.0*125.)) # Corrected 
                    ## Manual application of SF:
                    if ('lxy7p0to11p0' in d) or ('lxy11p0to16p0' in d) or ('lxy16p0to70p0' in d):
                        print("Manually applying the scale factor on the most displaced regions")
                        nSig = nSig * 0.82 # Manually applying the scale factor on the most displaced regions
                    ##
                    #efilter = 1.0
                    #if correctByFilter:
                    #    with open('data/hahm-request.csv') as mcinfo:
                    #        reader = csv.reader(mcinfo, delimiter=',')
                    #        for row in reader:
                    #            if "MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t) in row[0]:
                    #            #if "MZd-%s"%(str(m).replace('.','p')) in row[0]:
                    #                efilter = float(row[-1])
                    #                print("EFILTER FOUND")
                    #                break
                    ##
                    if y==2022:
                        acceptance.append(nSig/(1000*35.)) # Nexp / (sigma*L) = A * eff (before L = 35. but correct is 34.627501094)
                    else:
                        acceptance.append(nSig/(1000*26.59)) # Nexp / (sigma*L) = A * eff (before L = 27. but correct is 27.754413924999998)
                    nSignal_perYear[sy][d][_m][_t] = nSig
                    masses.append(m)
                # Graph and acceptance for spline
                if not doPaperPlot:
                    graph = ROOT.TGraph(len(acceptance), np.array(masses), np.array(acceptance))
                    splines.append(ROOT.TSpline3("spline_acceptance_%s_%.2f_%s"%(sigModel,t,d), graph))
                    splines[-1].SetName("spline_acceptance_%s_%.2f_%s"%(sigModel,t,d))
                    acceptance_100 = [100*x for x in acceptance]
                    graph_100 = ROOT.TGraph(len(acceptance_100), np.array(masses), np.array(acceptance_100))
                    spline_100 = ROOT.TSpline3("spline_acceptance_%s_%.2f_%s_100"%(sigModel,t,d), graph_100)
                    if sigModel=="HTo2ZdTo2mu2x":
                        if masses[0] < 1.5:
                            m_interp0 = np.linspace(0.5, 1.5, 100)
                            m_interp1 = np.linspace(1.51, 9.95, 100)
                            m_interp2 = np.linspace(10, masses[-1], 300)
                            m_interp = np.concatenate((m_interp0, m_interp1, m_interp2))
                        elif masses[0] < 30.0:
                            m_interp1 = np.linspace(1.5, 9.95, 100)
                            m_interp2 = np.linspace(10, masses[-1], 300)
                            m_interp = np.concatenate((m_interp1, m_interp2))
                        else:
                            m_interp = np.linspace(30.00, masses[-1], 300)
                    elif sigModel=="BToPhi":
                        m_interp = np.linspace(0.25, 4.6, 200)
                    a_interp = [spline_100.Eval(x) for x in m_interp]
                    # Plot in the canvas
                    if len(sigCTaus) > 5:
                        ax.plot(masses, acceptance_100, label=r'$h\rightarrow Z_{D}Z_{D}$, $c\tau = $%i mm'%(t), color='k', marker='o', linestyle='')
                        ax.plot(m_interp, a_interp, color='k')
                    else:
                        ax.plot(masses, acceptance_100, label=r'$h\rightarrow Z_{D}Z_{D}$, $c\tau = $%i mm'%(t), color=colors[str(t)], marker='o', linestyle='')
                        ax.plot(m_interp, a_interp, color=colors[str(t)])
                    # Save spline
                    outFile = ROOT.TFile.Open(outFileName, "UPDATE")
                    splines[-1].Write()
                    outFile.Close()
            # Hardcoded and to be removed, only for the Scenario B1
            if False:
                for _t,t in enumerate([0.1, 1, 10, 100]):
                    acceptance = []
                    sigTag = "Signal_ScenarioB1_mpi-4_mA-1p33_ctau-%smm"%(str(t).replace('.','p'))
                    print("Analyzing %s, in region %s"%(sigTag, d))
                    print("%s/%s_%s_%i_workspace.root"%(inDir,d,sigTag,y))
                    finame = "%s/%s_%s_%i_workspace.root"%(inDir,d,sigTag,y)
                    # Open input file with workspace
                    f = ROOT.TFile(finame)
                    # Retrieve workspace from file
                    w = f.Get(wsname)
                    # Retrieve signal normalization
                    nSig = w.var("signalNorm%s"%catExtS).getValV()
                    acceptance.append(nSig/(1000*35)) # Nexp / (sigma*L) = A * eff
                    masses.append(m)
                    # Close input file with workspace
                    f.Close()
                    acceptance_100 = [100*x for x in acceptance]
                    ax.plot([1.33], acceptance_100, label=r'Scenario B1 $c\tau = $%s mm'%(str(t)), color=colors[str(t)], marker='x', linestyle='', ms=20)
            ax.legend(loc='upper left', fontsize = 16, frameon = True, ncol=2)
            fig.savefig('%s/acceptance_%s_%s.png'%(outDir, d, y), dpi=140)
            #
        else:
            # If the model is HToZdZd use the "interpolation by sectors"
            if sigModel=="HTo2ZdTo2mu2x":
                ctau_splines = {}
                ctau_data = {}
                ctau_mass = {}
                for _t,t in enumerate(sigCTaus):
                    ctau_data[t] = []
                    ctau_mass[t] = []
                    for m in sigMasses:
                        if (m < 1.0 and t > 10) or (m < 30.0 and t > 100):
                            continue
                        sigTag = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm"%(str(m).replace('.','p'), t)
                        for e,era in enumerate(eras[y]):
                            finame = "%s/histograms_%s_%s_%i_0.root"%(inDir,sigTag,era,y)
                            # Open input file with workspace
                            f = ROOT.TFile(finame)
                            # Retrieve workspace from file
                            if e==0:
                                dataset = f.Get(d)
                            else:
                                dataset.append(f.Get(d))
                            # Close input file with workspace
                            f.Close()
                        # Retrieve signal normalization
                        nSig = dataset.sumEntries("%f < mfit && mfit < %f"%(m-0.018*5.0*m, m+0.018*5.0*m))
                        efilter = 1.0
                        if correctByFilter:
                            with open('data/hahm-request.csv') as mcinfo:
                                reader = csv.reader(mcinfo, delimiter=',')
                                for row in reader:
                                    if "MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t) in row[0]:
                                    #if "MZd-%s"%(str(m).replace('.','p')) in row[0]:
                                        efilter = float(row[-1])
                                        print("EFILTER FOUND")
                                        break
                        ctau_data[t].append(nSig/(1000*35*efilter)) # Nexp / (sigma*L) = A * eff
                        ctau_mass[t].append(m) # Nexp / (sigma*L) = A * eff
                    graph = ROOT.TGraph(len(ctau_data[t]), np.array(ctau_mass[t]), np.array(ctau_data[t]))
                    ctau_splines[t] = ROOT.TSpline3("spline_acceptance_%s_%i_%s"%(sigModel,t,d), graph)
                # Plot:
                local = True
                if local:
                    #
                    # 2D plot
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    log = True
                    mass_grid = np.logspace(-0.301, 1.699, num=200)
                    ctau_grid = sigCTaus # for now
                    # Interpolated surface
                    Z = np.zeros((len(ctau_grid), len(mass_grid)))
                    for m_,m in enumerate(mass_grid):
                        for t_,t in enumerate(ctau_grid):
                            if (m < 1.0 and t > 10) or (m < 30.0 and t > 100):
                                continue
                            Z[t_, m_] = ctau_splines[t].Eval(m)
                    X, Y = np.meshgrid(mass_grid, np.log10(ctau_grid))
                    surface = ax.plot_surface(X, Y, Z*100., cmap='viridis', edgecolor='none', alpha=0.5)
                    minZ = 9999.
                    for _t,t in enumerate(sigCTaus):
                        if log:
                            major_ticks = [0.1, 1.0, 10.0, 100.0]
                            ax.set_yticks(np.log10(major_ticks))
                            ax.set_yticklabels(major_ticks)
                            minor_ticks = np.log10([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 2, 3, 4, 5, 6, 7, 8, 9, 20., 30., 40., 50., 60., 70., 80., 90.])
                            ax.yaxis.set_minor_locator(FixedLocator(minor_ticks))
                            ctau_mass_log = np.log10(ctau_mass[t])
                            ctau_log = np.log10(t)
                            ax.scatter(ctau_mass[t], np.full(len(ctau_mass[t]), ctau_log), np.array(ctau_data[t])*100., c='gray', zorder=10)
                            if min(ctau_data[t]) < minZ: minZ = min(ctau_data[t])
                        else:
                            ax.scatter(ctau_mass[t], np.full(len(ctau_mass[t]), t), ctau_data[t], c='blue')
                    ax.set_xlabel("Mass (GeV)", labelpad=20)                    
                    ax.set_ylabel(r"$c\tau$ (mm)", labelpad=20)                    
                    ax.set_zlabel(r'Acceptance $\times$ Efficiency (%)', labelpad=20)
                    ax.set_zlim(minZ, 1.3*np.max(Z)*100.)
                    ax.set_xlim(np.min(X), np.max(X))
                    ax.set_ylim(np.min(Y), np.max(Y))
                    ax.set_title(title, fontsize=30) 
                    fig.savefig('%s/2Dacceptance_%s_%s_%s.png'%(outDir, sigModel, d, y), dpi=140)
                else:
                    log = True
                    mass_grid = np.logspace(-0.301, 1.699, num=100)
                    ctau_grid = sigCTaus
                    Z = np.zeros((len(ctau_grid), len(mass_grid)))

                    # Creates surface for interpolation
                    for m_, m in enumerate(mass_grid):
                        for t_, t in enumerate(ctau_grid):
                            if (m < 1.0 and t > 10) or (m < 30.0 and t > 100):
                                continue
                            Z[t_, m_] = ctau_splines[t].Eval(m) 
                    #
                    # Grid with ctau log
                    X, Y = np.meshgrid(mass_grid, np.log10(ctau_grid))
                    #
                    # Plotly figure
                    fig = go.Figure()
                    # Add surface for interpolation
                    fig.add_trace(go.Surface(
                        x=X,
                        y=Y,
                        z=Z * 100,
                        colorscale='Viridis',
                        opacity=0.5,
                        colorbar=dict(title='Acceptance x Efficiency (%)')
                    ))
                    # Add points for samples
                    minZ = 9999.
                    for t in sigCTaus:
                        ctau_log = np.log10(t) if log else t
                        ctau_mass_log = np.log10(ctau_mass[t]) if log else ctau_mass[t]
                        fig.add_trace(go.Scatter3d(
                            x=np.array(ctau_mass[t]),
                            y=np.full(len(ctau_mass[t]), ctau_log),
                            z=np.array(ctau_data[t]) * 100,
                            mode='markers',
                            marker=dict(color='gray', size=3),
                            name=f'ct={t} mm'
                        ))
                        minZ = min(minZ, min(ctau_data[t]))
                    # Axis and labels configuration
                    fig.update_layout(
                        scene=dict(
                            xaxis=dict(
                                title="Mass (GeV)",
                                range=[0, 50]
                            ),
                            yaxis=dict(
                                title=r"$c\tau$ (mm)",
                                tickvals=np.log10([0.1, 1.0, 10.0, 100.0]) if log else None,
                                ticktext=[0.1, 1.0, 10.0, 100.0] if log else None
                            ),
                            zaxis=dict(
                                title='Acceptance x Efficiency (%)',
                                range=[minZ * 0.1, 1.3 * np.max(Z) * 100]
                            )
                        ),
                        title=dict(text=title, font=dict(size=30)),
                    )
                    #
                    # Save the html
                    fig.write_html(f'{outDir}/2Dacceptance_{sigModel}_{d}_{y}.html')
# 
# 
# Plot signal efficiency vs lifetime (paper)
if doPaperPlot:
    #
    #colors = ["k","#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"] 
    colors = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"] 
    #
    nSignal_perYear['total'] = {}
    for d_,d in enumerate(dNames):
        nSignal_perYear['total'][d] = np.zeros((len(sigMasses),len(sigCTaus)))
        for y in years:
            nSignal_perYear['total'][d] = nSignal_perYear['total'][d] + nSignal_perYear[str(y)][d]
    #
    # Inclusive and Run 2 line
    nSignal_perYear['total']['inclusive'] = nSignal_perYear['total'][dNames[0]]
    for d_,d in enumerate(dNames):
        if d_==0 or 'Four' in d: continue
        nSignal_perYear['total']['inclusive'] = nSignal_perYear['total']['inclusive'] + nSignal_perYear['total'][d]
    nSignal_perYear['total']['run2'] = nSignal_perYear['total']['inclusive'] - nSignal_perYear['total']['d_Dimuon_lxy11p0to16p0_inclusive'] - nSignal_perYear['total']['d_Dimuon_lxy16p0to70p0_inclusive']
    #
    sigCTaus_cm = np.array(sigCTaus)*0.1
    for _m,m in enumerate(sigMasses):
        plt.style.use(hep.style.CMS)
        fig, ax = plt.subplots(figsize=(10.5, 8))
        #hep.cms.label("Preliminary", data=False, com='13.6')
        hep.cms.text("Simulation", loc=0, ax=ax, fontsize=30)
        hep.cms.lumitext("2022 + 2023 (13.6 TeV)", ax=ax, fontsize=30, fontname=None)
        ax.set_ylabel(r'Acceptance x selection efficiency', fontsize=30)
        if sigModel=="HTo2ZdTo2mu2x":
            ax.set_xlabel(r'Dark photon $c\tau_{0}$ [cm]', fontsize=30)
            #ax.text(0.04, 0.95, r'$H\rightarrow Z_DZ_D \rightarrow 2\mu + X$', transform=ax.transAxes, fontsize=17, verticalalignment='top',horizontalalignment='left')
            #ax.text(0.04, 0.9, r'$m_H = 125$ GeV', transform=ax.transAxes, fontsize=17, verticalalignment='top',horizontalalignment='left')
            #ax.text(0.04, 0.85, r'$m_{Z_D} =$ %.0f GeV'%m, transform=ax.transAxes, fontsize=17, verticalalignment='top',horizontalalignment='left')
            ax.text(0.04, 0.6, r'$H\rightarrow Z_DZ_D \rightarrow 2\mu + X$, $m_H = 125$ GeV $m_{Z_D} =$ %.0f GeV'%m, transform=ax.transAxes, fontsize=20, verticalalignment='top',horizontalalignment='left')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylim(5e-3, 10)
        #ax.set_yscale('linear')
        #ax.set_ylim(0.0, 0.5)
        ax.set_xlim(sigCTaus_cm[0], sigCTaus_cm[-1])
        #ax.set_yticks([0.001, 0.01, 0.1, 1.0])
        #ax.set_yticklabels([r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$", "1"])
        if sigCTaus_cm[-1] > 11:
            ax.set_xticks([0.01, 0.1, 1.0, 10.00, 100.0])
            ax.set_xticklabels([r"$10^{-2}$", r"$10^{-1}$", "1", r"$10$", r"$10^2$"])
        else:
            ax.set_xticks([0.01, 0.1, 1.0, 10.00])
            ax.set_xticklabels([r"$10^{-2}$", r"$10^{-1}$", "1", r"$10$"])
        #
        #ax.set_xlim(sigCTaus_cm[0], 1.0)
        efilter_vector = np.zeros(len(sigCTaus_cm))
        if correctByFilter and sigModel=="HTo2ZdTo2mu2x":
            for n in range(len(sigCTaus_cm)):
                if sigCTaus_cm[n]*10. <= 1.0001:
                    timestamp = 1
                elif sigCTaus_cm[n]*10. <= 10.0001:
                    timestamp = 10
                elif sigCTaus_cm[n]*10. <= 100.0001:
                    timestamp = 100
                else:
                    timestamp = 1000
                efilter = 1.0
                with open('data/hahm-request.csv') as mcinfo:
                    reader = csv.reader(mcinfo, delimiter=',')
                    for row in reader:
                        if "MZd-%s_ctau-%imm"%(str(m).replace('.','p'), timestamp) in row[0]:
                            #efilter = float(row[-1])
                            efilter_vector[n] = float(row[-1])
                            break
                nSignal_perYear['total']['inclusive'][_m][n] = nSignal_perYear['total']['inclusive'][_m][n] / efilter_vector[n]
                nSignal_perYear['total']['run2'][_m][n] = nSignal_perYear['total']['run2'][_m][n] / efilter_vector[n]
                for d_,d in enumerate(dNames):
                    nSignal_perYear['total'][d][_m][n] = nSignal_perYear['total'][d][_m][n] / efilter_vector[n]
        ax.plot(sigCTaus_cm, nSignal_perYear['total']['inclusive'][_m]/(1000*62), label='Inclusive', color='k', linestyle='-', lw=2)
        ax.plot(sigCTaus_cm, nSignal_perYear['total']['run2'][_m]/(1000*62), label=r'$0.0 < l_{xy} < 11.0 $ cm', color='k', linestyle=':', lw=2)
        for d_,d in enumerate(dNames):
            ax.plot(sigCTaus_cm, nSignal_perYear['total'][d][_m]/(1000*62), label=legData[d], color=colors[d_], linestyle='--', lw=2)
        ax.legend(loc='upper left', fontsize = 20, frameon = False, ncol=2)
        fig.savefig('%s/signalEfficiency_%s_M%s_paper.png'%(outDir, sigModel, str(m).replace('.', 'p')), dpi=400)
        fig.savefig('%s/signalEfficiency_%s_M%s_paper.pdf'%(outDir, sigModel, str(m).replace('.', 'p')), dpi=400)

        if hepdata_input:
            if sigModel=="HTo2ZdTo2mu2x" and m in [2.0, 5.0, 12.0, 20.0]:
                if m==2.0:
                    name = "Figure_004-a"
                if m==5.0:
                    name = "Figure_004-b"
                if m==12.0:
                    name = "Figure_004-c"
                if m==20.0:
                    name = "Figure_004-d"
                fig.savefig(f"paperPlots/{name}.png", dpi=140)
                fig.savefig(f"paperPlots/{name}.pdf", dpi=140)
                #data_hep = {}
                #data_hep['ctau_values'] = ctauv
                #data_hep['expected_values'] = expv
                #data_hep['observed_values'] = obsv
                #data_hep['p2sigma_values'] = p2sv
                #data_hep['p1sigma_values'] = p1sv
                #data_hep['m1sigma_values'] = m1sv
                #data_hep['m2sigma_values'] = m2sv, 
                #with open(f'paperPlots/hepdata_{name}.pkl', 'wb') as f:
                #    pickle.dump(data_hep, f)
    