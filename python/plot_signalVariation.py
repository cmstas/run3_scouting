import ROOT
import numpy
import copy
import os,sys
from datetime import date
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
#import plotUtils

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

doRel = True

wsname = "wfit"
thisDir = os.environ.get("PWD")

useCategorizedSignal = True
useCategorizedBackground = True

outDir = ("%s/signalParameters_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)

years = []
#years.append("2022")
#years.append("2017")
#years.append("2016APV")
#years.append("2016nonAPV")
###
years.append("allEras")

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

ROOT.gStyle.SetOptStat(0)

f = ROOT.TFile.Open("utils/signalFitParameters_lxybins_2022_new.root")

params = []
params.append(['gsigma', 'splines', r'width $\sigma$'])
params.append(['gmean', 'splinem', r'mean $\mu$'])
params.append(['gnL', 'splinenL', r'$n_{L}$'])
params.append(['gnR', 'splinenR', r'$n_{R}$'])
params.append(['gaL', 'splineaL', r'$a_{L}$'])
params.append(['gaR', 'splineaR', r'$a_{R}$'])

colors = ['#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd']
isRelative = True

for p,par in enumerate(params):

    lxybins = []
    lxybins.append('lxy0p0to0p2')
    lxybins.append('lxy0p2to1p0')
    lxybins.append('lxy1p0to2p4')
    lxybins.append('lxy2p4to3p1')
    lxybins.append('lxy3p1to7p0')
    lxybins.append('lxy7p0to11p0')
    lxybins.append('lxy11p0to16p0')
    lxybins.append('lxy16p0to70p0')

    xmass_axis = np.logspace(-1, 2, 300)

    plt.style.use(hep.style.CMS)
    fig, ax = plt.subplots(figsize=(9, 7))

    for t,lxy in enumerate(lxybins):

        gname = "%s_d_Dimuon_%s_inclusive"%(par[0], str(lxy))
        sname = "%s_d_Dimuon_%s_inclusive"%(par[1], str(lxy))
        print(gname, sname)

        graph = f.Get(gname)
        points = np.array([graph.GetPointY(i) for i in range(graph.GetN())])
        masses = np.array([graph.GetPointX(i) for i in range(graph.GetN())])
   
        spline = f.Get(gname)
        spline_val = []
        for mass in xmass_axis:
            spline_val.append(spline.Eval(mass))
        inter = np.array(spline_val)

        relpoints = points/masses
        relinter = inter/xmass_axis

        labeltag = ''
        if lxy=='lxy0p0to0p2': labeltag = r'$l_{xy} \in [0.0, 0.2]$ cm'
        if lxy=='lxy0p2to1p0': labeltag = r'$l_{xy} \in [0.2, 1.0]$ cm'
        if lxy=='lxy1p0to2p4': labeltag = r'$l_{xy} \in [1.0, 2.4]$ cm'
        if lxy=='lxy2p4to3p1': labeltag = r'$l_{xy} \in [2.4, 3.1]$ cm'
        if lxy=='lxy3p1to7p0': labeltag = r'$l_{xy} \in [3.1, 7.0]$ cm'
        if lxy=='lxy7p0to11p0': labeltag = r'$l_{xy} \in [7.0, 11.0]$ cm'
        if lxy=='lxy11p0to16p0': labeltag = r'$l_{xy} \in [11.0, 16.0]$ cm'
        if lxy=='lxy16p0to70p0': labeltag = r'$l_{xy} \in [16.0, 70.0]$ cm'
    
        if isRelative:
            ax.plot(xmass_axis, relinter, label=labeltag, linestyle='-', color = colors[t])
            ax.scatter(masses, relpoints, color = colors[t])
        else:
            ax.plot(xmass_axis, inter, label=labeltag, linestyle='-', color = colors[t])
            ax.scatter(masses, points, color = colors[t])

    hep.cms.label("", data=False, year='2022', com='13.6')
    ax.set_xlabel(r'Dimuon invariant mass $m_{\mu\mu}$ (GeV)', fontsize=20)
    if isRelative:
        ax.set_ylabel('Relative ' + par[2], fontsize=20)
    else:
        ax.set_ylabel(par[2], fontsize=20)
    ax.set_xscale('log')
    ax.set_xlim(0.5, 50.0)
    if isRelative:
        ax.set_ylim(0.1*min(relpoints), 1.1*max(relpoints))
    else:
        ax.set_ylim(0.3*min(points), 3*max(points))

    legsize = 15
    ax.legend(fontsize=15, ncol = 2)

    if isRelative:
        ax.text(0.6, 2.1*max(relpoints), r'$h\rightarrow Z_{D}Z_{D}$, $Z_{D}\rightarrow\mu\mu$ (c$\tau$ = 1, 10, 100, 1000 mm)', fontsize=13)

    if isRelative:
        fig.savefig('rel_%s.png'%(par[0]), dpi=140)
    else:
        fig.savefig('%s.png'%(par[0]), dpi=140)



f.Close()

