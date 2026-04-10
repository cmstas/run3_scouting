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

# Output definition
outDir = ("%s/plotsTriggerEfficiency_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)
##

# Years
years = []
years.append(2022)
years.append(2023)

eras = {}
eras[2022] = ['2022', '2022postEE']
#eras[2023] = ['2023', '2023BPix']
eras[2023] = ['2023BPix']

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
    sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 7.0, 8.0, 14.0, 16.0, 20.0, 24.0, 30.0, 40.0, 50.0]
    sigCTaus = [1, 10, 100, 1000]
    #sigCTaus = [10]

if sigModel=="BToPhi":
    sigMasses = [0.25, 0.3, 0.4, 0.6, 0.7, 0.9, 1.25, 1.5, 2.85, 3.35]
    sigCTaus = [0.1, 1, 10, 100]

#
#
## Loop to make the plots
for y in years:
    if y==2022:
        inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Mar-19-2024_2022_HLTeff"
    else:
        inDir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Mar-19-2024_2023_HLTeff"
    #
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.set_ylabel(r'Trigger efficiency', fontsize=24)
    ax.set_xlabel(r'LLP mass (GeV)', fontsize=24)
    ax.set_xscale('log')
    hep.cms.label("Preliminary", data=True, lumi=27, year=y, com='13.6')
    #
    for t in sigCTaus:
        trigEff = []
        masses = []
        for m in sigMasses:
            if (sigModel=="HTo2ZdTo2mu2x" and ((m < 1.0 and t > 10) or (m < 1.99 and t > 100))):
                continue
            den = 0
            num = 0
            for era in eras[y]:
                inFile = inDir + "/output_Signal_%s_MZd-%s_ctau-%imm_%s_%i_0To99.root"%(sigModel, str(m).replace('.', 'p'), t, era, y)
                tFile = ROOT.TFile(inFile)
                counts = tFile.Get('counts')
                cutflow = tFile.Get('cutflow')
                den = den + counts.GetEntries()
                num = num + cutflow.GetBinContent(2)
            print(m, t, num, den)
            trigEff.append(num/den)
            masses.append(m)
        ax.plot(masses, trigEff, label=r'$h\rightarrow Z_{D}Z_{D}$, $c\tau = $%i mm'%(t), color=colors[str(t)], marker='o', linestyle='')
    ax.legend(loc='upper left', fontsize = 16, frameon = True, ncol=2)
    fig.savefig('%s/trigEff_%s_%s.png'%(outDir, sigModel, y), dpi=140)


