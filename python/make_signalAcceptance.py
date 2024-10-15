import ROOT
import numpy
import copy
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

doRel = True

wsname = "wfit"
thisDir = os.environ.get("PWD")

useCategorizedSignal = True
useCategorizedBackground = True
useSignalMC = True
doSystVariations = False
sigModel = "HTo2ZdTo2mu2x"

# Output definition
outDir = ("%s/plotsAcceptance_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)
#
outFileName = ("%s/plotsAcceptance_"%(thisDir))+today + "/acceptanceSplines_2022.root" # Year is hardcoded
outFile = ROOT.TFile(outFileName, "RECREATE")
outFile.Close()

# Signal Regions
dNames = []
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

# Years
years = []
years.append("2022")
#years.append("2023")

# Style settings
ROOT.gStyle.SetOptStat(0)
# Colors : ['#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd']
colors = {}
colors['0.1']   = '#832db6'
colors['1']     = '#3f90da'
colors['10']    = '#ffa90e'
colors['100']   = '#bd1f01'
colors['1000']  = '#94a4a2'

# Signals
sigMasses = []
sigCTaus = []
if sigModel=="HTo2ZdTo2mu2x":
    sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
    for  m in sigMasses:
        sigCTaus = [1, 10, 100, 1000]
        for t in sigCTaus:
            if ((m < 1.0 and t > 10) or (m < 30.0 and t > 100)):
                continue
    sigCTaus = [1, 10, 100, 1000]

#
#
## Loop to make the plots
splines = []
for d_,d in enumerate(dNames):
    #
    y = 2022 # hardcoded
    #inDir  = "%s/fitResults_%i_August2024/"%(thisDir, y)
    inDir  = "%s/fitResults_%i/"%(thisDir, y)
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
        catExtS = "_ch%d_%i"%(binidx, 2022)
    #
    # Start making the plot
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(11, 10))
    ax.set_ylabel(r'Acceptance $\times$ Efficiency (%)', fontsize=24)
    ax.set_xlabel(r'LLP mass (GeV)', fontsize=24)
    #ax.set_xlim(0, 42)
    #ax.set_ylim(1e-3, 1e7)
    ax.set_xscale('log')
    hep.cms.label("Preliminary", data=True, lumi=35, year=2022, com='13.6')
    if "FourMu_sep" in d:
        fig.text(0.15, 0.7, 'Multivertex four-muon region', color='black', fontsize = 16)
    elif "FourMu_osv" in d:
        fig.text(0.15, 0.7, 'Overlapping four-muon vertex region', color='black', fontsize = 16)
    else:
        if "non-pointing" in d:
            fig.text(0.15, 0.67, r'Non-pointing dimuons: $0.02 < |\Delta\Phi| < \pi/2$', color='black', fontsize = 16)
        else:
            fig.text(0.15, 0.67, r'Pointing dimuons: $|\Delta\Phi| < 0.02$', color='black', fontsize = 16)
        if "lxy0p0to0p2":
            fig.text(0.15, 0.64, r'$l_{xy} \in [0.0, 0.2]$ cm', color='black', fontsize = 16)
        elif "lxy0p2to1p0":
            fig.text(0.15, 0.64, r'$l_{xy} \in [0.2, 1.0]$ cm', color='black', fontsize = 16)
        elif "lxy1p0to2p4":
            fig.text(0.15, 0.64, r'$l_{xy} \in [1.0, 2.4]$ cm', color='black', fontsize = 16)
        elif "lxy2p4to3p1":
            fig.text(0.15, 0.64, r'$l_{xy} \in [2.4, 3.1]$ cm', color='black', fontsize = 16)
        elif "lxy3p1to7p0":
            fig.text(0.15, 0.64, r'$l_{xy} \in [3.1, 7.0]$ cm', color='black', fontsize = 16)
        elif "lxy7p0to11p0":
            fig.text(0.15, 0.64, r'$l_{xy} \in [7.0, 11.0]$ cm', color='black', fontsize = 16)
        elif "lxy11p0to16p0":
            fig.text(0.15, 0.64, r'$l_{xy} \in [11.0, 16.0]$ cm', color='black', fontsize = 16)
        elif "lxy16p0to70p0":
            fig.text(0.15, 0.64, r'$l_{xy} \in [16.0, 70.0]$ cm', color='black', fontsize = 16)
        if "iso1" in d:
            fig.text(0.15, 0.61, r'Isolated muons', color='black', fontsize = 16)
        elif "iso0" in d:
            fig.text(0.15, 0.61, r'Non-isolated muons', color='black', fontsize = 16)
        if "pthigh" in d:
            fig.text(0.15, 0.58, r'$p_{T}^{\mu\mu} > 25$ GeV', color='black', fontsize = 16)
        elif "ptlow" in d:
            fig.text(0.15, 0.58, r'$p_{T}^{\mu\mu} < 25$ GeV', color='black', fontsize = 16)
    for _t,t in enumerate(sigCTaus):
        acceptance = []
        masses = []
        for m in sigMasses:
            if (sigModel=="HTo2ZdTo2mu2x" and ((m < 1.0 and t > 10) or (m < 30.0 and t > 100))):
                    continue
            sigTag = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t)
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
        # Graph and acceptance for spline
        graph = ROOT.TGraph(len(acceptance), np.array(masses), np.array(acceptance))
        splines.append(ROOT.TSpline3("spline_acceptance_%s_%i_%s"%(sigModel,t,d), graph))
        splines[-1].SetName("spline_acceptance_%s_%i_%s"%(sigModel,t,d))
        acceptance_100 = [100*x for x in acceptance]
        graph_100 = ROOT.TGraph(len(acceptance_100), np.array(masses), np.array(acceptance_100))
        spline_100 = ROOT.TSpline3("spline_acceptance_%s_%i_%s_100"%(sigModel,t,d), graph_100)
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
        a_interp = [spline_100.Eval(x) for x in m_interp]
        # Plot in the canvas
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

