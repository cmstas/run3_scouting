import ROOT
import numpy
import copy
import os,sys
from datetime import date
import plotUtils

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine(".L cpp/helper.C+")

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

doRatio = False
doPull = False
useSignalMC = False
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
model = "HTo2ZdTo2mu2x"

sigMasses = []
if useSignalMC:
    if (model=="HTo2ZdTo2mu2x"):
        sigMasses = [0.5, 0.7, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
        sigCtau = [1, 10, 100]
    elif (model=="ScenarioB1"):
        sigMasses = [1.33]
        sigCtau = ["0p1", "1", "10", "100"]
else:
    if (model=="HTo2ZdTo2mu2x"):
        sigCtau = [1, 10, 100]
        lastmass = 0.5
        while (lastmass < 5.0):
            lastmass = 1.04*lastmass
            if not ROOT.passMassVeto(lastmass):
                continue
            sigMasses.append(lastmass)

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
for y in years:
    for t in sigCtau:
        for mf in sigMasses:
            if (model=="HTo2ZdTo2mu2x") and ((mf < 1.0 and t > 10) or (mf < 30.0 and t > 100)):
                continue
            m = str(mf)
            for d_,d in enumerate(dNames):
                if (model=="HTo2ZdTo2mu2x"):
                    if useSignalMC:
                        sample = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%imm"%(m.replace(".", "p"),t)
                    else:
                        sample = "Signal_HTo2ZdTo2mu2x_MZd-%.2f_ctau-%imm"%(mf,t)
                else:
                    sample = "Signal_ScenarioB1_mpi-4_mA-%s_ctau-%imm"%(m.replace(".", "p"),t)
                finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,sample,y)
                print(finame)
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
                lumi=35. if year=='2022' else 27.2 # 27.2              
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
                except TypeError: # if it doesn't exist... (assuming there ir signal)
                    print("Background not found for this mass, skipping to next")
                    break

                # Get data
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
                bpdf = w.pdf("roomultipdf%s"%catExtB)
                nPDF = w.cat("pdf_index%s"%catExtB).numTypes()
                p  = []
                pn = []
                hp = []
                hpr = []
                numpars = []
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

                # Get signal pdfs 
                sp = w.pdf("signal%s"%catExtS)
                hs = sp.createHistogram("hs",x,ROOT.RooFit.Binning(100*nBins,minx,maxx))
                hs.SetLineColor(ROOT.kMagenta)
                hs.SetLineWidth(2)
                hs.Scale(nSig*100)

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
                if plotBackground and plotSignal and not plotOnlySignal and normalizeSignal and nBG > 1e-6:
                    scale = float(nBG)/float(nSig)
                    hs.Scale(scale)

                ROOT.gStyle.SetOptStat(0)
                if doRatio:
                    can = ROOT.TCanvas("can","",600, 600)
                else:
                    can = ROOT.TCanvas("can","",700, 600)
                can.cd()

                ## Make graphs out of RooData
                g_data = ROOT.TGraphAsymmErrors()
                plotUtils.ConvertToPoissonGraph(hd, g_data, drawZeros=True, drawXerr=False)
                g_data.SetMarkerStyle(20)
                g_data.SetMarkerSize(1.2)
                g_data.SetLineWidth(2)
                # draw with zero marker size so error bars drawn all the way to x axis in the case of 0 content
                g_data_clone = g_data.Clone()
                g_data_clone.SetMarkerSize(0.0)

                ## Create axis plot
                h_axis = ROOT.TH1D("h_axis","", hd.GetNbinsX(), hd.GetXaxis().GetBinLowEdge(1), hd.GetXaxis().GetBinUpEdge(hd.GetNbinsX()))
                h_axis.GetXaxis().SetTitle("m_{#mu#mu} [GeV]")
                h_axis.GetYaxis().SetTitle("Events")

                h_axis_ratio = ROOT.TH2D("h_axis_ratio","", hd.GetNbinsX(), hd.GetXaxis().GetBinLowEdge(1), hd.GetXaxis().GetBinUpEdge(hd.GetNbinsX()), 2000, -100.0, 100.0)
                g_ratio = [] 
                for pp in range(nPDF):
                    g_ratio.append(ROOT.TGraphAsymmErrors())
                    if not doPull:
                        plotUtils.GetPoissonRatioGraph(hpr[pp], hd, g_ratio[pp], drawZeros=False, drawXerr=False, useMCErr=False)
                    else:
                        plotUtils.GetPullGraph(hpr[pp], hd, g_ratio[pp], drawZeros=True, drawXerr=False, useMCErr=False)                        
                    g_ratio[pp].SetMarkerStyle(4)
                    g_ratio[pp].SetMarkerSize(1.2)
                    g_ratio[pp].SetMarkerColor(hpr[pp].GetLineColor())
                    g_ratio[pp].SetLineWidth(1)
                    g_ratio[pp].SetLineColor(hpr[pp].GetLineColor())

                pads = []
                if doRatio==True:
                    if not doPull:
                        minR=0.25
                        maxR=1.75
                        ty = numpy.array([])
                        tmax=maxR
                        for pp in range(nPDF):
                            ty = g_ratio[pp].GetY()
                            if len(ty)>0:
                                tmax = numpy.amax(ty)
                            if tmax>maxR:
                                maxR=tmax*1.05
                        if maxR>5.0:
                            minR=0.1
                    else:
                        minR=-2.0
                        maxR=+2.0
                        ty = numpy.array([])
                        tmax=maxR
                        tmin=minR
                        for pp in range(nPDF):
                            ty = g_ratio[pp].GetY()
                            if len(ty)>0:
                                tmax = numpy.amax(ty)
                                tmin = numpy.amin(ty)
                            if tmax>maxR:
                                maxR=tmax*1.10
                            if tmin<minR:
                                minR=tmin
                                if minR<0.0:
                                    minR = minR*1.10
                                else:
                                    minR = minR*0.90
                        if maxR>5.0 and not doPull:
                            minR=0.1
                    h_axis_ratio.GetYaxis().SetRangeUser(minR,maxR)
                    #h_axis_ratio.SetMinimum(minR)
                    #h_axis_ratio.SetMaximum(maxR)
                    if not doPull:
                        h_axis_ratio.SetTitle(";;Data / fit")
                    else:
                        h_axis_ratio.SetTitle(";;(Data-fit)/#sigma_{data}")
                    h_axis_ratio.GetYaxis().SetTitleSize(0.16)
                    h_axis_ratio.GetYaxis().SetTitleOffset(0.25)
                    h_axis_ratio.GetYaxis().SetLabelSize(0.12)
                    h_axis_ratio.GetYaxis().CenterTitle()
                    h_axis_ratio.GetYaxis().SetTickLength(0.02)
                    h_axis_ratio.GetXaxis().SetLabelSize(0)
                    h_axis_ratio.GetXaxis().SetTitle("")
                    h_axis_ratio.GetXaxis().SetTickSize(0.06)

                    line = ROOT.TLine(minx, 1.0, maxx, 1.0)
                    if doPull:
                        line = ROOT.TLine(minx, 0.0, maxx, 0.0)
                        linep1 = ROOT.TLine(minx, 1.0, maxx, 1.0)
                        linep2 = ROOT.TLine(minx, 2.0, maxx, 2.0)
                        linem1 = ROOT.TLine(minx, -1.0, maxx, -1.0)
                        linem2 = ROOT.TLine(minx, -2.0, maxx, -2.0)

                    pads.append(ROOT.TPad("1","1",0.0,0.18,1.0,1.0))
                    pads.append(ROOT.TPad("2","2",0.0,0.0,1.0,0.19))
                    pads[0].SetTopMargin(0.08)
                    pads[0].SetBottomMargin(0.13)
                    pads[0].SetRightMargin(0.05)
                    pads[0].SetLeftMargin(0.10)
                    pads[1].SetRightMargin(0.05)
                    pads[1].SetLeftMargin(0.10)
                    pads[0].Draw()
                    pads[1].Draw()
                    pads[1].cd()
                    if maxR>5.0 and not doPull:
                        pads[1].SetLogy()
                    pads[1].SetTickx()
                    h_axis_ratio.Draw("")
                    for pp in range(nPDF):
                        g_ratio[pp].Draw("SAME,P0")

                    line.SetLineStyle(2)
                    line.SetLineColor(1)
                    line.SetLineWidth(1)
                    line.Draw("SAME")
                    if doPull:
                        linep1.SetLineStyle(2)
                        linep1.SetLineColor(1)
                        linep1.SetLineWidth(1)
                        linep2.SetLineStyle(2)
                        linep2.SetLineColor(1)
                        linep2.SetLineWidth(1)
                        linem1.SetLineStyle(2)
                        linem1.SetLineColor(1)
                        linem1.SetLineWidth(1)
                        linem2.SetLineStyle(2)
                        linem2.SetLineColor(1)
                        linem2.SetLineWidth(1)
                        if minR<-2.0:
                            linem1.Draw("SAME")
                            linem2.Draw("SAME")
                        elif minR<-1.0:
                            linem1.Draw("SAME")
                        if maxR>2.0:
                            linep1.Draw("SAME")
                            linep2.Draw("SAME")
                        elif maxR>1.0:
                            linep1.Draw("SAME")
                    pads[1].Modified();
                    pads[1].Update();
                else:
                    pads.append(ROOT.TPad("1","1",0,0,1,1))
                    pads[0].SetTopMargin(0.08)
                    pads[0].SetLeftMargin(0.10)
                    pads[0].SetRightMargin(0.05)
                    pads[0].Draw()

                pads[0].cd()

                minR=0.0
                maxR=0.0
                ty = numpy.array([])
                tmax=maxR
                if plotOnlySignal:
                    ty = [hmc.GetMaximum()]
                else:
                    ty = g_data.GetY() 
                if len(ty)>0:
                    tmax = numpy.amax(ty)
                    if tmax>maxR:
                        maxR=tmax
                if plotSignal:
                    if hs.GetMaximum() > maxR:
                        maxR = hs.GetMaximum()
                if plotOnlySignal:
                    maxR = maxR*2.0
                else:
                    if maxR>50.0:
                        maxR = maxR*1.5
                    elif maxR<50.0 and maxR>2.0:
                        maxR = maxR*3.0
                    elif maxR<=2.0 and maxR > 0.01:
                        maxR = maxR*5.0
                    else:
                        maxR = maxR*10.0
                
                if nSig < 1e-5:
                    scale = -1
                    hs.Scale(0.0)

                h_axis.SetMinimum(minR)
                h_axis.SetMaximum(maxR)
                h_axis.GetYaxis().SetRangeUser(minR,maxR)
                if doRatio==True:
                    h_axis.GetYaxis().SetTitleSize(0.04)
                    h_axis.GetXaxis().SetTitleSize(0.04)
                    h_axis.GetXaxis().SetTitleOffset(1.25)
                    h_axis.GetYaxis().SetLabelSize(0.03)
                else:
                    h_axis.GetXaxis().SetTitleSize(0.045)
                    h_axis.GetXaxis().SetLabelSize(0.04)
                    h_axis.GetYaxis().SetTitleSize(0.045)
                    h_axis.GetYaxis().SetLabelSize(0.04)
                    h_axis.GetXaxis().SetTitleOffset(1.1)

                h_axis.Draw("")
                if plotOnlySignal:
                    hmc.Draw("P,same")
                else:
                    g_data.Draw("P,same")
                    g_data_clone.Draw("P,same")
                    for pp in range(nPDF):
                        hp[pp].Draw("hist,same")
                if plotSignal:
                    hs.Draw("hist,same")
                if plotOnlySignal:
                    g_gauss.Draw("l,same")
                    g_dcb.Draw("l,same")

                llabel = "M_{Z_{D}} = %s, c#tau = %s mm"%(m, t)
                if plotOnlySignal:
                    legend = getLegend(binidx,g_data,pn,hp,hs,llabel,float(m), -1, True, False, True, hmc, g_gauss, g_dcb)
                else:
                    legend = getLegend(binidx,g_data,pn,hp,hs,llabel,float(m), -1, plotSignal)
                #year="2022"
                drawLabels(year,lumi,useData)
                legend.Draw("same")
                pads[0].Update()
                pads[0].RedrawAxis()
                
                ## Search region labels
                #
                latexExtra = ROOT.TLatex()
                latexExtra.SetTextFont(42)
                latexExtra.SetTextSize(0.04)
                latexExtra.SetNDC(True)
                #
                latexExtraBold = ROOT.TLatex()
                latexExtraBold.SetTextFont(62)
                latexExtraBold.SetTextSize(0.04)
                latexExtraBold.SetNDC(True)
                #
                catnames = d.split("_")
                lxybin = catnames[2]
                lxybin = (lxybin[3:]).split("to")
                if "d_Dimuon" in d:
                    latexExtraBold.DrawLatex(0.14,0.86,"Dimuon")
                    if "non-pointing" not in d:
                        latexExtra.DrawLatex(0.14,0.81,"l_{{xy}} #in [{},{}]".format(lxybin[0].replace("p", "."), lxybin[1].replace("p", ".")))
                        isobin = "Isolated" if catnames[3]=="iso1" else "Non isolated"
                        latexExtra.DrawLatex(0.14,0.76,isobin)
                        ptbin = "High p_{T}^{#mu#mu}" if catnames[4]=="pthigh" else "Low p_{T}^{#mu#mu}"
                        latexExtra.DrawLatex(0.14,0.71,ptbin)
                    else:
                        latexExtra.DrawLatex(0.14,0.81,"l_{{xy}} #in [{},{}]".format(lxybin[0].replace("p", "."), lxybin[1].replace("p", ".")))
                        latexExtra.DrawLatex(0.14,0.76,"Non-pointing")
                elif "d_FourMu" in d:
                    latexExtraBold.DrawLatex(0.14,0.86,"Four muon")
                    fourmucat = "Resolved" if "sep" in d else "Overlapping"
                    latexExtra.DrawLatex(0.14,0.81,fourmucat)

                ## Save canvas
                if plotOnlySignal:
                    can.SaveAs("%s/fitSIG_M%s_CT_%imm_%s.png"%(outDir,m,t,d))
                    can.SaveAs("%s/fitSIG_M%s_CT_%imm_%s.pdf"%(outDir,m,t,d))
                else:
                    can.SaveAs("%s/fitBG_M%s_%s.png"%(outDir,m,d))
                    can.SaveAs("%s/fitBG_M%s_%s.pdf"%(outDir,m,d))

                # Close input file with workspace                
                f.Close()
