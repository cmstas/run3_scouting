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

def plotSystematic(outDir, sigTag, y, nominal, up, down, ymin = -50, ymax = 50, stype = 'trigger'):
    ## Plot        
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(16, 5)) 
    fig.subplots_adjust(bottom=0.2, right=0.80)
    luminosity = 35 if y=='2022' else 27
    hep.cms.label("Preliminary", data=True, lumi=luminosity, year=y, com='13.6')
    fig.text(0.35, 0.9, r'$m_{4\mu} = $125 GeV, $m_{2\mu} =$ %s GeV'%(str(m)), color='black', fontsize = 13)
    ax.set_ylabel(r'Signal yield / Search Region', fontsize=20)
    ### Signal
    nh, nbins = getValues(nominal)
    uh, ubins = getValues(up)
    dh, ubins = getValues(down)
    hep.histplot([nh, uh, dh],
                 stack=False,
                 bins=nbins,
                 color=['black', 'blue', 'red'],
                 histtype="step",
                 alpha=1,
                 label=['Nominal', 'Up SF var', 'Down SF var'],
                 ax=ax,
                )
    ax.set_xlim(0, 42)
    ax.set_ylim(1e-3, 1e3)
    ax.set_yscale('log')
    ax.axvline(x=2, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=10, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=18, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=26, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=34, color='gray', linestyle='--', linewidth=1)
    ax.text(0.6, 1e5, r'$4\mu$', color='gray', fontsize = 9)
    ax.text(2.5, 1e5, r'Pointing, isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
    ax.text(10.5, 1e5, r'Pointing, isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
    ax.text(18.5, 1e5, r'Pointing, non-isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
    ax.text(26.5, 1e5, r'Pointing, non-isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
    ax.text(34.5, 1e5, r'Non-pointing', color='gray', fontsize = 8)
    ## x axis:
    x_ticks = [0.0, 1.0]
    x_labels = ['Multivertex', 'Overlapping']
    for x in range(0, 5):
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
    ax.set_xticklabels(x_labels, ha = 'left', rotation=-45, fontsize = 10)
    #ax.xaxis.set_minor_locator(MultipleLocator(0.0))
    ax.minorticks_off()
    ## Legend
    #ax.legend(loc='best', fontsize = 10, frameon = True)
    ax.legend(loc='upper left', fontsize = 10, frameon = True, bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    ## Save
    fig.savefig('%s/Syst_%s_%s.png'%(outDir, sigTag, y), dpi=140)

def plotSystematicVar(outDir, sigTag, y, nominal, up, down, ylabel, ymin = -50., ymax = 50., stype = 'trigger', raw = False):
    ## Plot        
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(16, 5)) 
    fig.subplots_adjust(bottom=0.2, right=0.80)
    luminosity = 35 if y=='2022' else 27
    hep.cms.label("Preliminary", data=True, lumi=luminosity, year=y, com='13.6')
    fig.text(0.35, 0.9, r'$m_{4\mu} = $125 GeV, $m_{2\mu} =$ %s GeV'%(str(m)), color='black', fontsize = 13)
    ax.set_ylabel(ylabel, fontsize=20)
    ### Variations from nominal
    nh, nbins = getValues(nominal)
    uh, ubins = getValues(up)
    dh, ubins = getValues(down)
    uv = (uh/nh - 1.0)*100.0 # upper in %
    dv = (dh/nh - 1.0)*100.0 # lower in %
    #print(uv)
    #print(dv)
    if raw: # filter for 2mu
        rawv, rbins = getValues(raw)
        print(rawv)
        fuv = uv[2:][rawv[2:] > 200.0]
        fdv = dv[2:][rawv[2:] > 200.0]
        print(fuv)
        print(fdv)
    maxdev = max(np.concatenate((np.absolute(uv), np.absolute(dv)))) # from max to mean
    if raw:
        try:
            maxdev_2mu = max(np.concatenate((np.absolute(fuv), np.absolute(fdv)))) # from max to mean
        except ValueError:
            maxdev_2mu = max(np.concatenate((np.absolute(uv), np.absolute(dv))))
    else:
        maxdev_2mu = max(np.concatenate((np.absolute(uv[2:]), np.absolute(dv[2:])))) # from max to mean
    maxdev_4mu = max(np.concatenate((np.absolute(uv[:2]), np.absolute(dv[:2])))) # from max to mean
    print(maxdev)
    if maxdev < 0.1:
        ymax = 0.2
        ymin = -0.2
    elif maxdev < 0.8:
        ymax = 1.0
        ymin = -1.0
    elif maxdev < 4:
        ymax = 5.0
        ymin = -5.0
    elif maxdev < 9:
        ymax = 10.0
        ymin = -10.0
    elif maxdev < 18:
        ymax = 20.0
        ymin = -20.0
    ax.hist(nbins[:-1], bins=nbins, weights = uv, color='blue', alpha=0.5, label='Upper %s SF variation'%stype)
    ax.hist(nbins[:-1], bins=nbins, weights = dv, color='red', alpha=0.5, label='Lower %s SF variation'%stype)
    ax.set_xlim(0, 42)
    ax.set_ylim(ymin, ymax)
    ax.axvline(x=2, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=10, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=18, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=26, color='gray', linestyle='--', linewidth=1)
    ax.axvline(x=34, color='gray', linestyle='--', linewidth=1)
    ax.text(0.6, 0.8*ymax, r'$4\mu$', color='gray', fontsize = 9)
    ax.text(2.5, 0.8*ymax, r'Pointing, isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
    ax.text(10.5, 0.8*ymax, r'Pointing, isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
    ax.text(18.5, 0.8*ymax, r'Pointing, non-isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
    ax.text(26.5, 0.8*ymax, r'Pointing, non-isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
    ax.text(34.5, 0.8*ymax, r'Non-pointing', color='gray', fontsize = 8)
    plt.axhline(y=maxdev, color="black", linestyle="--")
    plt.axhline(y=-maxdev, color="black", linestyle="--")
    ax.text(34.5, (ymax/30.)+maxdev, r'Maximum deviation = %.2f%%'%maxdev, color='black', fontsize = 8)
    ## x axis:
    x_ticks = [0.0, 1.0]
    x_labels = ['Multivertex', 'Overlapping']
    for x in range(0, 5):
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
    ax.set_xticklabels(x_labels, ha = 'left', rotation=-45, fontsize = 10)
    #ax.xaxis.set_minor_locator(MultipleLocator(0.0))
    ax.minorticks_off()
    ## Legend
    #ax.legend(loc='best', fontsize = 10, frameon = True)
    ax.legend(loc='upper left', fontsize = 10, frameon = True, bbox_to_anchor=(1.02, 1), borderaxespad=0.)
    ## Save
    fig.savefig('%s/SystVar_%s_%s.png'%(outDir, sigTag, y), dpi=140)
    ## Return the maximum deviation
    return maxdev_2mu,maxdev_4mu

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

doRel = True

wsname = "wfit"
thisDir = os.environ.get("PWD")

useCategorizedSignal = True
useCategorizedBackground = True
useSignalMC = True
doSystVariations = True
sigModel = "HTo2ZdTo2mu2x" # HTo2ZdTo2mu2x  ScenarioB1

outDir = ("%s/plotsSRs_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)
outFileName = "%s/systematicSplines_2022.root"%(outDir) # Year is hardcoded
outFile = ROOT.TFile(outFileName, "RECREATE")
outFile.Close()

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

years = []
years.append("2022")
#years.append("2023")

ROOT.gStyle.SetOptStat(0)

# Load signals
if useSignalMC:
    if sigModel=="HTo2ZdTo2mu2x":
        sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        sigCTaus = [1, 10, 100, 1000]
    elif sigModel=="ScenarioB1":
        sigMasses = [1.33]
        sigCTaus = [0.1, 1, 10, 100]


## Loop to make the plots
for y in years:
    inDir  = "%s/fitResults_%s/"%(thisDir, y)
    # Normalization:
    values_norm_trg = {} # mass, ctau, dname
    values_norm_sel = {} # mass, ctau, dname
    # Shape variations:
    values_maxdev_mean_2mu = [] # Depth: mass, ctau, dname
    values_maxdev_mean_4mu = []
    values_maxdev_sigma_2mu = []
    values_maxdev_sigma_4mu = []
    #
    for m in sigMasses:
        hbkg = ROOT.TH1F("bkg_%s"%(str(m)), "", len(dNames), 0, len(dNames))
        hsigs = []
        hsigs_raw = []
        hsigs_trgUp = []
        hsigs_trgDown = []
        hsigs_selUp = []
        hsigs_selDown = []
        hsigma = []
        hsigma_trgUp = []
        hsigma_trgDown = []
        hsigma_selUp = []
        hsigma_selDown = []
        hmean = []
        hmean_trgUp = []
        hmean_trgDown = []
        hmean_selUp = []
        hmean_selDown = []
        legLabels = []
        values_maxdev_mean_2mu.append([])
        values_maxdev_sigma_2mu.append([])
        values_maxdev_mean_4mu.append([])
        values_maxdev_sigma_4mu.append([])
        #
        values_norm_trg[m] = {}
        values_norm_sel[m] = {}
        #
        for t in sigCTaus:
            if (sigModel=="HTo2ZdTo2mu2x" and ((m < 1.0 and t > 10) or (m < 30.0 and t > 100))):
                 continue
            sigTag = ""
            if (sigModel=="HTo2ZdTo2mu2x"):
                sigTag = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t)
                legLabels.append(r"$h\rightarrow Z_{D}Z_{D}$, $m_{Z_D} = $%s GeV, $c\tau =$ %s mm"%(str(m), str(t)))
            elif (sigModel=="ScenarioB1"):
                sigTag = "Signal_ScenarioB1_mpi-4_mA-%s_ctau-%smm"%(str(m).replace(".", "p"),str(t).replace('.','p'))
                legLabels.append(r"$m_{\pi} = 4$ GeV, $m_{A} = $%s GeV, $c\tau =$ %s mm"%(str(m), str(t))) 
            hsigs.append(ROOT.TH1F(sigTag, "", len(dNames), 0, len(dNames)))
            hsigs_raw.append(ROOT.TH1F(sigTag+"_raw", "", len(dNames), 0, len(dNames)))
            hsigs_trgUp.append(ROOT.TH1F(sigTag+"_trg_up", "", len(dNames), 0, len(dNames)))
            hsigs_trgDown.append(ROOT.TH1F(sigTag+"_trg_down", "", len(dNames), 0, len(dNames)))
            hsigs_selUp.append(ROOT.TH1F(sigTag+"_sel_up", "", len(dNames), 0, len(dNames)))
            hsigs_selDown.append(ROOT.TH1F(sigTag+"_sel_down", "", len(dNames), 0, len(dNames)))
            hsigma.append(ROOT.TH1F(sigTag+"_sigma", "", len(dNames), 0, len(dNames)))
            hsigma_trgUp.append(ROOT.TH1F(sigTag+"_sigma_trg_up", "", len(dNames), 0, len(dNames)))
            hsigma_trgDown.append(ROOT.TH1F(sigTag+"_sigma_trg_down", "", len(dNames), 0, len(dNames)))
            hsigma_selUp.append(ROOT.TH1F(sigTag+"_sigma_sel_up", "", len(dNames), 0, len(dNames)))
            hsigma_selDown.append(ROOT.TH1F(sigTag+"_sigma_sel_down", "", len(dNames), 0, len(dNames)))
            hmean.append(ROOT.TH1F(sigTag+"_mean", "", len(dNames), 0, len(dNames)))
            hmean_trgUp.append(ROOT.TH1F(sigTag+"_mean_trg_up", "", len(dNames), 0, len(dNames)))
            hmean_trgDown.append(ROOT.TH1F(sigTag+"_mean_trg_down", "", len(dNames), 0, len(dNames)))
            hmean_selUp.append(ROOT.TH1F(sigTag+"_mean_sel_up", "", len(dNames), 0, len(dNames)))
            hmean_selDown.append(ROOT.TH1F(sigTag+"_mean_sel_down", "", len(dNames), 0, len(dNames)))
            #
            values_norm_trg[m][t] = {}
            values_norm_sel[m][t] = {}
            #
            for d_,d in enumerate(dNames):
                print("Analyzing %s, in region %s"%(sigTag, d))
                print("%s/%s_%s_%s_workspace.root"%(inDir,d,sigTag,y))
                finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,sigTag,y)
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
                catExtB = ""
                if useCategorizedSignal:
                    catExtS = "_ch%d_%s"%(binidx, y)
                if useCategorizedBackground:
                    catExtB = "_ch%d_%s"%(binidx, y)
                # Open input file with workspace
                f = ROOT.TFile(finame)
                # Retrieve workspace from file
                w = f.Get(wsname)
                # Retrieve signal normalization
                nSig = w.var("signalNorm%s"%catExtS).getValV()
                nSigRaw = w.var("signalRawNorm%s"%catExtS).getValV()
                # Retrieve BG normalization:
                nBG = w.data("data_obs%s"%catExtB).sumEntries()
                # Retrieve signal width and mean
                sigma = w.var("sigma%s"%catExtS).getValV()
                mean = w.var("mean%s"%catExtS).getValV()
                # Assign
                hbkg.SetBinContent(d_+1, nBG)
                hbkg.SetBinError(d_+1, nBG**0.5)
                hsigs[-1].SetBinContent(d_+1, nSig)
                hsigs_raw[-1].SetBinContent(d_+1, nSigRaw)
                hsigma[-1].SetBinContent(d_+1, sigma)
                hmean[-1].SetBinContent(d_+1, mean)
                if doSystVariations:
                    w_trgUp = f.Get(wsname + '_trg_up')
                    w_trgDown = f.Get(wsname + '_trg_down')
                    w_selUp = f.Get(wsname + '_sel_up')
                    w_selDown = f.Get(wsname + '_sel_down')
                    nSig_trgUp = w_trgUp.var("signalNorm%s"%catExtS).getValV()
                    nSig_trgDown = w_trgDown.var("signalNorm%s"%catExtS).getValV()
                    nSig_selUp = w_selUp.var("signalNorm%s"%catExtS).getValV()
                    nSig_selDown = w_selDown.var("signalNorm%s"%catExtS).getValV()
                    sigma_trgUp = w_trgUp.var("sigma%s"%catExtS).getValV()
                    sigma_trgDown = w_trgDown.var("sigma%s"%catExtS).getValV()
                    sigma_selUp = w_selUp.var("sigma%s"%catExtS).getValV()
                    sigma_selDown = w_selDown.var("sigma%s"%catExtS).getValV()
                    mean_trgUp = w_trgUp.var("mean%s"%catExtS).getValV()
                    mean_trgDown = w_trgDown.var("mean%s"%catExtS).getValV()
                    mean_selUp = w_selUp.var("mean%s"%catExtS).getValV()
                    mean_selDown = w_selDown.var("mean%s"%catExtS).getValV()
                    hsigs_trgUp[-1].SetBinContent(d_+1, nSig_trgUp)
                    hsigs_trgDown[-1].SetBinContent(d_+1, nSig_trgDown)
                    hsigs_selUp[-1].SetBinContent(d_+1, nSig_selUp)
                    hsigs_selDown[-1].SetBinContent(d_+1, nSig_selDown)
                    hsigma_trgUp[-1].SetBinContent(d_+1, sigma_trgUp)
                    hsigma_trgDown[-1].SetBinContent(d_+1, sigma_trgDown)
                    hsigma_selUp[-1].SetBinContent(d_+1, sigma_selUp)
                    hsigma_selDown[-1].SetBinContent(d_+1, sigma_selDown)
                    hmean_trgUp[-1].SetBinContent(d_+1, mean_trgUp)
                    hmean_trgDown[-1].SetBinContent(d_+1, mean_trgDown)
                    hmean_selUp[-1].SetBinContent(d_+1, mean_selUp)
                    hmean_selDown[-1].SetBinContent(d_+1, mean_selDown)
                    #
                    values_norm_trg[m][t][d] = max([(nSig_trgUp/nSig - 1.0), (1.0 - nSig_trgDown/nSig)])
                    values_norm_sel[m][t][d] = max([(nSig_selUp/nSig - 1.0), (1.0 - nSig_selDown/nSig)])
                    #
                # Close input file with workspace
                f.Close()

            ## Systematic plots
            if doSystVariations:
                #plotSystematic(outDir, sigTag+'_trg', y, hsigs[-1], hsigs_trgUp[-1], hsigs_trgDown[-1])
                plotSystematicVar(outDir, sigTag+'_trg', y, hsigs[-1], hsigs_trgUp[-1], hsigs_trgDown[-1], r'$N_{Signal}^{Up/Down}$/$N_{Signal}^{Nominal}$ (%)', stype='trigger')
                #plotSystematic(outDir, sigTag+'_sigma_trg', y, hsigma[-1], hsigma_trgUp[-1], hsigma_trgDown[-1])
                vtrg_sigma_2mu,vtrg_sigma_4mu = plotSystematicVar(outDir, sigTag+'_sigma_trg', y, hsigma[-1], hsigma_trgUp[-1], hsigma_trgDown[-1], r'$\sigma^{Up/Down}$/$\sigma$ (%)', -20., 20., stype='trigger', raw=hsigs_raw[-1])
                #plotSystematic(outDir, sigTag+'_mean_trg', y, hmean[-1], hmean_trgUp[-1], hmean_trgDown[-1])
                vtrg_mean_2mu,vtrg_mean_4mu = plotSystematicVar(outDir, sigTag+'_mean_trg', y, hmean[-1], hmean_trgUp[-1], hmean_trgDown[-1], r'$\mu^{Up/Down}$/$\mu$ (%)', -1., 1., 'trigger', raw=hsigs_raw[-1])
                #plotSystematic(outDir, sigTag+'_sel', y, hsigs[-1], hsigs_selUp[-1], hsigs_selDown[-1])
                plotSystematicVar(outDir, sigTag+'_sel', y, hsigs[-1], hsigs_selUp[-1], hsigs_selDown[-1], r'$N_{Signal}^{Up/Down}$/$N_{Signal}^{Nominal}$ (%)', stype='selection',)
                #plotSystematic(outDir, sigTag+'_sigma_sel', y, hsigma[-1], hsigma_selUp[-1], hsigma_selDown[-1])
                vsel_sigma_2mu,vsel_sigma_4mu = plotSystematicVar(outDir, sigTag+'_sigma_sel', y, hsigma[-1], hsigma_selUp[-1], hsigma_selDown[-1], r'$\sigma^{Up/Down}$/$\sigma$ (%)', -20., 20., stype='selection', raw=hsigs_raw[-1])
                #plotSystematic(outDir, sigTag+'_mean_sel', y, hmean[-1], hmean_selUp[-1], hmean_selDown[-1])
                vsel_mean_2mu,vsel_mean_4mu = plotSystematicVar(outDir, sigTag+'_mean_sel', y, hmean[-1], hmean_selUp[-1], hmean_selDown[-1], r'$\mu^{Up/Down}$/$\mu$ (%)', -1., 1., stype='selection', raw=hsigs_raw[-1])
                values_maxdev_mean_2mu[-1].append(max([vtrg_mean_2mu, vsel_mean_2mu]))
                values_maxdev_sigma_2mu[-1].append(max([vtrg_sigma_2mu, vsel_sigma_2mu]))
                values_maxdev_mean_4mu[-1].append(max([vtrg_mean_4mu, vsel_mean_4mu]))
                values_maxdev_sigma_4mu[-1].append(max([vtrg_sigma_4mu, vsel_sigma_4mu]))

        ## Plot        
        print(len(hsigs), len(legLabels))
        plt.style.use(hep.style.CMS)
        colors = ['#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd']
        fig, ax = plt.subplots(figsize=(16, 5)) 
        fig.subplots_adjust(bottom=0.2, right=0.80)
        luminosity = 35 if y=='2022' else 27
        hep.cms.label("Preliminary", data=True, lumi=luminosity, year=y, com='13.6')
        fig.text(0.35, 0.9, r'$m_{4\mu} = $125 GeV, $m_{2\mu} =$ %s GeV'%(str(m)), color='black', fontsize = 13)
        ax.set_ylabel(r'Events / Search Region', fontsize=20)
        ### Data
        hb, bins = getValues(hbkg)
        print(hb)
        print(bins)
        width = (bins[1] - bins[0])
        print(width)
        bcenter = np.array([(bins[x] + 0.5*width) for x in range(0, len(bins)-1)])
        xerrs = [width * 0.5 for i in range(0, len(bins)-1)]
        yerrs = np.sqrt(hb)
        ax.errorbar(bcenter,
            hb,
            xerr=xerrs,
            yerr=yerrs,
            linestyle="None",
            color="black",
            marker="o",
            label="Data"
            )
        ### Signal
        msigs = []
        for h in hsigs:
            mh, mbins = getValues(h)
            msigs.append(mh)
        hep.histplot(
            msigs,
            stack=False,
            bins=bins,
            color=colors[:len(msigs)],
            histtype="step",
            alpha=1,
            label=legLabels,
            ax=ax,
        )
        ax.set_xlim(0, 42)
        ax.set_ylim(1e-3, 1e7)
        ax.set_yscale('log')
        ax.axvline(x=2, color='gray', linestyle='--', linewidth=1)
        ax.axvline(x=10, color='gray', linestyle='--', linewidth=1)
        ax.axvline(x=18, color='gray', linestyle='--', linewidth=1)
        ax.axvline(x=26, color='gray', linestyle='--', linewidth=1)
        ax.axvline(x=34, color='gray', linestyle='--', linewidth=1)
        ax.text(0.6, 1e5, r'$4\mu$', color='gray', fontsize = 9)
        ax.text(2.5, 1e5, r'Pointing, isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
        ax.text(10.5, 1e5, r'Pointing, isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
        ax.text(18.5, 1e5, r'Pointing, non-isolated, $p_{T}^{\mu\mu} > 25$ GeV', color='gray', fontsize = 8)
        ax.text(26.5, 1e5, r'Pointing, non-isolated, $p_{T}^{\mu\mu} < 25$ GeV', color='gray', fontsize = 8)
        ax.text(34.5, 1e5, r'Non-pointing', color='gray', fontsize = 8)
        ## x axis:
        x_ticks = [0.0, 1.0]
        x_labels = ['Multivertex', 'Overlapping']
        for x in range(0, 5):
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
        ax.set_xticklabels(x_labels, ha = 'left', rotation=-45, fontsize = 10)
        #ax.xaxis.set_minor_locator(MultipleLocator(0.0))
        ax.minorticks_off()
        ## Legend
        #ax.legend(loc='best', fontsize = 10, frameon = True)
        ax.legend(loc='upper left', fontsize = 10, frameon = True, bbox_to_anchor=(1.02, 1), borderaxespad=0.)
        ## Save
        fig.savefig('%s/SRs_%s_%s.png'%(outDir, sigTag, y), dpi=140)

    ### Summary plots and splines
    colors = {}
    colors['0.1']   = '#832db6'
    colors['1.0']     = '#3f90da'
    colors['10.0']    = '#ffa90e'
    colors['100.0']   = '#bd1f01'
    colors['1000.0']  = '#94a4a2'
    if doSystVariations:
        #
        # Normalization variations
        for d_,d in enumerate(dNames):
            for t in sigCTaus:
                fig, ax = plt.subplots(figsize=(16, 5))
                fig.subplots_adjust(bottom=0.2, right=0.80)
                ax.set_ylabel(r'Normalization variation (%)', fontsize=20)
                ax.set_xlabel(r'Mass (GeV)', fontsize=20)
                ax.set_xscale('log')
                hep.cms.label("Preliminary", data=False, lumi=luminosity, year=y, com='13.6')
                #
                vmasses = []
                vtrg = []
                vsel = []
                for m in sigMasses:
                    if t not in values_norm_trg[m].keys():
                        continue
                    vmasses.append(m)
                    vtrg.append(values_norm_trg[m][t][d])
                    vsel.append(values_norm_sel[m][t][d])
                ax.plot(np.array(vmasses), 100*np.array(vtrg), label='Trigger variation (%)', marker='o', linestyle='', color='tab:blue')
                ax.plot(np.array(vmasses), 100*np.array(vsel), label='Selection variation (%)', marker='o', linestyle='', color='tab:green')
                ax.legend(loc='upper right', fontsize = 10)
                fig.text(0.45, 0.9, r'$H\rightarrow Z_DZ_D, Z_D\rightarrow\mu\mu$', color='black', fontsize = 13)
                fig.text(0.15, 0.8, d, color='black', fontsize = 13)
                fig.savefig('%s/NormUnc_%s_%s_%.1f_%s.png'%(outDir, sigModel, d, t, y), dpi=140)
                graph_trg = ROOT.TGraph(len(vmasses), np.array(vmasses), np.array(vtrg))
                spline_trg = ROOT.TSpline3("spline_trgsys_%s_%s_%.1f_%s"%(sigModel, d, t, y), graph_trg)
                spline_trg.SetName("spline_trgsys_%s_%s_%.1f_%s"%(sigModel, d, t, y))
                graph_sel = ROOT.TGraph(len(vmasses), np.array(vmasses), np.array(vsel))
                spline_sel = ROOT.TSpline3("spline_selsys_%s_%s_%.1f_%s"%(sigModel, d, t, y), graph_sel)
                spline_sel.SetName("spline_selsys_%s_%s_%.1f_%s"%(sigModel, d, t, y))
                # Save spline
                outFile = ROOT.TFile.Open(outFileName, "UPDATE")
                spline_trg.Write()
                spline_sel.Write()
                outFile.Close()
        #
        # Shape variations
        vmean_2mu = {}
        vmean_4mu = {}
        vsigma_2mu = {}
        vsigma_4mu = {}
        #print(values_maxdev_mean_2mu)
        #print(values_maxdev_mean_4mu)
        #print(values_maxdev_sigma_2mu)
        #print(values_maxdev_sigma_4mu)
        for t in range(0, len(sigCTaus)):
            ctauLabel = '%.1f'%(sigCTaus[t])
            vmean_2mu[ctauLabel] = []
            vmean_4mu[ctauLabel] = []
            vsigma_2mu[ctauLabel] = []
            vsigma_4mu[ctauLabel] = []
            if sigCTaus[t] <= 10:
                vmean_2mu[ctauLabel] += [values_maxdev_mean_2mu[m][t] for m in range(0, len(sigMasses))]
                vmean_4mu[ctauLabel] += [values_maxdev_mean_4mu[m][t] for m in range(0, len(sigMasses))]
                vsigma_2mu[ctauLabel] += [values_maxdev_sigma_2mu[m][t] for m in range(0, len(sigMasses))]
                vsigma_4mu[ctauLabel] += [values_maxdev_sigma_4mu[m][t] for m in range(0, len(sigMasses))]
            elif sigCTaus[t] <= 100:
                vmean_2mu[ctauLabel] += [values_maxdev_mean_2mu[m][t] for m in range(2, len(sigMasses))]
                vmean_4mu[ctauLabel] += [values_maxdev_mean_4mu[m][t] for m in range(2, len(sigMasses))]
                vsigma_2mu[ctauLabel] += [values_maxdev_sigma_2mu[m][t] for m in range(2, len(sigMasses))]
                vsigma_4mu[ctauLabel] += [values_maxdev_sigma_4mu[m][t] for m in range(2, len(sigMasses))]
            else:
                vmean_2mu[ctauLabel] += [values_maxdev_mean_2mu[m][t] for m in range(14, len(sigMasses))]
                vmean_4mu[ctauLabel] += [values_maxdev_mean_4mu[m][t] for m in range(14, len(sigMasses))]
                vsigma_2mu[ctauLabel] += [values_maxdev_sigma_2mu[m][t] for m in range(14, len(sigMasses))]
                vsigma_4mu[ctauLabel] += [values_maxdev_sigma_4mu[m][t] for m in range(14, len(sigMasses))]
        ### Mean variation (2mu)
        fig, ax = plt.subplots(figsize=(16, 5))
        fig.subplots_adjust(bottom=0.2, right=0.80)
        ax.set_ylabel(r'Max shape $\mu$ variation (%)', fontsize=20)
        ax.set_xlabel(r'Mass (GeV)', fontsize=20)
        ax.set_xscale('log')
        hep.cms.label("Preliminary", data=False, lumi=luminosity, year=y, com='13.6')
        for ctauLabel in vmean_2mu.keys():
            graph_vmean_2mu = ROOT.TGraph(len(vmean_2mu[ctauLabel]), np.array(sigMasses[-len(vmean_2mu[ctauLabel]):]), np.array(vmean_2mu[ctauLabel]))
            spline_vmean_2mu = ROOT.TSpline3("spline_meanvar_2mu_%s_%s"%(sigModel,ctauLabel), graph_vmean_2mu)
            m_interp = np.linspace(sigMasses[-len(vmean_2mu[ctauLabel])], 50.0, 500)
            v_interp = [spline_vmean_2mu.Eval(x) for x in m_interp]
            ax.plot(sigMasses[-len(vmean_2mu[ctauLabel]):], vmean_2mu[ctauLabel], label=r'c$\tau$ = %s'%ctauLabel, marker='o', linestyle='', color=colors[ctauLabel])
            ax.plot(m_interp, v_interp, color=colors[ctauLabel])
        ax.legend(loc='upper right', fontsize = 10)
        fig.text(0.45, 0.9, r'$H\rightarrow Z_DZ_D, Z_D\rightarrow\mu\mu$', color='black', fontsize = 13)
        fig.savefig('%s/ShapeUnc_%s_%s_mean_2mu.png'%(outDir, sigTag, y), dpi=140)
        ### Sigma variation (2mu)
        fig, ax = plt.subplots(figsize=(16, 5))
        fig.subplots_adjust(bottom=0.2, right=0.80)
        ax.set_ylabel(r'Max shape $\sigma$ variation (%)', fontsize=20)
        ax.set_xlabel(r'Mass (GeV)', fontsize=20)
        ax.set_xscale('log')
        hep.cms.label("Preliminary", data=False, lumi=luminosity, year=y, com='13.6')
        for ctauLabel in vsigma_2mu.keys():
            graph_vsigma_2mu = ROOT.TGraph(len(vsigma_2mu[ctauLabel]), np.array(sigMasses[-len(vsigma_2mu[ctauLabel]):]), np.array(vsigma_2mu[ctauLabel]))
            spline_vsigma_2mu = ROOT.TSpline3("spline_sigmavar_2mu_%s_%s"%(sigModel,ctauLabel), graph_vsigma_2mu)
            m_interp = np.linspace(sigMasses[-len(vsigma_2mu[ctauLabel])], 50.0, 500)
            v_interp = [spline_vsigma_2mu.Eval(x) for x in m_interp]
            ax.plot(sigMasses[-len(vsigma_2mu[ctauLabel]):], vsigma_2mu[ctauLabel], label=r'c$\tau$ = %s'%ctauLabel, marker='o', linestyle='', color=colors[ctauLabel])
            ax.plot(m_interp, v_interp, color=colors[ctauLabel])
        ax.legend(loc='upper right', fontsize = 10)
        fig.text(0.45, 0.9, r'$H\rightarrow Z_DZ_D, Z_D\rightarrow\mu\mu$', color='black', fontsize = 13)
        fig.savefig('%s/ShapeUnc_%s_%s_sigma_2mu.png'%(outDir, sigTag, y), dpi=140)
        ### Mean variation (4mu)
        fig, ax = plt.subplots(figsize=(16, 5))
        fig.subplots_adjust(bottom=0.2, right=0.80)
        ax.set_ylabel(r'Max shape $\mu$ variation (%)', fontsize=20)
        ax.set_xlabel(r'Mass (GeV)', fontsize=20)
        ax.set_xscale('log')
        hep.cms.label("Preliminary", data=False, lumi=luminosity, year=y, com='13.6')
        for ctauLabel in vmean_4mu.keys():
            graph_vmean_4mu = ROOT.TGraph(len(vmean_4mu[ctauLabel]), np.array(sigMasses[-len(vmean_4mu[ctauLabel]):]), np.array(vmean_4mu[ctauLabel]))
            spline_vmean_4mu = ROOT.TSpline3("spline_meanvar_4mu_%s_%s"%(sigModel,ctauLabel), graph_vmean_4mu)
            m_interp = np.linspace(sigMasses[-len(vmean_4mu[ctauLabel])], 50.0, 500)
            v_interp = [spline_vmean_4mu.Eval(x) for x in m_interp]
            ax.plot(sigMasses[-len(vmean_4mu[ctauLabel]):], vmean_4mu[ctauLabel], label=r'c$\tau$ = %s'%ctauLabel, marker='o', linestyle='', color=colors[ctauLabel])
            ax.plot(m_interp, v_interp, color=colors[ctauLabel])
        ax.legend(loc='upper right', fontsize = 10)
        fig.text(0.45, 0.9, r'$H\rightarrow Z_DZ_D, Z_D\rightarrow\mu\mu$', color='black', fontsize = 13)
        fig.savefig('%s/ShapeUnc_%s_%s_mean_4mu.png'%(outDir, sigTag, y), dpi=140)
        ### Sigma variation (4mu)
        fig, ax = plt.subplots(figsize=(16, 5))
        fig.subplots_adjust(bottom=0.2, right=0.80)
        ax.set_ylabel(r'Max shape $\sigma$ variation (%)', fontsize=20)
        ax.set_xlabel(r'Mass (GeV)', fontsize=20)
        ax.set_xscale('log')
        hep.cms.label("Preliminary", data=False, lumi=luminosity, year=y, com='13.6')
        for ctauLabel in vsigma_4mu.keys():
            graph_vsigma_4mu = ROOT.TGraph(len(vsigma_4mu[ctauLabel]), np.array(sigMasses[-len(vsigma_4mu[ctauLabel]):]), np.array(vsigma_4mu[ctauLabel]))
            spline_vsigma_4mu = ROOT.TSpline3("spline_sigmavar_4mu_%s_%s"%(sigModel,ctauLabel), graph_vsigma_4mu)
            m_interp = np.linspace(sigMasses[-len(vsigma_4mu[ctauLabel])], 50.0, 500)
            v_interp = [spline_vsigma_4mu.Eval(x) for x in m_interp]
            ax.plot(sigMasses[-len(vsigma_4mu[ctauLabel]):], vsigma_4mu[ctauLabel], label=r'c$\tau$ = %s'%ctauLabel, marker='o', linestyle='', color=colors[ctauLabel])
            ax.plot(m_interp, v_interp, color=colors[ctauLabel])
        ax.legend(loc='upper right', fontsize = 10)
        fig.text(0.45, 0.9, r'$H\rightarrow Z_DZ_D, Z_D\rightarrow\mu\mu$', color='black', fontsize = 13)
        fig.savefig('%s/ShapeUnc_%s_%s_sigma_4mu.png'%(outDir, sigTag, y), dpi=140)








