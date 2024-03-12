import ROOT
import numpy
import copy
import os,sys
from datetime import date
import plotUtils

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

doRatio = True
doPull = True
useData = True
useSignalMC = True
doPartialUnblinding = True
normalizeSignal = False # Only if background is > 0

wsname = "wfit"
thisDir = os.environ.get("PWD")
inDir  = "%s/fitResults_allEras/"%thisDir

useCategorizedSignal = True
useCategorizedBackground = True

outDir = ("%s/fitPlots_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)

dNames = []
dNames.append("d_FourMu_sep")
dNames.append("d_FourMu_osv")
dNames.append("d_Dimuon_lxy0p0to0p5_iso0_ptlow");
dNames.append("d_Dimuon_lxy0p0to0p5_iso0_pthigh");
dNames.append("d_Dimuon_lxy0p0to0p5_iso1_ptlow");
dNames.append("d_Dimuon_lxy0p0to0p5_iso1_pthigh");
dNames.append("d_Dimuon_lxy0p5to2p7_iso0_ptlow");
dNames.append("d_Dimuon_lxy0p5to2p7_iso0_pthigh");
dNames.append("d_Dimuon_lxy0p5to2p7_iso1_ptlow");
dNames.append("d_Dimuon_lxy0p5to2p7_iso1_pthigh");
dNames.append("d_Dimuon_lxy2p7to6p5_iso0_ptlow");
dNames.append("d_Dimuon_lxy2p7to6p5_iso0_pthigh");
dNames.append("d_Dimuon_lxy2p7to6p5_iso1_ptlow");
dNames.append("d_Dimuon_lxy2p7to6p5_iso1_pthigh");
dNames.append("d_Dimuon_lxy6p5to11p0_iso0_ptlow");
dNames.append("d_Dimuon_lxy6p5to11p0_iso0_pthigh");
dNames.append("d_Dimuon_lxy6p5to11p0_iso1_ptlow");
dNames.append("d_Dimuon_lxy6p5to11p0_iso1_pthigh");
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_ptlow");
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh");
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow");
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh");
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_ptlow");
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh");
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow");
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh");
#dNames.append("")

years = []
#years.append("2022")
#years.append("2017")
#years.append("2016APV")
#years.append("2016nonAPV")
###
years.append("allEras")

# Signals
sigModels = []
sigModels.append("Y3")
#sigModels.append("DY3")
#sigModels.append("DYp3")
#sigModels.append("B3mL2")

sigMasses = []
if useSignalMC:
    sigMasses.append("7.0")
else:
    mF = 350.0
    mL = 2000.0
    sigMasses.append("%.0f"%mF)
    tm = mF
    while tm < mL:
      if tm<400.0: tm=tm+5.0
      elif tm<700.0: tm=tm+10.0
      elif tm<1000.0: tm=tm+15.0
      elif tm<1500.0: tm=tm+25.0
      else: tm=tm+50.0
      sigMasses.append("%.0f"%tm)
sigCtau = ["1", "10", "100"]

def drawLabels(year="all",lumi=59.83+41.48+19.5+16.8,plotData=False):
    # Labels
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.04)
    latex.SetNDC(True)

    latexCMS = ROOT.TLatex()
    latexCMS.SetTextFont(61)
    latexCMS.SetTextSize(0.04)
    latexCMS.SetNDC(True)

    latexCMSExtra = ROOT.TLatex()
    latexCMSExtra.SetTextFont(52)
    latexCMSExtra.SetTextSize(0.04)
    latexCMSExtra.SetNDC(True)

    legoffset = 0.0
    latexSel = ROOT. TLatex()
    latexSel.SetTextAlign(11)
    latexSel.SetTextFont(42)
    latexSel.SetTextSize(0.02-0.1*legoffset)
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
        latex.DrawLatex(0.90, 0.91+expoffset, yearenergy);
        latexCMS.DrawLatex(0.15,0.91+expoffset,"CMS");
        latexCMSExtra.DrawLatex(0.25,0.91+expoffset, cmsExtra);


def getLegend(ch,gd,p,hp,hs,smodel,smass,sigsf=-1.0,plotSignal=True,plotData=True):
    legend = ROOT.TLegend(0.3,0.6,0.91,0.91)
    legend.SetLineColor(0)
    legend.SetLineWidth(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    if plotData:
        legend.AddEntry(gd,"Data","EP")
    else:
        legend.AddEntry(gd,"Data (toy)","EP")
    for pn,pp in enumerate(p):
        legend.AddEntry(hp[pn],pp,"L")
    if plotSignal:
        if smodel=="Y3":
            smodel="Y_{3}"
        elif smodel=="DY3":
            smodel="DY_{3}"
        elif smodel=="DYp3":
            smodel="DY'_{3}"
        elif smodel=="B3mL2":
            smodel="B_{3}-L_{2}"
        if sigsf>0:
            #legend.AddEntry(hs,"%s, M=%.0f GeV (x%d)"%(smodel,smass,sigsf), "L")
            legend.AddEntry(hs,"%s, (x%.4f)"%(smodel,sigsf), "L")
        else:
            legend.AddEntry(hs,"%s"%(smodel), "L")
            
    if ch==0:
        legend.SetHeader("N_{b}#geq1")
    elif ch==1:
        legend.SetHeader("N_{b}=1")
    elif ch==2:
        legend.SetHeader("N_{b}#geq2")

    return legend

mean = 0.0
sigma = 0.0
for y in years:
    for t in sigCtau:
        for m in sigMasses:
            for d in dNames:
                sample = "Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-%smm"%(m.replace(".", "p"),t)
                finame = "%s/%s_%s_%s_workspace.root"%(inDir,d,sample,y)
                print(finame)
                binidx=-1
                if d=="d_Dimuon_lxy0p0to0p5_iso0_ptlow":
                    binidx=0
                elif d=="d_Dimuon_lxy0p0to0p5_iso0_pthigh":
                    binidx=1
                elif d=="d_Dimuon_lxy0p0to0p5_iso1_ptlow":
                    binidx=2
                elif d=="d_Dimuon_lxy0p0to0p5_iso1_pthigh":
                    binidx=3
                elif d=="d_Dimuon_lxy0p5to2p7_iso0_ptlow":
                    binidx=4
                elif d=="d_Dimuon_lxy0p5to2p7_iso0_pthigh":
                    binidx=5
                elif d=="d_Dimuon_lxy0p5to2p7_iso1_ptlow":
                    binidx=6
                elif d=="d_Dimuon_lxy0p5to2p7_iso1_pthigh":
                    binidx=7
                elif d=="d_Dimuon_lxy2p7to6p5_iso0_ptlow":
                    binidx=8
                elif d=="d_Dimuon_lxy2p7to6p5_iso0_pthigh":
                    binidx=9
                elif d=="d_Dimuon_lxy2p7to6p5_iso1_ptlow":
                    binidx=10
                elif d=="d_Dimuon_lxy2p7to6p5_iso1_pthigh":
                    binidx=11
                elif d=="d_Dimuon_lxy6p5to11p0_iso0_ptlow":
                    binidx=12
                elif d=="d_Dimuon_lxy6p5to11p0_iso0_pthigh":
                    binidx=13
                elif d=="d_Dimuon_lxy6p5to11p0_iso1_ptlow":
                    binidx=14
                elif d=="d_Dimuon_lxy6p5to11p0_iso1_pthigh":
                    binidx=15
                elif d=="d_Dimuon_lxy11p0to16p0_iso0_ptlow":
                    binidx=16
                elif d=="d_Dimuon_lxy11p0to16p0_iso0_pthigh":
                    binidx=17
                elif d=="d_Dimuon_lxy11p0to16p0_iso1_ptlow":
                    binidx=18
                elif d=="d_Dimuon_lxy11p0to16p0_iso1_pthigh":
                    binidx=19
                elif d=="d_Dimuon_lxy16p0to70p0_iso0_ptlow":
                    binidx=20
                elif d=="d_Dimuon_lxy16p0to70p0_iso0_pthigh":
                    binidx=21
                elif d=="d_Dimuon_lxy16p0to70p0_iso1_ptlow":
                    binidx=22
                elif d=="d_Dimuon_lxy16p0to70p0_iso1_pthigh":
                    binidx=23
                elif d=="d_FourMu_sep":
                    binidx=24
                elif d=="d_FourMu_osv":
                    binidx=25
                catExtS = ""
                catExtB = ""
                if useCategorizedSignal:
                    catExtS = "_ch%d"%binidx
                if useCategorizedBackground:
                    catExtB = "_ch%d"%binidx
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
                lumi=35.                
                if doPartialUnblinding:
                    lumi = 0.1*lumi
                nSig = w.var("signalNorm%s"%catExtS).getValV()
                nSig = nSig*lumi
                print(m, binidx, nSig)
                # Retrieve signal mean and std. deviation
                if binidx==0 or useCategorizedSignal:
                    mean = w.var("mean%s"%catExtS).getValV()
                    sigma = w.var("sigma%s"%catExtS).getValV()

                #try
                print(d)
                """
                try:
                    # Retrive BG normalization:
                    nBG = w.data("data_obs").sumEntries()
                    d = w.data("data_obs")
                    hd = x.createHistogram("hd",ROOT.RooFit.Binning(nBins,minx,maxx))                
                    d.fillHistogram(hd,ROOT.RooArgList(x))

                    bpdf = w.pdf("roomultipdf")
                    nPDF = w.cat("pdf_index").numTypes()
                except TypeError:
                    nBG = 0
                    hd = x.createHistogram("hd",ROOT.RooFit.Binning(nBins,minx,maxx))
                    nPDF = 0
                """
                # Retrive BG normalization:
                nBG = w.data("data_obs%s"%catExtB).sumEntries()
                d = w.data("data_obs%s"%catExtB)
                hd = x.createHistogram("hd",ROOT.RooFit.Binning(nBins,minx,maxx))                
                d.fillHistogram(hd,ROOT.RooArgList(x))

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
                        color=2
                    elif "powerlaw" in p[pp].GetName():
                       pn.append("Power-law")
                       color=3
                    else:
                       pn.append("Bernstein<%d>"%(numpars[pp]))
                       color=4
                    hp.append(p[pp].createHistogram("hp%d"%pp,x,ROOT.RooFit.Binning(100*nBins,minx,maxx)))
                    hp[pp].SetLineColor(color)
                    hp[pp].SetLineWidth(2)
                    hp[pp].Scale(nBG)
                    hpr.append(hp[pp].Clone("hpr%d"%pp))
                    hpr[pp].Rebin(100)
                    hp[pp].Scale(100.0)
                #except TypeError:

                sp = w.pdf("signal%s"%catExtS)
                hs = sp.createHistogram("hs",x,ROOT.RooFit.Binning(100*nBins,minx,maxx))
                hs.SetLineColor(6)
                hs.SetLineWidth(2)
                hs.Scale(nSig*100.0)
                #hs.Scale(lumi*1000./200000.)
                scale = -1.0
                if normalizeSignal and nBG > 1e-6:
                    scale = float(nBG)/float(nSig)
                    hs.Scale(scale)

                ROOT.gStyle.SetOptStat(0)
                can = ROOT.TCanvas("can","",600,600)
                can.cd()

                h_axis = ROOT.TH1D("h_axis","", hd.GetNbinsX(), hd.GetXaxis().GetBinLowEdge(1), hd.GetXaxis().GetBinUpEdge(hd.GetNbinsX()))
                h_axis.GetXaxis().SetTitle("m_{#mu#mu} [GeV]")
                h_axis.GetYaxis().SetTitle("Events")
                g_data = ROOT.TGraphAsymmErrors()
                plotUtils.ConvertToPoissonGraph(hd, g_data, drawZeros=True, drawXerr=False)
                g_data.SetMarkerStyle(20)
                g_data.SetMarkerSize(1.2)
                g_data.SetLineWidth(2)
                # draw with zero marker size so error bars drawn all the way to x axis in the case of 0 content
                g_data_clone = g_data.Clone()
                g_data_clone.SetMarkerSize(0.0)

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
                    pads[0].Draw()

                pads[0].cd()

                minR=0.0
                maxR=0.0
                ty = numpy.array([])
                tmax=maxR
                ty = g_data.GetY() 
                if len(ty)>0:
                    tmax = numpy.amax(ty)
                    if tmax>maxR:
                        maxR=tmax
                if hs.GetMaximum() > maxR:
                    maxR = hs.GetMaximum()
                if maxR>2.0:
                    maxR = maxR*1.5
                else:
                    #maxR = maxR*2.0
                    maxR = maxR*10.0
                    scale = scale*10.0
                    hs.Scale(10.0)
                
                if nSig < 1e-5:
                    scale = -1
                    hs.Scale(0.0)

                h_axis.SetMinimum(minR)
                h_axis.SetMaximum(maxR)
                h_axis.GetYaxis().SetRangeUser(minR,maxR)
                h_axis.GetYaxis().SetTitleSize(0.04)
                h_axis.GetXaxis().SetTitleSize(0.04)
                h_axis.GetXaxis().SetTitleOffset(1.25)
                h_axis.GetYaxis().SetLabelSize(0.03)

                h_axis.Draw("")
                g_data.Draw("P,same")
                g_data_clone.Draw("P,same")
                for pp in range(nPDF):
                    hp[pp].Draw("hist,same")
                hs.Draw("hist,same")

                llabel = "M_{Z_{D}} = %s, c#tau = %s mm"%(m, t)
                legend = getLegend(binidx,g_data,pn,hp,hs,llabel,float(m))
                year="all"
                drawLabels(year,lumi,useData)
                legend.Draw("same")
                pads[0].Update()
                pads[0].RedrawAxis()
                
                can.SaveAs("%s/fitBG_M%s_CT_%smm_%s.png"%(outDir,m,t,d))
                can.SaveAs("%s/fitBG_M%s_CT_%smm_%s.pdf"%(outDir,m,t,d))

                # Close input file with workspace                
                f.Close()
