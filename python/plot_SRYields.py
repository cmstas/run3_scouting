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

def plotSystematic(outDir, sigTag, y, nominal, up, down):
    ## Plot        
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(16, 5)) 
    fig.subplots_adjust(bottom=0.2, right=0.80)
    luminosity = 3.5 if y=='2022' else 2.7
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

def plotSystematicVar(outDir, sigTag, y, nominal, up, down):
    ## Plot        
    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(16, 5)) 
    fig.subplots_adjust(bottom=0.2, right=0.80)
    luminosity = 3.5 if y=='2022' else 2.7
    hep.cms.label("Preliminary", data=True, lumi=luminosity, year=y, com='13.6')
    fig.text(0.35, 0.9, r'$m_{4\mu} = $125 GeV, $m_{2\mu} =$ %s GeV'%(str(m)), color='black', fontsize = 13)
    ax.set_ylabel(r'Signal yield / Search Region', fontsize=20)
    ### Signal
    nh, nbins = getValues(nominal)
    uh, ubins = getValues(up)
    dh, ubins = getValues(down)
    uv = (uh/nh - 1.0)*100.0
    dv = (dh/nh - 1.0)*100.0
    print(uv)
    print(dv)
    ax.hist(nbins[:-1], bins=nbins, weights = uv, color='blue', alpha=0.5, label='Upper trigger SF variation')
    ax.hist(nbins[:-1], bins=nbins, weights = dv, color='red', alpha=0.5, label='Lower trigger SF variation')
    ax.set_xlim(0, 42)
    ax.set_ylim(-50., 50.0)
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
    fig.savefig('%s/SystVar_%s_%s.png'%(outDir, sigTag, y), dpi=140)

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

outDir = ("%s/plotsSRs_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)

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
sigTags = []
if useSignalMC:
    if sigModel=="HTo2ZdTo2mu2x":
        sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        for  m in sigMasses:
            sigCTaus = [1, 10, 100, 1000]
            for t in sigCTaus:
                if ((m < 1.0 and t > 10) or (m < 30.0 and t > 100)):
                    continue
                sigTags.append("Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t))

sigCTaus = [1, 10, 100, 1000]

## Loop to make the plots
for y in years:
    inDir  = "%s/fitResults_%s/"%(thisDir, y)
    for m in sigMasses:
        hbkg = ROOT.TH1F("bkg_%s"%(str(m)), "", len(dNames), 0, len(dNames))
        hsigs = []
        hsigs_trgUp = []
        hsigs_trgDown = []
        legLabels = []
        for t in sigCTaus:
            if ((m < 1.0 and t > 10) or (m < 30.0 and t > 100)):
                continue
            sigTag = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(str(m).replace('.','p'), t)
            legLabels.append(r"$h\rightarrow Z_{D}Z_{D}$, $m_{Z_D} = $%s GeV, $c\tau =$ %s mm"%(str(m), str(t))) 
            hsigs.append(ROOT.TH1F(sigTag, "", len(dNames), 0, len(dNames)))
            hsigs_trgUp.append(ROOT.TH1F(sigTag+"_trg_up", "", len(dNames), 0, len(dNames)))
            hsigs_trgDown.append(ROOT.TH1F(sigTag+"_trg_down", "", len(dNames), 0, len(dNames)))
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
                # Retrive BG normalization:
                nBG = w.data("data_obs%s"%catExtB).sumEntries()
                # Assign
                hbkg.SetBinContent(d_+1, nBG)
                hbkg.SetBinError(d_+1, nBG**0.5)
                hsigs[-1].SetBinContent(d_+1, nSig)
                if doSystVariations:
                    w_trgUp = f.Get(wsname + '_trg_up')
                    w_trgDown = f.Get(wsname + '_trg_down')
                    nSig_trgUp = w_trgUp.var("signalNorm%s"%catExtS).getValV()
                    nSig_trgDown = w_trgDown.var("signalNorm%s"%catExtS).getValV()
                    hsigs_trgUp[-1].SetBinContent(d_+1, nSig_trgUp)
                    hsigs_trgDown[-1].SetBinContent(d_+1, nSig_trgDown)
                # Close input file with workspace
                f.Close()

            ## Systematic plots
            if doSystVariations:
                plotSystematic(outDir, sigTag, y, hsigs[-1], hsigs_trgUp[-1], hsigs_trgDown[-1])
                plotSystematicVar(outDir, sigTag, y, hsigs[-1], hsigs_trgUp[-1], hsigs_trgDown[-1])

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

         

