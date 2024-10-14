import os,sys,math
import numpy as np
import ROOT

ROOT.gROOT.SetBatch(1)
drawObserved = False
drawPoints = True
maskSMResonances = True
NORMCONST = 0.01 # Needs to be consistent with what it was put on make_datacards.py e.g. if signal was scaled by NORMCONST xsec should be divided by it
typeOfLimit = "BRH" # "r", "xsec", "xsecBR" "BRH" 
xsec = 1.0 # in pb, used to normalize the MC
xsec_h = 59.8 # higgs cross section in pb at 13.6 GeV, used to normalize the MC
scaleToFullLumi = False
compare = True
luminosity = 35

## Normalize:
xsec = xsec*NORMCONST

model = sys.argv[1]
limdir = sys.argv[2]
ctau = sys.argv[3]
year = sys.argv[4]

if year=='2022':
    luminosity = 35
elif year=='2023':
    luminosity = 27
else:
    luminosity = 27 + 35

massl = []
obsl  = []
expl  = []
m2sl  = []
m1sl  = []
p1sl  = []
p2sl  = []
mext  = []
pext  = []

if typeOfLimit=="r":
    ylabel = "95% CL upper limit on #sigma/#sigma_{theory}"
elif typeOfLimit=="xsec":
    ylabel = "95% CL upper limit on #sigma"
    if model=="HTo2ZdTo2mu2x":
        ylabel = "95% CL upper limit on #sigma(h#rightarrowZ_{D}Z_{D}) [pb]"
elif typeOfLimit=="BRH":
    ylabel = "95% CL upper limit on Br(h#rightarrowXX)"
    if model=="HTo2ZdTo2mu2x":
        ylabel = "95% CL upper limit on Br(h#rightarrowZ_{D}Z_{D})"
    if model=="DarkShowers":
        ylabel = "95% CL upper limit on Br(h#rightarrow#Psi#Psi)"
elif typeOfLimit=="xsecBR":
    ylabel = "95% CL upper limit on #sigmaxBR"
    if model=="HTo2ZdTo2mu2x":
        ylabel = "95% CL upper limit on #sigma(h#rightarrowZ_{D}Z_{D})xB(Z_{D}#rightarrow#mu#mu) [pb]"

fin = open("%s/limits_%s_%s.txt"%(limdir,model,year),"r")
for l in fin.readlines():
    if l.startswith("#"):
        continue
    ls = l.split(",")
    if ls[0]!=model:
        continue
    if int(ls[2])!=int(ctau):
        continue
    scale = 1.0
    if typeOfLimit=="xsec":
        scale = xsec
    if typeOfLimit=="BRH":
        scale = xsec/xsec_h
    elif typeOfLimit=="xsecBR":
        if model=="HTo2ZdTo2mu2x":
            BR = 1.0
            with open('data/hahm-mass_brs.txt', 'r') as f:
                for line in f.readlines():
                    if "mZd" in line: continue
                    brs = line.split('\t')
                    while '' in brs:
                        brs.remove('')
                    brs[-1] = brs[-1].strip('\n')
                    if (abs(float(brs[0])-float(ls[1])) < 0.0001):
                        BR = float(brs[2])
                        break
        scale = xsec*BR
        print(float(ls[1]), float(ls[4]), BR)
    #if scaleToFullLumi:
    #    scale = scale / math.sqrt(10.0)
    if model=="HTo2ZdTo2mu2x" and float(ctau) > 10 and float(ls[1]) < 1.5:
        continue
    massl.append(float(ls[1]))
    obsl .append(scale*float(ls[3]))
    expl .append(scale*float(ls[4]))
    m2sl .append(scale*float(ls[5]))
    m1sl .append(scale*float(ls[6]))
    p1sl .append(scale*float(ls[7]))
    p2sl .append(scale*float(ls[8]))

    if scaleToFullLumi:
        mext .append(scale*float(ls[4])/10.0)
        pext .append(scale*float(ls[4])/math.sqrt(10.0))

fin.close()

massv = np.array(massl,"d")
obsv  = np.array(obsl ,"d")
expv  = np.array(expl ,"d")
m1sv  = np.array(m1sl ,"d")
p1sv  = np.array(p1sl ,"d")
m2sv  = np.array(m2sl ,"d")
p2sv  = np.array(p2sl ,"d")

cfile = None
if compare:
    print("> Request to open files to compare")
    try:
        if model=="HTo2ZdTo2mu2x":
            if typeOfLimit=="BRH":
                if ctau=="1":
                    cfile = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Figure_8a.root")
                    cgobs = cfile.Get("Figure 8a/Graph1D_y1")
                    cgexp = cfile.Get("Figure 8a/Graph1D_y2")
                if ctau=="100":
                    cfile = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Figure_8b.root")
                    cgobs = cfile.Get("Figure 8b/Graph1D_y1")
                    cgexp = cfile.Get("Figure 8b/Graph1D_y2")
        cgobs.SetLineColor(ROOT.kBlue)
        cgobs.SetMarkerColor(ROOT.kBlue)
        cgobs.SetMarkerStyle(20)
        cgobs.SetLineStyle(1)
        cgobs.SetLineWidth(2)
        cgexp.SetLineColor(ROOT.kBlue)
        cgexp.SetMarkerColor(ROOT.kBlue)
        cgexp.SetMarkerStyle(20)
        cgexp.SetLineStyle(2)
        cgexp.SetLineWidth(2)
        print("> Files accessed")
    except NameError:
        print("> Files not available")
        pass

miny = 999.
maxy = -1.0
if min(obsl)<miny:
    miny=min(obsl)*0.1
if min(m1sl)<miny:
    miny=min(m1sl)*0.1
miny=5e-6
maxy=1e-1

if max(obsl)>maxy:
    maxy=max(obsl)*10.0
if max(p1sl)>maxy:
    maxy=max(p1sl)*10.0

if compare:
    miny=5e-6
    maxy=0.1

gobs = ROOT.TGraph(len(massv),massv,obsv)
gobs.SetLineColor(1)
gobs.SetMarkerColor(1)
gobs.SetMarkerStyle(20)
gobs.SetLineStyle(1)
gobs.SetLineWidth(2)

gexp = ROOT.TGraph(len(massv),massv,expv)
gexp.SetLineColor(2)
gexp.SetMarkerColor(2)
gexp.SetMarkerStyle(20)
gexp.SetLineStyle(1)
gexp.SetLineWidth(2)

gm1s = ROOT.TGraph(len(massv),massv,m1sv)
gm1s.SetLineColor(2)
gm1s.SetMarkerColor(2)
gm1s.SetMarkerStyle(20)
gm1s.SetLineStyle(2)
gm1s.SetLineWidth(2)

gp1s = ROOT.TGraph(len(massv),massv,p1sv)
gp1s.SetLineColor(2)
gp1s.SetMarkerColor(2)
gp1s.SetMarkerStyle(20)
gp1s.SetLineStyle(2)
gp1s.SetLineWidth(2)

dummy = np.full(len(massv), 0.0)
g1s = ROOT.TGraphAsymmErrors(len(massv),massv,expv, dummy, dummy, expv-m1sv, p1sv-expv)
g1s.SetLineColor(ROOT.kGreen+2)
g1s.SetFillColor(ROOT.kGreen+2)
g1s.SetMarkerColor(ROOT.kGreen+2)
g1s.SetMarkerStyle(1)

if scaleToFullLumi:
    gext = ROOT.TGraphAsymmErrors(len(massv),massv,expv, dummy, dummy, expv-mext, pext-expv)
    gext.SetLineColor(2)
    gext.SetFillColor(2)
    gext.SetFillStyle(3244)
    gext.SetMarkerColor(2)
    gext.SetMarkerStyle(1)

g2s = ROOT.TGraphAsymmErrors(len(massv),massv,expv, dummy, dummy, expv-m2sv, p2sv-expv)
g2s.SetLineColor(ROOT.kOrange)
g2s.SetFillColor(ROOT.kOrange)
g2s.SetMarkerColor(ROOT.kOrange)
g2s.SetMarkerStyle(1)

if not compare:
    leg = ROOT.TLegend(0.6,0.68,0.89,0.89)
else:
    leg = ROOT.TLegend(0.35,0.67,0.89,0.89)
leg.SetMargin(0.15)
leg.SetFillColor(ROOT.kWhite)
leg.SetTextSize(0.03)
modelLeg = model
if model=="HTo2ZdTo2mu2x":
    modelLeg="h#rightarrow Z_{D}Z_{D}"
elif model=="DY3":
    modelLeg="DY_{3}"
elif model=="DYp3":
    modelLeg="DY'_{3}"
elif model=="B3mL2":
    modelLeg="B_{3}-L_{2}"
leg.SetHeader("%s (c#tau = %s mm)"%(modelLeg,ctau))
if drawObserved:
    leg.AddEntry(gobs,"Observed","L")
leg.AddEntry(gexp,"Expected","L")
leg.AddEntry(g1s,"#pm1#sigma expected","F")
leg.AddEntry(g2s,"#pm2#sigma expected","F")
if scaleToFullLumi:
    leg.AddEntry(gext,"Full lumi extrapolated","F")
if compare and cfile is not None:
    leg.AddEntry(cgexp,"Run 2 dimuon scouting 101 fb^{-1} (expected)","L")

haxis = ROOT.TH1D("haxis","",10,massv[0]-0.05*massv[0],massv[len(massv)-1]+0.05*massv[len(massv)-1])
haxis.GetXaxis().SetTitle("Mass [GeV]")
haxis.GetYaxis().SetTitle("95% CL upper limit on #sigma/#sigma_{theory}")
haxis.GetYaxis().SetTitle(ylabel)
haxis.GetXaxis().SetLabelSize(0.03)
haxis.GetYaxis().SetLabelSize(0.03)
haxis.SetMinimum(miny)
haxis.SetMaximum(maxy)
haxis.GetYaxis().SetRangeUser(miny,maxy)

line = ROOT.TLine(massv[0],1.0,massv[len(massv)-1],1.0)
line.SetLineColor(ROOT.kGray)
line.SetLineStyle(2)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetFrameLineWidth(2)
can = ROOT.TCanvas("can","",700,600)
can.cd()
ROOT.gPad.SetTicky()
ROOT.gPad.SetLogy()
ROOT.gPad.SetLogx()

haxis.Draw()

if not drawPoints:
    g2s.Draw("3")
    g1s.Draw("3")
    gexp.Draw("L")
    if scaleToFullLumi:
        gext.Draw("3")
    if drawObserved:
        gobs.Draw("L")
else:
    g2s.Draw("3")
    g1s.Draw("3")
    gexp.Draw("PL")
    if scaleToFullLumi:
        gext.Draw("3")
    if drawObserved:
        gobs.Draw("PL")

if cfile is not None:
    #cgobs.Draw("L")
    cgexp.Draw("L")

if maskSMResonances:

    bks = ROOT.TGraph(4)
    bks.SetPoint(0, 0.43, miny+0.02*miny)
    bks.SetPoint(1, 0.49, miny+0.02*miny)
    bks.SetPoint(2, 0.49, maxy-0.02*maxy)
    bks.SetPoint(3, 0.43, maxy-0.02*maxy)
    bks.SetFillColorAlpha(ROOT.kGray, 1.0)
    bks.Draw("f")

    beta = ROOT.TGraph(4)
    beta.SetPoint(0, 0.52, miny+0.02*miny)
    beta.SetPoint(1, 0.58, miny+0.02*miny)
    beta.SetPoint(2, 0.58, maxy-0.02*maxy)
    beta.SetPoint(3, 0.52, maxy-0.02*maxy)
    beta.SetFillColorAlpha(ROOT.kGray, 1.0)
    beta.Draw("f")

    brho = ROOT.TGraph(4)
    brho.SetPoint(0, 0.73, miny+0.02*miny)
    brho.SetPoint(1, 0.84, miny+0.02*miny)
    brho.SetPoint(2, 0.84, maxy-0.02*maxy)
    brho.SetPoint(3, 0.73, maxy-0.02*maxy)
    brho.SetFillColorAlpha(ROOT.kGray, 1.0)
    brho.Draw("f")

    bphi = ROOT.TGraph(4)
    bphi.SetPoint(0, 0.91, miny+0.02*miny)
    bphi.SetPoint(1, 1.2, miny+0.02*miny)
    bphi.SetPoint(2, 1.2, maxy-0.02*maxy)
    bphi.SetPoint(3, 0.91, maxy-0.02*maxy)
    bphi.SetFillColorAlpha(ROOT.kGray, 1.0)
    bphi.Draw("f")

    bjpsi = ROOT.TGraph(4)
    bjpsi.SetPoint(0, 2.8, miny+0.02*miny)
    bjpsi.SetPoint(1, 4.1, miny+0.02*miny)
    bjpsi.SetPoint(2, 4.1, maxy-0.02*maxy)
    bjpsi.SetPoint(3, 2.8, maxy-0.02*maxy)
    bjpsi.SetFillColorAlpha(ROOT.kGray, 1.0)
    bjpsi.Draw("f, same")

    bups = ROOT.TGraph(4)
    bups.SetPoint(0, 8.6, miny+0.02*miny)
    bups.SetPoint(1, 11.0, miny+0.02*miny)
    bups.SetPoint(2, 11.0, maxy-0.02*maxy)
    bups.SetPoint(3, 8.6, maxy-0.02*maxy)
    bups.SetFillColorAlpha(ROOT.kGray, 1.0)
    bups.Draw("f, same")


#line.Draw("same")

ROOT.gPad.RedrawAxis()
leg.Draw("same")
can.Update()

## Draw CMS banners and lumi
#
latexCMS = ROOT.TLatex()
latexCMS.SetTextFont(61)
latexCMS.SetTextSize(0.055)
latexCMS.SetNDC(True)
latexCMS.DrawLatex(0.11,0.91,"CMS");
#
latexCMSExtra = ROOT.TLatex()
latexCMSExtra.SetTextFont(52)
latexCMSExtra.SetTextSize(0.04)
latexCMSExtra.SetNDC(True)
latexCMSExtra.DrawLatex(0.21,0.91, "Work in progress");
# 
latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(31)
latex.SetTextSize(0.04)
latex.SetNDC(True)
latex.DrawLatex(0.9,0.91, "%.2f fb^{-1} (%s, 13.6 TeV)"%(luminosity,year));

if scaleToFullLumi:
    can.SaveAs("%s/limits_%s_ctau%s_%s_scaled.png"%(limdir,model,ctau,typeOfLimit))
    can.SaveAs("%s/limits_%s_ctau%s_%s_scaled.pdf"%(limdir,model,ctau,typeOfLimit))
else:
    if drawObserved:
        can.SaveAs("%s/limits_%s_ctau%s_%s_obs.png"%(limdir,model,ctau,typeOfLimit))
        can.SaveAs("%s/limits_%s_ctau%s_%s_obs.pdf"%(limdir,model,ctau,typeOfLimit))
    else:
        can.SaveAs("%s/limits_%s_ctau%s_%s.png"%(limdir,model,ctau,typeOfLimit))
        can.SaveAs("%s/limits_%s_ctau%s_%s.pdf"%(limdir,model,ctau,typeOfLimit))
