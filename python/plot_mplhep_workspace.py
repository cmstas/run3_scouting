import ROOT
import numpy as np
import copy
import os,sys
from datetime import date
import plotUtils
import matplotlib.pyplot as plt
import mplhep as hep

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine(".L cpp/helper.C+")

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

doRatio = False
doPull = False
useSignalMC = True
doPartialUnblinding = False
normalizeSignal = False # Only if background is > 0

wsname = "wfit"
thisDir = os.environ.get("PWD")

if len(sys.argv) < 4:
    exit
inDir = sys.argv[1]
year = sys.argv[2]
if sys.argv[3]=='Signal':
    plotBackground = False
    plotSignal = True
    plotOnlySignal = True
elif sys.argv[3]=='Background':
    plotBackground = True
    plotSignal = False
    plotOnlySignal = False
else:
    print('Argument 2 must be Signal or Background')
useData = not plotOnlySignal


useCategorizedSignal = True
useCategorizedBackground = True

outDir = ("%s/fitPlots_%s_%s_"%(thisDir, sys.argv[3], year))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)

dNames = []
#dNames.append("d_FourMu_sep")
#dNames.append("d_Dimuon_lxy0p0to0p2_inclusive")
#dNames.append("d_Dimuon_lxy0p2to1p0_inclusive")
#dNames.append("d_Dimuon_lxy1p0to2p4_inclusive")
#dNames.append("d_Dimuon_lxy2p4to3p1_inclusive")
#dNames.append("d_Dimuon_lxy3p1to7p0_inclusive")
#dNames.append("d_Dimuon_lxy7p0to11p0_inclusive")
#dNames.append("d_Dimuon_lxy11p0to16p0_inclusive")
#dNames.append("d_Dimuon_lxy16p0to70p0_inclusive")
#
dNames.append("d_FourMu_sep")
dNames.append("d_FourMu_osv")
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p2_non-pointing")
dNames.append("d_Dimuon_lxy0p2to1p0_non-pointing")
dNames.append("d_Dimuon_lxy1p0to2p4_non-pointing")
dNames.append("d_Dimuon_lxy2p4to3p1_non-pointing")
dNames.append("d_Dimuon_lxy3p1to7p0_non-pointing")
dNames.append("d_Dimuon_lxy7p0to11p0_non-pointing")
dNames.append("d_Dimuon_lxy11p0to16p0_non-pointing")
dNames.append("d_Dimuon_lxy16p0to70p0_non-pointing")

years = []
years.append(year)

# Signals
#model = "HTo2ZdTo2mu2x" # HTo2ZdTo2mu2x
#model = "ScenarioA" # HTo2ZdTo2mu2x
model = "ScenarioA"
#model = "BToPhi"

sigMasses = []
if useSignalMC:
    if (model=="HTo2ZdTo2mu2x"):
        sigMasses = [1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        sigCtau = [1, 10, 100]
        sigMasses = [7.000]
        sigCtau = [10]
    elif (model=="ScenarioB1"):
        sigMasses = []
        sigMasses.append([4, 1.33])
        sigMasses.append([5, 2.40])
        sigCtau = [0.1, 1, 10, 100]
    elif (model=="ScenarioA"):
        sigMasses = []
        #sigMasses.append([4, 1.33])
        sigMasses.append([5, 1.67])
        sigCtau = [0.1, 0.25]
    elif model == "BToPhi":
        #sigMasses = [0.3, 1.25, 1.5, 2.0]
        #sigCtau = [0.1, 1, 10, 100]
        sigMasses = [5.00]
        sigCtau = [1.0, 10.0]
else:
    if (model=="HTo2ZdTo2mu2x"):
        sigCtau = [1, 10, 100]
        lastmass = 0.5
        while (lastmass < 5.0):
            lastmass = 1.04*lastmass
            if not ROOT.passMassVeto(lastmass):
                continue
            sigMasses.append(lastmass)
        sigMasses = [7.000]
        sigCtau = [1]

def drawLabels(year="all",lumi=59.83+41.48+19.5+16.8,plotData=False):
    # Labels
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.04)
    latex.SetNDC(True)

    latexCMS = ROOT.TLatex()
    latexCMS.SetTextFont(61)
    latexCMS.SetTextSize(0.055)
    latexCMS.SetNDC(True)

    latexCMSExtra = ROOT.TLatex()
    latexCMSExtra.SetTextFont(52)
    latexCMSExtra.SetTextSize(0.04)
    latexCMSExtra.SetNDC(True)

    legoffset = 0.0
    latexSel = ROOT. TLatex()
    latexSel.SetTextAlign(31)
    latexSel.SetTextFont(42)
    latexSel.SetTextSize(0.04)
    latexSel.SetNDC(True)

    yearenergy=""
    if year!="all" or lumi<100.0:
        if year!="all":
            yearenergy="%.1f fb^{-1} (%s, 13 TeV)"%(lumi,year)
        else:
            yearenergy="%.1f fb^{-1} (2022, 13.6 TeV)"%(lumi)
    else:
        yearenergy="%.0f fb^{-1} (13 TeV)"%(lumi)
    if plotData:
        cmsExtra="Preliminary"
    else:
        cmsExtra="Simulation"

    # Draw CMS headers
    expoffset=0
    if doRatio:
        latex.DrawLatex(0.95, 0.93+expoffset, yearenergy);
        latexCMS.DrawLatex(0.15,0.93+expoffset,"CMS");
        latexCMSExtra.DrawLatex(0.24,0.93+expoffset, cmsExtra);
    else:
        latex.DrawLatex(0.95, 0.93+expoffset, yearenergy);
        latexCMS.DrawLatex(0.11,0.93+expoffset,"CMS");
        latexCMSExtra.DrawLatex(0.21,0.93+expoffset, cmsExtra);


def getLegend(ch,gd,p,hp,hs,smodel,smass,sigsf=-1.0,plotSignal=True,plotData=True,plotOnlySignal=False,hmc=None,hgauss=None,hdcb=None):
    legend = ROOT.TLegend(0.5,0.65,0.91,0.91)
    legend.SetLineColor(0)
    legend.SetTextSize(0.04)
    legend.SetLineWidth(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    if plotOnlySignal:
        legend.SetHeader(smodel)
        legend.AddEntry(hmc,"Signal Monte Carlo","EP")
        legend.AddEntry(hs,"Total signal fit", "L")
        legend.AddEntry(hgauss,"Gaussian", "L")
        legend.AddEntry(hdcb,"Double Crystal Ball", "L")
    else:
        if plotData:
            legend.AddEntry(gd,"Data","EP")
        else:
            legend.AddEntry(gd,"Data (toy)","EP")
        for pn,pp in enumerate(p):
            legend.AddEntry(hp[pn],pp,"L")
        if plotSignal:
            if sigsf>0:
                legend.AddEntry(hs,"%s, (x%.4f)"%(smodel,sigsf), "L")
            else:
                legend.AddEntry(hs,"%s"%(smodel), "L")
    return legend

mean = 0.0
sigma = 0.0
for year in years:
    for t in sigCtau:
        for mf in sigMasses:
            if (model=="HTo2ZdTo2mu2x") and ((mf < 1.0 and t > 10) or (mf < 30.0 and t > 100)):
                continue
            if (model=="HTo2ZdTo2mu2x" or model=='BToPhi'):
                m = str(mf)
            if model=='BToPhi':
                m = "%.2f"%(mf)
            elif (model=="ScenarioB1"):
                m = "%.3f_%.2f"%(mf[0], mf[1])
            for d_,d in enumerate(dNames):
                masked = False # Assume the masking
                if (model=="HTo2ZdTo2mu2x"):
                    if useSignalMC:
                        #sample = "Signal_HTo2ZdTo2mu2x_MZd-%.3f_ctau-%.1fmm" % (float(m), float(t))
                        #sample = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(m.replace(".", "p"),t)
                        sample = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%.2fmm"%(m.replace(".", "p"),t)
                    else:
                        sample = "Signal_HTo2ZdTo2mu2x_MZd-%.3f_ctau-%.2fmm"%(float(mf),float(t))
                elif (model=="BToPhi"):
                    #sample = ("Signal_BToPhi-%s_ctau-%smm"%(m.replace('.','p'), t))
                    sample = "Signal_BToPhi_MPhi-%s_ctau-%.2fmm" % (m.replace(".", "p"), float(t))
                    #sample = "Signal_BToPhi_MPhi-%.2f_ctau-%.2fmm" % (float(mf), float(t))
                    #finame = "%s/%s_%s_%s_2022_workspace.root"%(inDir,d,sample,y)
                elif (model=="ScenarioB1"):
                    sample = "Signal_ScenarioB1_Mpi-%s_MA-%s_ctau-%.2fmm" % (("%.0f"%(mf[0])), ("%.2f"%(mf[1])).replace('.','p'),float(t))
                elif (model=="ScenarioA"):
                    sample = "Signal_ScenarioA_Mpi-%s_MA-%s_ctau-%.2fmm" % (("%.0f"%(mf[0])), ("%.2f"%(mf[1])).replace('.','p'),float(t))
                finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,sample,year)
                if (d == "d_FourMu_sep" ): binidx=1
                elif (d == "d_FourMu_osv" ): binidx=2
                elif (d == "d_Dimuon_lxy0p0to0p2_iso0_ptlow" ): binidx=3
                elif (d == "d_Dimuon_lxy0p0to0p2_iso0_pthigh" ): binidx=4
                elif (d == "d_Dimuon_lxy0p0to0p2_iso1_ptlow" ): binidx=5
                elif (d == "d_Dimuon_lxy0p0to0p2_iso1_pthigh" ): binidx=6
                elif (d == "d_Dimuon_lxy0p2to1p0_iso0_ptlow" ): binidx=7
                elif (d == "d_Dimuon_lxy0p2to1p0_iso0_pthigh" ): binidx=8
                elif (d == "d_Dimuon_lxy0p2to1p0_iso1_ptlow" ): binidx=9
                elif (d == "d_Dimuon_lxy0p2to1p0_iso1_pthigh" ): binidx=10
                elif (d == "d_Dimuon_lxy1p0to2p4_iso0_ptlow" ): binidx=11
                elif (d == "d_Dimuon_lxy1p0to2p4_iso0_pthigh" ): binidx=12
                elif (d == "d_Dimuon_lxy1p0to2p4_iso1_ptlow" ): binidx=13
                elif (d == "d_Dimuon_lxy1p0to2p4_iso1_pthigh" ): binidx=14
                elif (d == "d_Dimuon_lxy2p4to3p1_iso0_ptlow" ): binidx=15
                elif (d == "d_Dimuon_lxy2p4to3p1_iso0_pthigh" ): binidx=16
                elif (d == "d_Dimuon_lxy2p4to3p1_iso1_ptlow" ): binidx=17
                elif (d == "d_Dimuon_lxy2p4to3p1_iso1_pthigh" ): binidx=18
                elif (d == "d_Dimuon_lxy3p1to7p0_iso0_ptlow" ): binidx=19
                elif (d == "d_Dimuon_lxy3p1to7p0_iso0_pthigh" ): binidx=20
                elif (d == "d_Dimuon_lxy3p1to7p0_iso1_ptlow" ): binidx=21
                elif (d == "d_Dimuon_lxy3p1to7p0_iso1_pthigh" ): binidx=22
                elif (d == "d_Dimuon_lxy7p0to11p0_iso0_ptlow" ): binidx=23
                elif (d == "d_Dimuon_lxy7p0to11p0_iso0_pthigh" ): binidx=24
                elif (d == "d_Dimuon_lxy7p0to11p0_iso1_ptlow" ): binidx=25
                elif (d == "d_Dimuon_lxy7p0to11p0_iso1_pthigh" ): binidx=26
                elif (d == "d_Dimuon_lxy11p0to16p0_iso0_ptlow" ): binidx=27
                elif (d == "d_Dimuon_lxy11p0to16p0_iso0_pthigh" ): binidx=28
                elif (d == "d_Dimuon_lxy11p0to16p0_iso1_ptlow" ): binidx=29
                elif (d == "d_Dimuon_lxy11p0to16p0_iso1_pthigh" ): binidx=30
                elif (d == "d_Dimuon_lxy16p0to70p0_iso0_ptlow" ): binidx=31
                elif (d == "d_Dimuon_lxy16p0to70p0_iso0_pthigh" ): binidx=32
                elif (d == "d_Dimuon_lxy16p0to70p0_iso1_ptlow" ): binidx=33
                elif (d == "d_Dimuon_lxy16p0to70p0_iso1_pthigh" ): binidx=34
                elif (d == "d_Dimuon_lxy0p0to0p2_non-pointing" ): binidx=35
                elif (d == "d_Dimuon_lxy0p2to1p0_non-pointing" ): binidx=36
                elif (d == "d_Dimuon_lxy1p0to2p4_non-pointing" ): binidx=37
                elif (d == "d_Dimuon_lxy2p4to3p1_non-pointing" ): binidx=38
                elif (d == "d_Dimuon_lxy3p1to7p0_non-pointing" ): binidx=39
                elif (d == "d_Dimuon_lxy7p0to11p0_non-pointing" ): binidx=40
                elif (d == "d_Dimuon_lxy11p0to16p0_non-pointing" ): binidx=41
                elif (d == "d_Dimuon_lxy16p0to70p0_non-pointing" ): binidx=42
                catExtS = ""
                catExtB = ""
                if useCategorizedSignal:
                    catExtS = "_ch%d_%s"%(binidx, year)
                if useCategorizedBackground:
                    catExtB = "_ch%d_%s"%(binidx, year)
                print(catExtS, catExtB)
                # Open input file with workspace
                f = ROOT.TFile(finame)
                # Retrieve workspace from file
                w = f.Get(wsname)
                # Retrive x, min and max
                if "Dimuon" in d:
                    x = w.var("mfit")
                else:
                    x = w.var("m4fit")
                minx = x.getMin()
                maxx = x.getMax()
                #nBins = int((maxx-minx)/(0.01*float(m)))
                nBins = 5*10;
                # Retrieve signal normalization
                lumi=34.6 if year=='2022' else 27.8              
                if doPartialUnblinding:
                    lumi = 0.1*lumi
                nSig = w.var("signalNorm%s"%catExtS).getValV()

                # Retrieve signal mean and std. deviation
                if binidx==0 or useCategorizedSignal:
                    mean = w.var("mean%s"%catExtS).getValV()
                    sigma = w.var("sigma%s"%catExtS).getValV()

                # Retrive BG normalization:
                try:
                    nBG = w.data("data_obs%s"%catExtB).sumEntries()
                except TypeError: # if it doesn't exist... (assuming there is signal)
                    print("Background not found for this mass, will do only signal fits")
                    masked = True

                # Get data
                if not masked:
                    data = w.data("data_obs%s"%catExtB)
                    hd = x.createHistogram("hd",ROOT.RooFit.Binning(nBins,minx,maxx))                
                    data.fillHistogram(hd,ROOT.RooArgList(x))

                # Get mc
                if plotOnlySignal:
                    mc = w.data("signalRooDataSet%s"%catExtS)
                    frame = x.frame(minx,maxx);
                    mc.plotOn(frame, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Binning(nBins,minx,maxx))
                    hmc = frame.getHist()
                    #hmc = x.createHistogram("hmc",ROOT.RooFit.Binning(nBins,minx,maxx))                
                    #hmc.Sumw2()
                    #mc.fillHistogram(hmc,ROOT.RooArgList(x))
                 
                # Get background pdfs
                if not masked:
                    bpdf = w.pdf("roomultipdf%s"%catExtB)
                    nPDF = w.cat("pdf_index%s"%catExtB).numTypes()
                    p  = []
                    pn = []
                    hp = []
                    hpr = []
                    numpars = []
                    gp = []
                    print(nPDF)
                    for pp in range(nPDF):
                        p.append(bpdf.getPdf(pp))
                        numpars.append(w.pdf(bpdf.getPdf(pp).GetName()).getVariables().getSize()-1)
                        if "exponential" in p[pp].GetName():
                            pn.append("Exponential")
                            color=ROOT.kOrange-7
                        elif "powerlaw" in p[pp].GetName():
                           pn.append("Power-law")
                           color=ROOT.kOrange-2
                        elif "bernstein" in p[pp].GetName():
                           pn.append("Bernstein<%d>"%(numpars[pp]))
                           color=ROOT.kRed+1
                        else:
                           pn.append("Uniform")
                           color=ROOT.kGray+2
                        hp.append(p[pp].createHistogram("hp%d"%pp,x,ROOT.RooFit.Binning(100*nBins,minx,maxx)))
                        hp[pp].SetLineColor(color)
                        hp[pp].SetLineWidth(2)
                        hp[pp].Scale(nBG)
                        hpr.append(hp[pp].Clone("hpr%d"%pp))
                        hpr[pp].Rebin(100)
                        hp[pp].Scale(100.0)
                        gp.append(ROOT.TGraph(hp[pp]))

                # Get signal pdfs 
                sp = w.pdf("signal%s"%catExtS)
                hs = sp.createHistogram("hs",x,ROOT.RooFit.Binning(100*nBins,minx,maxx))
                hs.SetLineColor(ROOT.kMagenta)
                hs.SetLineWidth(2)
                hs.Scale(nSig*100)
                g_signal = ROOT.TGraph(hs)

                sp_gauss = w.pdf("gauss%s"%catExtS)
                sp_sigma = w.var("sigma%s"%catExtS).getValV()
                sp_mean = w.var("mean%s"%catExtS).getValV()
                mcfrac = w.var("mcfrac%s"%catExtS).getValV()
                hs_gauss = sp_gauss.createHistogram("hs_gauss",x,ROOT.RooFit.Binning(100*nBins,minx,maxx))
                hs_gauss.Scale(nSig*mcfrac*100)
                g_gauss = ROOT.TGraph(hs_gauss)
                g_gauss.SetLineColor(ROOT.kCyan)
                g_gauss.SetLineWidth(2)
                g_gauss.SetLineStyle(1)

                #sp_dcb = ROOT.RooDoubleCBFast("dcb", "dcb", x, w.var("mean%s"%catExtS), w.var("sigma%s"%catExtS), w.var("alphaL%s"%catExtS), w.var("nL%s"%catExtS), w.var("nR%s"%catExtS), w.var("alphaR%s"%catExtS))
                sp_dcb = w.pdf("dcb%s"%catExtS)
                sp_alphaL = w.var("alphaL%s"%catExtS).getValV()
                sp_alphaR = w.var("alphaR%s"%catExtS).getValV()
                sp_nL = w.var("nL%s"%catExtS).getValV()
                sp_nR = w.var("nR%s"%catExtS).getValV()
                #recfrac = w.function("signal%s_recursive_fraction_dcb%s"%(catExtS,catExtS))
                recfrac = 1.0 - mcfrac
                hs_dcb = sp_dcb.createHistogram("hs_dcb",x,ROOT.RooFit.Binning(100*nBins,minx,maxx))
                hs_dcb.Scale(nSig*recfrac*100)
                g_dcb = ROOT.TGraph(hs_dcb)
                g_dcb.SetLineColor(ROOT.kBlue)
                g_dcb.SetLineWidth(2)
                g_dcb.SetLineStyle(1)

                scale = -1.0
                if plotBackground and plotSignal and not plotOnlySignal and normalizeSignal and nBG > 1e-6 and not masked:
                    scale = float(nBG)/float(nSig)
                    hs.Scale(scale)


                ## Make graphs out of RooData
                if not masked:
                    g_data = ROOT.TGraphAsymmErrors()
                    plotUtils.ConvertToPoissonGraph(hd, g_data, drawZeros=True, drawXerr=False)
                    g_data.SetMarkerStyle(20)
                    g_data.SetMarkerSize(1.2)
                    g_data.SetLineWidth(2)
                    # draw with zero marker size so error bars drawn all the way to x axis in the case of 0 content
                    g_data_clone = g_data.Clone()
                    g_data_clone.SetMarkerSize(0.0)


                ## Plot with mplhep
                fig, ax = plt.subplots(1, 1, figsize=(11, 8))
                plt.style.use(hep.style.CMS)
                if plotBackground:
                    luminosity = 34.6 if year=="2022" else 27.8
                    hep.cms.label("Preliminary", data=True, year=year, lumi = luminosity, com='13.6', ax=ax)
                else:
                    hep.cms.label("Simulation Preliminary", data=True, year=year, com='13.6', ax=ax)
                
                # Plot the data:
                if plotBackground and not masked:
                    x = []
                    y = []
                    x_err_low = []
                    x_err_high = []
                    y_err_low = []
                    y_err_high = []
                    for i in range(g_data.GetN()):
                        x_point = np.array([0.])
                        y_point = np.array([0.])
                        g_data.GetPoint(i, x_point, y_point)
                        x.append(x_point[0])
                        y.append(y_point[0])
                        x_err_low.append(g_data.GetErrorXlow(i))
                        x_err_high.append(g_data.GetErrorXhigh(i))
                        y_err_low.append(g_data.GetErrorYlow(i))
                        y_err_high.append(g_data.GetErrorYhigh(i))
                    ax.errorbar(
                                x, y,
                                xerr=[x_err_low, x_err_high], 
                                yerr=[y_err_low, y_err_high], 
                                fmt='o',  # Marcador circular
                                color='black',
                                label="Data",
                                ms = 7,
                                capsize=2
                                )
                else:
                    x = []
                    y = []
                    x_err_low = []
                    x_err_high = []
                    y_err_low = []
                    y_err_high = []
                    for i in range(hmc.GetN()):
                        x_point = np.array([0.])
                        y_point = np.array([0.])
                        hmc.GetPoint(i, x_point, y_point)
                        x.append(x_point[0])
                        y.append(y_point[0])
                        x_err_low.append(hmc.GetErrorXlow(i))  # Error bajo en X
                        x_err_high.append(hmc.GetErrorXhigh(i))  # Error alto en X
                        # Errores en Y
                        y_err_low.append(hmc.GetErrorYlow(i))  # Error bajo en Y
                        y_err_high.append(hmc.GetErrorYhigh(i))  # Error alto en Y
                    ax.errorbar(
                                x, y,
                                xerr=[x_err_low, x_err_high], 
                                yerr=[y_err_low, y_err_high], 
                                fmt='o',  # Marcador circular
                                color='black',
                                label="Signal Monte Carlo",
                                ms = 7,
                                capsize=2
                                )
                bwidth = x[1] - x[0]
                
                # Plot the signal:
                if plotBackground:
                    for pp in range(nPDF):
                        if "exponential" in p[pp].GetName():
                            col='sienna'
                        elif "powerlaw" in p[pp].GetName():
                            col='orange'
                        elif "bernstein" in p[pp].GetName():
                            col='firebrick'
                        else:
                            col='slategrey'
                        ax.plot(gp[pp].GetX(), gp[pp].GetY(), label=pn[pp], color=col, lw = 3)
                        ax.set_ylim(0, 2*max(y))
                else:
                    if plotOnlySignal:
                        ax.plot(g_gauss.GetX(), g_gauss.GetY(), label='Gaussian', color='dodgerblue', lw = 3, ls=':')
                        ax.plot(g_dcb.GetX(), g_dcb.GetY(), label='Double Crystal Ball', color='blue', lw = 3, ls=':')
                    ax.plot(g_signal.GetX(), g_signal.GetY(), label='Total signal fit', color='magenta', lw = 3)
                
                # Text labels
                catnames = d.split("_")
                lxybin = catnames[2]
                lxybin = (lxybin[3:]).split("to")
                if "d_Dimuon" in d:
                    ax.text(0.03, 0.95, 'Dimuon', fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
                    ax.text(0.03, 0.9, r"$l_{{xy}} \in [{},{}]$ cm".format(lxybin[0].replace("p", "."), lxybin[1].replace("p", ".")), fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                    if "non-pointing" not in d:
                        isobin = "Isolated" if catnames[3]=="iso1" else "Non isolated"
                        ax.text(0.03, 0.85, isobin, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                        ptbin = r"High $p_{T}^{\mu\mu}$" if catnames[4]=="pthigh" else r"Low $p_{T}^{\mu\mu}$"
                        ax.text(0.03, 0.8, ptbin, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                    else:
                        ax.text(0.03, 0.85, 'Non-pointing', fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                elif "d_FourMu" in d:
                    ax.text(0.03, 0.95, 'Four muon', fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
                    fourmucat = "Resolved" if "sep" in d else "Overlapping"
                    ax.text(0.03, 0.9, fourmucat, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                
                # Signal label
                if plotSignal:
                    if (model=="HTo2ZdTo2mu2x"):
                        signal_label = r"$M_{Z_D} = %.1f$ GeV, $c\tau = %.0f$ cm"%(mf, t*0.1) # provisionally to cm
                        signal_label = signal_label.replace('.0', '')
                        ax.text(0.03, 0.7, r"$h\rightarrow Z_D Z_D$", fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
                        ax.text(0.03, 0.65, signal_label, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                    if (model=="ScenarioB1"):
                        ax.text(0.03, 0.7, "Scenario B1", fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
                        signal_label = r"$M_{\pi} = %.0f$ GeV, $M_{A} = %.2f$ GeV, $c\tau = %.1f$ mm"%(mf[0], mf[1], t)
                        ax.text(0.03, 0.65, signal_label, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                    if (model=="ScenarioA"):
                        ax.text(0.03, 0.7, "Scenario A", fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
                        signal_label = r"$M_{\pi} = %.0f$ GeV, $M_{A} = %.2f$ GeV, $c\tau = %.1f$ mm"%(mf[0], mf[1], t)
                        ax.text(0.03, 0.65, signal_label, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
                    if (model=="BToPhi"):
                        ax.text(0.03, 0.7, r"$B\rightarrow\phi X (\phi \rightarrow \mu\mu)$", fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
                        signal_label = r"$M_{\phi} = %.2f$ GeV, $c\tau = %.1f$ mm"%(mf, t)
                        ax.text(0.03, 0.65, signal_label, fontsize=20, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

                # Axis
                ax.set_ylabel(r'Events / %.2f GeV'%(bwidth), fontsize=24)
                if "d_Dimuon" in d:
                    ax.set_xlabel(r'$m_{\mu\mu} (GeV)$')
                else:
                    ax.set_xlabel(r'$m_{4\mu} (GeV)$')
                ax.margins(x=0)
                ax.set_ylim(0, None)
                
                # Legend
                ax.legend(loc='upper right', fontsize = 26, frameon = False, ncol=1)
                
                # Save
                fig.savefig("%s/fitSIG_%s_%s.png" % (outDir, sample, d), dpi=140)
                fig.savefig("%s/fitSIG_%s_%s.pdf" % (outDir, sample, d), dpi=140)
                
                


                #minR=0.0
                #maxR=0.0
                #ty = numpy.array([])
                #tmax=maxR
                #if plotOnlySignal:
                #    ty = [hmc.GetMaximum()]
                #else:
                #    ty = g_data.GetY() 
                #if len(ty)>0:
                #    tmax = numpy.amax(ty)
                #    if tmax>maxR:
                #        maxR=tmax
                #if plotSignal:
                #    if hs.GetMaximum() > maxR:
                #        maxR = hs.GetMaximum()
                #if plotOnlySignal:
                #    maxR = maxR*2.0
                #else:
                #    if maxR>50.0:
                #        maxR = maxR*1.5
                #    elif maxR<50.0 and maxR>2.0:
                #        maxR = maxR*3.0
                #    elif maxR<=2.0 and maxR > 0.01:
                #        maxR = maxR*5.0
                #    else:
                #        maxR = maxR*10.0
                #
                #if nSig < 1e-5:
                #    scale = -1
                #    hs.Scale(0.0)
#
                #h_axis.SetMinimum(minR)
                #h_axis.SetMaximum(maxR)
                #h_axis.GetYaxis().SetRangeUser(minR,maxR)
                #if doRatio==True:
                #    h_axis.GetYaxis().SetTitleSize(0.04)
                #    h_axis.GetXaxis().SetTitleSize(0.04)
                #    h_axis.GetXaxis().SetTitleOffset(1.25)
                #    h_axis.GetYaxis().SetLabelSize(0.03)
                #else:
                #    h_axis.GetXaxis().SetTitleSize(0.045)
                #    h_axis.GetXaxis().SetLabelSize(0.04)
                #    h_axis.GetYaxis().SetTitleSize(0.045)
                #    h_axis.GetYaxis().SetLabelSize(0.04)
                #    h_axis.GetXaxis().SetTitleOffset(1.1)
#
                #h_axis.Draw("")
                #if plotOnlySignal:
                #    hmc.Draw("P,same")
                #else:
                #    g_data.Draw("P,same")
                #    g_data_clone.Draw("P,same")
                #    for pp in range(nPDF):
                #        hp[pp].Draw("hist,same")
                #if plotSignal:
                #    hs.Draw("hist,same")
                #if plotOnlySignal:
                #    g_gauss.Draw("l,same")
                #    g_dcb.Draw("l,same")
#
                #llabel = "M_{Z_{D}} = %s, c#tau = %s mm"%(m, t)
                #if plotOnlySignal:
                #    legend = getLegend(binidx,g_data,pn,hp,hs,llabel,float(m), -1, True, False, True, hmc, g_gauss, g_dcb)
                #else:
                #    legend = getLegend(binidx,g_data,pn,hp,hs,llabel,float(m), -1, plotSignal)
                ##year="2022"
                #drawLabels(year,lumi,useData)
                #legend.Draw("same")
                #pads[0].Update()
                #pads[0].RedrawAxis()
                #
                ### Search region labels
                ##
                #latexExtra = ROOT.TLatex()
                #latexExtra.SetTextFont(42)
                #latexExtra.SetTextSize(0.04)
                #latexExtra.SetNDC(True)
                ##
                #latexExtraBold = ROOT.TLatex()
                #latexExtraBold.SetTextFont(62)
                #latexExtraBold.SetTextSize(0.04)
                #latexExtraBold.SetNDC(True)
                ##
                #catnames = d.split("_")
                #lxybin = catnames[2]
                #lxybin = (lxybin[3:]).split("to")
                #if "d_Dimuon" in d:
                #    latexExtraBold.DrawLatex(0.14,0.86,"Dimuon")
                #    if "non-pointing" not in d:
                #        latexExtra.DrawLatex(0.14,0.81,"l_{{xy}} #in [{},{}]".format(lxybin[0].replace("p", "."), lxybin[1].replace("p", ".")))
                #        isobin = "Isolated" if catnames[3]=="iso1" else "Non isolated"
                #        latexExtra.DrawLatex(0.14,0.76,isobin)
                #        ptbin = "High p_{T}^{#mu#mu}" if catnames[4]=="pthigh" else "Low p_{T}^{#mu#mu}"
                #        latexExtra.DrawLatex(0.14,0.71,ptbin)
                #    else:
                #        latexExtra.DrawLatex(0.14,0.81,"l_{{xy}} #in [{},{}]".format(lxybin[0].replace("p", "."), lxybin[1].replace("p", ".")))
                #        latexExtra.DrawLatex(0.14,0.76,"Non-pointing")
                #elif "d_FourMu" in d:
                #    latexExtraBold.DrawLatex(0.14,0.86,"Four muon")
                #    fourmucat = "Resolved" if "sep" in d else "Overlapping"
                #    latexExtra.DrawLatex(0.14,0.81,fourmucat)
#
                ### Save canvas
                #if plotOnlySignal:
                #    #can.SaveAs("%s/fitSIG_M%s_CT_%imm_%s.png"%(outDir,m,t,d))
                #    can.SaveAs("%s/fitSIG_M%.3f_CT_%.1fmm_%s.png" % (outDir, float(m), float(t), d))
                #    #can.SaveAs("%s/fitSIG_M%s_CT_%imm_%s.pdf"%(outDir,m,t,d))
                #    can.SaveAs("%s/fitSIG_M%.3f_CT_%.1fmm_%s.pdf" % (outDir, float(m), float(t), d))
                #else:
                #    #can.SaveAs("%s/fitBG_M%s_%s.png"%(outDir,m,d))
                #    can.SaveAs("%s/fitBG_M%.3f_%s.png" % (outDir, float(m), d))
                #    #can.SaveAs("%s/fitBG_M%s_%s.pdf"%(outDir,m,d))
                #    can.SaveAs("%s/fitBG_M%.3f_%s.pdf" % (outDir, float(m), d))
#
                ## Close input file with workspace                
                #f.Close()
