import ROOT
import numpy as np
import copy
import os,sys
from datetime import date
import plotUtils
import matplotlib.pyplot as plt
import mplhep as hep
import pickle

ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ProcessLine(".L cpp/helper.C+")
plt.style.use(hep.style.CMS)

def getValues(histo):
    histo.SetBinErrorOption(ROOT.TH1.kPoisson)
    values = []
    bins = []
    err_low = []
    err_up = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
        err_low.append(histo.GetBinErrorLow(n))
        err_up.append(histo.GetBinErrorUp(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins), np.array(err_low), np.array(err_up)

hepdata_input = True

"""

#############
############## Figures 5 a) and b)
#############
#
lumi=62.4
inDir = '/ceph/cms/store/user/fernance/EXO-24-016/Spectra/Fourmuon-spectra/'
#
# Figure a)
#
samples = []
samples.append('Data')
samples.append('Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm')
samples.append('Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm')
samples.append('Signal_ScenarioA_Mpi-5_MA-1p67_ctau-10.00mm')
samples.append('Signal_ScenarioA_Mpi-7p50_MA-2p50_ctau-10.00mm')
#
legnames = {}
legnames['Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm']  = r"$h\rightarrow Z_{{D}}Z_{{D}}$: $m_{Z_D}$ = 5 GeV, $c\tau_{0}^{{Z_{{D}}}} =$ 1 cm"
legnames['Signal_ScenarioA_Mpi-2_MA-0p67_ctau-1.00mm'] = r"ScenarioA: $m_\pi = 2$ GeV, $m_A = 0.67$ GeV, $c\tau_{0}^{A} =$ 0.1 cm"
legnames['Signal_ScenarioA_Mpi-5_MA-1p67_ctau-10.00mm'] = r"ScenarioA: $m_\pi = 5$ GeV, $m_A = 1.67$ GeV, $c\tau_{0}^{A} =$ 1 cm"
legnames['Signal_ScenarioA_Mpi-7p50_MA-2p50_ctau-10.00mm'] = r"ScenarioA: $m_\pi = 7.5$ GeV, $m_A = 2.5$ GeV, $c\tau_{0}^{A} =$ 1 cm"
#
colors = ["#3f90da", "#ffa90e", "#bd1f01", "#832db6", "#e76300"]
#
histograms = {}
histograms['d_FourMu_sep_rawmass'] = {}
histograms['d_FourMu_sep_rawmass']['Data'] = 0.0
histograms['d_FourMu_sep_rawmass']['Signal'] = {}
for sample in samples:
    if 'Signal' not in sample:
        continue
    histograms['d_FourMu_sep_rawmass']['Signal'][sample] = 0.0

# Fill histograms
for sample in samples:
    tfile = ROOT.TFile('%s/histograms_%s_%s_all.root'%(inDir, sample, "allYears"))
    th1f = tfile.Get('d_FourMu_sep_rawmass')
    if 'Data'==sample:
        histograms['d_FourMu_sep_rawmass']['Data'] = copy.deepcopy(th1f.Clone("%s_%s"%('d_FourMu_osv_rawmass',sample)))
    else:
        histograms['d_FourMu_sep_rawmass']['Signal'][sample] = copy.deepcopy(th1f.Clone("%s_%s"%('d_FourMu_osv_rawmass',sample)))
        #histograms['d_FourMu_sep_rawmass']['Signal'][sample].Scale((27+35)/35) ####### -----> THIS IS TO BE REMOVED!!!!!!!!!
#
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.text("", loc=0, ax=ax, fontsize=30)
hep.cms.lumitext("%s fb$^{-1}$ (2022 + 2023) (13.6 TeV)"%(lumi), ax=ax, fontsize=30, fontname=None)
ax.set_yscale("linear")
ax.set_xscale("log")
# Data histogram
dhist, dedges, y_err_down, y_err_up = getValues(histograms['d_FourMu_sep_rawmass']['Data'])
y_err = dhist**0.5
ddedges = []
for v in range(0, len(dedges)-1):
    ddedges.append(dedges[v] + 0.5*(dedges[v+1] - dedges[v]))
ax.errorbar(np.array(ddedges)[dhist>0], dhist[dhist>0], yerr=[y_err_down[dhist>0], y_err_up[dhist>0]], xerr=0.5*(dedges[1] - dedges[0]), fmt='o', label='Data', color='k', markersize=5, zorder=5)
# Signal histograms
shists = []
for s,signal in enumerate(histograms['d_FourMu_sep_rawmass']['Signal'].keys()):
    shist, sedges, sy_err_down, sy_err_up = getValues(histograms['d_FourMu_sep_rawmass']['Signal'][signal])
    hep.histplot(shist, sedges, color=colors[s], label = legnames[signal], histtype="fill", ax=ax, zorder=10, alpha=0.3)
    hep.histplot(shist, sedges, color=colors[s], histtype="step", ax=ax, zorder=2)
    shists.append([signal, shist])
ax.set_ylabel('Events / %.2f GeV'%(dedges[1] - dedges[0]), fontsize=28)
ax.set_xlabel(r'$m_{4\mu}$ [GeV]', fontsize=28)
ax.text(0.03, 0.52, "Four-muon, resolved", fontsize=23, color='black', horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
ax.set_xlim(1., 200.0)
ax.set_ylim(0,10)
ax.set_xticks([1, 10, 100])
ax.set_xticklabels(["1", r"$10^{1}$", r"$10^{2}$"])
ax.legend(loc="upper right", fontsize=22, frameon=False)
fig.savefig("paperPlots/Figure_005-a.png", dpi=140)
fig.savefig("paperPlots/Figure_005-a.pdf", dpi=140)

if hepdata_input:
    data = {}
    data['mass_binned_values'] = []
    data['data_values'] = []
    data['data_unc'] = []
    for i in range(len(sedges) - 1):
        data['mass_binned_values'].append((sedges[i], sedges[i+1]))
        data['data_values'].append(dhist[i])
        data['data_unc'].append(y_err[i])
    for [signal, shist] in shists:
        data[signal] = []
        for i in range(len(shist)):
            data[signal].append(shist[i])
    with open('paperPlots/hepdata_Figure_005-a.pkl', 'wb') as f:
        pickle.dump(data, f)

#
# Figure b)
#
samples = []
samples.append('Data')
samples.append('Signal_ScenarioB1_Mpi-2_MA-0p67_ctau-1.00mm')
samples.append('Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-1.00mm')
samples.append('Signal_ScenarioB1_Mpi-7p50_MA-2p50_ctau-1.00mm')
#
legnames = {}
legnames['Signal_ScenarioB1_Mpi-2_MA-0p67_ctau-1.00mm'] = r"ScenarioB1: $m_\pi = 2$ GeV, $m_A = 0.67$ GeV, $c\tau_{0}^{A} =$ 0.1 cm"
legnames['Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-1.00mm'] = r"ScenarioB1: $m_\pi = 5$ GeV, $m_A = 1.67$ GeV, $c\tau_{0}^{A} =$ 0.1 cm"
legnames['Signal_ScenarioB1_Mpi-7p50_MA-2p50_ctau-1.00mm'] = r"ScenarioB1: $m_\pi = 7.5$ GeV, $m_A = 2.5$ GeV, $c\tau_{0}^{A} =$ 0.1 cm"
#
colors = ["#3f90da", "#ffa90e", "#bd1f01", "#832db6", "#e76300"]
#
histograms = {}
histograms['d_FourMu_osv_rawmass'] = {}
histograms['d_FourMu_osv_rawmass']['Data'] = 0.0
histograms['d_FourMu_osv_rawmass']['Signal'] = {}
for sample in samples:
    if 'Signal' not in sample:
        continue
    histograms['d_FourMu_osv_rawmass']['Signal'][sample] = 0.0

# Fill histograms
for sample in samples:
    tfile = ROOT.TFile('%s/histograms_%s_%s_all.root'%(inDir, sample, "allYears"))
    th1f = tfile.Get('d_FourMu_osv_rawmass')
    if 'Data'==sample:
        histograms['d_FourMu_osv_rawmass']['Data'] = copy.deepcopy(th1f.Clone("%s_%s"%('d_FourMu_osv_rawmass',sample)))
    else:
        histograms['d_FourMu_osv_rawmass']['Signal'][sample] = copy.deepcopy(th1f.Clone("%s_%s"%('d_FourMu_osv_rawmass',sample)))
#
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.text("", loc=0, ax=ax, fontsize=30)
hep.cms.lumitext("%s fb$^{-1}$ (2022 + 2023) (13.6 TeV)"%(lumi), ax=ax, fontsize=30, fontname=None)
ax.set_yscale("linear")
ax.set_xscale("log")
# Data histogram
dhist, dedges, y_err_down, y_err_up = getValues(histograms['d_FourMu_osv_rawmass']['Data'])
y_err = dhist**0.5
ddedges = []
for v in range(0, len(dedges)-1):
    ddedges.append(dedges[v] + 0.5*(dedges[v+1] - dedges[v]))
ax.errorbar(np.array(ddedges)[dhist>0], dhist[dhist>0], yerr=[y_err_down[dhist>0], y_err_up[dhist>0]], xerr=0.5*(dedges[1] - dedges[0]), fmt='o', label='Data', color='k', markersize=5, zorder=5)
# Signal histograms
shists = []
for s,signal in enumerate(histograms['d_FourMu_osv_rawmass']['Signal'].keys()):
    shist, sedges, sy_err_down, sy_err_up = getValues(histograms['d_FourMu_osv_rawmass']['Signal'][signal])
    hep.histplot(shist, sedges, color=colors[s], label = legnames[signal], histtype="fill", ax=ax, zorder=10, alpha=0.3)
    hep.histplot(shist, sedges, color=colors[s], histtype="step", ax=ax, zorder=2)
    shists.append([signal, shist])
ax.set_ylabel('Events / %.2f GeV'%(dedges[1] - dedges[0]), fontsize=28)
ax.set_xlabel(r'$m_{4\mu}$ [GeV]', fontsize=28)
ax.text(0.03, 0.62, "Four-muon, overlapping", fontsize=23, color='black', horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
ax.set_xlim(1., 100.0)
ax.set_ylim(0,7)
ax.set_xticks([1, 10, 100])
ax.set_xticklabels(["1", r"$10^{1}$", r"$10^{2}$"])
ax.legend(loc="upper right", fontsize=22, frameon=False)
fig.savefig("paperPlots/Figure_005-b.png", dpi=140)
fig.savefig("paperPlots/Figure_005-b.pdf", dpi=140)

if hepdata_input:
    data = {}
    data['mass_binned_values'] = []
    data['data_values'] = []
    data['data_unc'] = []
    for i in range(len(sedges) - 1):
        data['mass_binned_values'].append((sedges[i], sedges[i+1]))
        data['data_values'].append(dhist[i])
        data['data_unc'].append(y_err[i])
    for [signal, shist] in shists:
        data[signal] = []
        for i in range(len(shist)):
            data[signal].append(shist[i])
    with open('paperPlots/hepdata_Figure_005-b.pkl', 'wb') as f:
        pickle.dump(data, f)


#############
############## Figure 6-9
#############
colors = ["#3f90da", "#ffa90e", "#bd1f01", "#832db6", "#e76300"]
lumi=62.4
inDir = '/ceph/cms/store/user/fernance/EXO-24-016/Spectra/Dimuon-noMasking/'
#
samples = []
samples.append('Data')
samples.append('Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm')
samples.append('Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm')
samples.append('Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-10.00mm')
samples.append('Signal_BToPhi_MPhi-2p00_ctau-10.00mm')
#
legnames = {}
legnames['Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm']  = r"$h\rightarrow Z_{{D}}Z_{{D}}$: $m_{Z_D}$ = 5 GeV, $c\tau_{0}^{{Z_{{D}}}} =$ 1 cm"
legnames['Signal_ScenarioA_Mpi-2_MA-0p67_ctau-10.00mm'] = r"ScenarioA: $m_\pi = 2$ GeV, $m_A = 0.67$ GeV, $c\tau_{0}^{A} =$ 1 cm"
legnames['Signal_ScenarioB1_Mpi-5_MA-1p67_ctau-10.00mm'] = r"ScenarioB1: $m_\pi = 5$ GeV, $m_A = 1.67$ GeV, $c\tau_{0}^{\pi} =$ 1 cm"
legnames['Signal_BToPhi_MPhi-2p00_ctau-10.00mm'] = r"$h_{b}\rightarrow \phi X$: $m_{\phi}$ = 2 GeV, $c\tau_{0}^{\phi} =$ 1 cm"
#
#
#
hnn = []
hnn.append(['d_Dimuon_lxy0p0to0p2_iso1_pthigh_rawmass', 6, 'a', [0.1, 8e10], 'log'])
hnn.append(['d_Dimuon_lxy0p2to1p0_iso1_pthigh_rawmass', 6, 'b', [0.1, 1e11], 'log'])
hnn.append(['d_Dimuon_lxy1p0to2p4_iso1_pthigh_rawmass', 6, 'c', [0.1, 1e10], 'log'])
hnn.append(['d_Dimuon_lxy2p4to3p1_iso1_pthigh_rawmass', 6, 'd', [0.1, 1e7], 'log'])
hnn.append(['d_Dimuon_lxy3p1to7p0_iso1_pthigh_rawmass', 6, 'e', [0.1, 2e6], 'log'])
hnn.append(['d_Dimuon_lxy7p0to11p0_iso1_pthigh_rawmass', 6, 'f', [0.1, 9e3], 'log'])
hnn.append(['d_Dimuon_lxy11p0to16p0_iso1_pthigh_rawmass', 7, 'a', [0.1, 3e3], 'log'])
hnn.append(['d_Dimuon_lxy16p0to70p0_iso1_pthigh_rawmass', 7, 'b', [0.1, 1e3], 'log'])
hnn.append(['d_Dimuon_lxy0p0to0p2_iso1_ptlow_rawmass', 8, 'a', [0.1, 8e11], 'log'])
hnn.append(['d_Dimuon_lxy0p2to1p0_iso1_ptlow_rawmass', 8, 'b', [0.1, 8e11], 'log'])
hnn.append(['d_Dimuon_lxy1p0to2p4_iso1_ptlow_rawmass', 8, 'c', [0.1, 2e9], 'log'])
hnn.append(['d_Dimuon_lxy2p4to3p1_iso1_ptlow_rawmass', 8, 'd', [0.1, 5e5], 'log'])
hnn.append(['d_Dimuon_lxy3p1to7p0_iso1_ptlow_rawmass', 8, 'e', [0.1, 6e6], 'log'])
hnn.append(['d_Dimuon_lxy7p0to11p0_iso1_ptlow_rawmass', 8, 'f', [0.1, 2e6], 'log'])
hnn.append(['d_Dimuon_lxy11p0to16p0_iso1_ptlow_rawmass', 9, 'a', [0.1, 3e5], 'log'])
hnn.append(['d_Dimuon_lxy16p0to70p0_iso1_ptlow_rawmass', 9, 'b', [0.1, 1e4], 'log'])
histograms = {}
for h_ in hnn:
    hn = h_[0]
    histograms[hn] = {}
    histograms[hn]['Data'] = 0.0
    histograms[hn]['Signal'] = {}
    for sample in samples:
        if 'Signal' not in sample:
            continue
        histograms[hn]['Signal'][sample] = 0.0
#
for sample in samples:
    print(samples)
    print(inDir)
    tfile = ROOT.TFile('%s/histograms_%s_%s_all.root'%(inDir, sample, 'allYears'))
    for h_ in hnn:
        hn = h_[0]
        th1f = tfile.Get(hn)
        if 'Data'==sample:
            histograms[hn]['Data'] = copy.deepcopy(th1f.Clone("%s_%s"%(hn,sample)))
        else:
            histograms[hn]['Signal'][sample] = copy.deepcopy(th1f.Clone("%s_%s"%(hn,sample)))
            #if 'Scenario' in sample:
            #    histograms[hn]['Signal'][sample].Scale((27+35)/35)
#
for h_ in hnn:
    hn = h_[0]
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    hep.cms.text("", loc=0, ax=ax, fontsize=30)
    hep.cms.lumitext("%s fb$^{-1}$ (2022 + 2023) (13.6 TeV)"%(lumi), ax=ax, fontsize=30, fontname=None)
    ax.set_yscale(h_[4])
    ax.set_xscale("log")
    # Data histogram
    dhist, dedges, y_err_down, y_err_up = getValues(histograms[hn]['Data'])
    y_err = dhist**0.5
    ddedges = []
    for v in range(0, len(dedges)-1):
        ddedges.append(dedges[v] + 0.5*(dedges[v+1] - dedges[v]))
    ax.errorbar(np.array(ddedges)[dhist>0], dhist[dhist>0], yerr=[y_err_down[dhist>0], y_err_up[dhist>0]], xerr=0.5*(dedges[1] - dedges[0]), fmt='o', label='Data', color='k', markersize=5, zorder=5)
    # Signal histograms
    shists = []
    for s,signal in enumerate(histograms[hn]['Signal'].keys()):
        shist, sedges, sy_err_down, sy_err_up = getValues(histograms[hn]['Signal'][signal])
        hep.histplot(shist, sedges, color=colors[s], label = legnames[signal], histtype="fill", ax=ax, zorder=10, alpha=0.3)
        hep.histplot(shist, sedges, color=colors[s], histtype="step", ax=ax, zorder=2)
    shists.append([signal, shist])
    ax.set_xticks([0.4, 1, 3, 5, 7, 10, 20, 30, 50])
    ax.set_xticklabels(["0.4", "1", "3", "5", "7", "10", "20", "30", "50"])
    ax.set_ylabel('Events / %.2f GeV'%(dedges[1] - dedges[0]), fontsize=28)
    ax.set_xlabel(r'$m_{\mu\mu}$ [GeV]', fontsize=28)
    #ax.text(0.03, 0.62, "Four-muon, overlapping", fontsize=23, color='black', horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    region_label = 'Dimuon: '
    lxybin = hn.split("_")[2]
    lxybin = (lxybin[3:]).split("to")
    lxy_label = r"$l_{{xy}} \in [{},{}]$ cm".format(lxybin[0].replace("p", ".").replace('.0', ''), lxybin[1].replace("p", ".").replace('.0', ''))
    region_label += lxy_label
    if "non-pointing" not in hn:
        isobin = "isolated" if hn.split("_")[3]=="iso1" else "non-isolated"
        region_label = region_label + ', ' + isobin
        ptbin = r"$p_{T}^{\mu\mu} > 25$ GeV" if hn.split("_")[4]=="pthigh" else r"$p_{T}^{\mu\mu} < 25$ GeV"
        region_label = region_label + ', ' + ptbin
    else:
        region_label = region_label + ', non-pointing'
    ax.text(0.03, 0.57, region_label, fontsize=22, color='black', horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.set_xlim(0.20, 50.0)
    #ax.set_ylim(0.1,800000*max(dhist))
    ax.set_ylim(h_[3][0],h_[3][1])
    ax.axvspan(0.41, 0.50, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # Ks
    ax.axvspan(0.51, 0.59, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # Eta
    ax.axvspan(0.73, 0.83, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # rho/w
    ax.axvspan(0.96, 1.08, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # phi
    ax.axvspan(2.91, 3.27, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # JPsi
    ax.axvspan(2.89, 3.33, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # JPsi
    ax.axvspan(3.47, 3.94, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # PSi2S
    ax.axvspan(8.88, 10.85, color='lightgray', ymin = 0.0, ymax = 0.54, alpha=1.0, zorder=1) # Upsilon
    ax.legend(loc="upper left", fontsize=20, frameon=False)
    fig.savefig(f"paperPlots/Figure_00{h_[1]}-{h_[2]}.png", dpi=140)
    fig.savefig(f"paperPlots/Figure_00{h_[1]}-{h_[2]}.pdf", dpi=140)

    if hepdata_input:
        data = {}
        data['mass_binned_values'] = []
        data['data_values'] = []
        data['data_unc'] = []
        for i in range(len(sedges) - 1):
            data['mass_binned_values'].append((sedges[i], sedges[i+1]))
            data['data_values'].append(dhist[i])
            data['data_unc'].append(y_err[i])
        for [signal, shist] in shists:
            data[signal] = []
            for i in range(len(shist)):
                data[signal].append(shist[i])
        with open(f"paperPlots/hepdata_Figure_00{h_[1]}-{h_[2]}.pkl", 'wb') as f:
            pickle.dump(data, f)


"""

#############
############## Figure 10 a)
#############

lumi=34.6
#f = ROOT.TFile('fitResults_2022_HTo2ZdTo2mu2x_vsCTau/d_Dimuon_lxy0p0to0p2_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-10.00mm_2022_workspace.root')
f = ROOT.TFile('fitResults_2022_HTo2ZdTo2mu2x_vsCTau/d_Dimuon_lxy0p2to1p0_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm_2022_workspace.root')
w = f.Get('wfit')
x = w.var("mfit")
minx = x.getMin()
maxx = x.getMax()
#nSig = w.var("signalNorm%s"%catExtS).getValV()
nBG = w.data("data_obs_ch10_2022").sumEntries() # 6
data = w.data("data_obs_ch10_2022") # 6
hd = x.createHistogram("hd",ROOT.RooFit.Binning(100,minx,maxx))                
data.fillHistogram(hd,ROOT.RooArgList(x))

# Background pdfs:
bpdf = w.pdf("roomultipdf_ch10_2022") # ch 6
nPDF = w.cat("pdf_index_ch10_2022").numTypes()
p  = []
pn = []
hp = []
hpr = []
numpars = []
gp = []
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
    nBins = 100
    hp.append(p[pp].createHistogram("hp%d"%pp,x,ROOT.RooFit.Binning(1*nBins,minx,maxx))) # 100*nBins
    hp[pp].SetLineColor(color)
    hp[pp].SetLineWidth(2)
    hp[pp].Scale(nBG)
    hpr.append(hp[pp].Clone("hpr%d"%pp))
    #hpr[pp].Rebin(100)
    #hp[pp].Scale(100.0)
    gp.append(ROOT.TGraph(hp[pp]))

# Data graph:
g_data = ROOT.TGraphAsymmErrors()
plotUtils.ConvertToPoissonGraph(hd, g_data, drawZeros=True, drawXerr=False)
g_data.SetMarkerStyle(20)
g_data.SetMarkerSize(1.2)
g_data.SetLineWidth(2)
g_data_clone = g_data.Clone()
g_data_clone.SetMarkerSize(0.0)

# Plot:
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
#hep.cms.label("", data=True, year=2022, lumi = lumi, com='13.6', ax=ax)
hep.cms.text("", loc=0, ax=ax, fontsize=30)
hep.cms.lumitext("%s fb$^{-1}$ (2022) (13.6 TeV)"%(lumi), ax=ax, fontsize=30, fontname=None)
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
ax.errorbar(x, y, xerr=[x_err_low, x_err_high], yerr=[y_err_low, y_err_high], fmt='o', color='black', label="Data", ms = 8, capsize=2)
bwidth = x[1] - x[0]
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
ax.text(0.03, 0.95, 'Dimuon', fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
ax.text(0.03, 0.88, r"$l_{{xy}} \in [0.2,1]$ cm", fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.8, r"Isolated", fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.74, r"$p^{{\mu\mu}}_{T} > 25$ GeV", fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.set_ylabel(r'Events / %.2f GeV'%(bwidth), fontsize=28)
ax.set_xlabel(r'$m_{\mu\mu}$ [GeV]', fontsize=28)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=25)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=25)
ax.set_xlim(minx, maxx)
ax.legend(loc='upper right', fontsize = 25, frameon = False, ncol=1)
fig.savefig("paperPlots/Figure_010-a.png", dpi=140)
fig.savefig("paperPlots/Figure_010-a.pdf", dpi=140)

if hepdata_input:
    data_hep = {}
    data_hep['mass_binned_values'] = []
    data_hep['data_values'] = []
    data_hep['data_unc_low'] = []
    data_hep['data_unc_high'] = []
    for i in range(len(x)):
        data_hep['mass_binned_values'].append((x[i] - x_err_low[i], x[i] + x_err_high[i]))
        data_hep['data_values'].append(y[i])
        data_hep['data_unc_low'].append(y_err_low[i])
        data_hep['data_unc_high'].append(y_err_high[i])
    data_hep['pdf_names'] = pn
    for pp in range(nPDF):
        data_hep[pn[pp]] = list(gp[pp].GetY())  # un valor por bin, ya rebinneado
    with open('paperPlots/hepdata_Figure_010-a.pkl', 'wb') as f:
        pickle.dump(data_hep, f)

#############
############## Figure 10 b)
#############

lumi=34.6
#f = ROOT.TFile('fitResults_2022_HTo2ZdTo2mu2x_vsCTau/d_Dimuon_lxy0p0to0p2_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-10.00mm_2022_workspace.root')
f = ROOT.TFile('fitResults_2022_HTo2ZdTo2mu2x_vsCTau/d_Dimuon_lxy0p2to1p0_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10.00mm_2022_workspace.root')
w = f.Get('wfit')
x = w.var("mfit")
minx = x.getMin()
maxx = x.getMax()
nSig = w.var("signalNorm_ch10_2022").getValV()
nSig = nSig * 0.1 # We transform 1pb into 100 fb for compatibility with new version of a)
mean = w.var("mean_ch10_2022").getValV()
sigma = w.var("sigma_ch10_2022").getValV()

# Signal pdf:
sp = w.pdf("signal_ch10_2022")
hs = sp.createHistogram("hs",x,ROOT.RooFit.Binning(1*nBins,minx,maxx)) # 100*nBins
#hs.Scale(nSig*100)
hs.Scale(nSig)
print("HERE", nSig)
g_signal = ROOT.TGraph(hs)
sp_gauss = w.pdf("gauss_ch10_2022")
sp_sigma = w.var("sigma_ch10_2022").getValV()
sp_mean = w.var("mean_ch10_2022").getValV()
mcfrac = w.var("mcfrac_ch10_2022").getValV()
hs_gauss = sp_gauss.createHistogram("hs_gauss",x,ROOT.RooFit.Binning(1*nBins,minx,maxx)) # 100*nBins
#hs_gauss.Scale(nSig*mcfrac*100)
hs_gauss.Scale(nSig*mcfrac)
g_gauss = ROOT.TGraph(hs_gauss)
sp_dcb = w.pdf("dcb_ch10_2022")
sp_alphaL = w.var("alphaL_ch10_2022").getValV()
sp_alphaR = w.var("alphaR_ch10_2022").getValV()
sp_nL = w.var("nL_ch10_2022").getValV()
sp_nR = w.var("nR_ch10_2022").getValV()
recfrac = 1.0 - mcfrac
hs_dcb = sp_dcb.createHistogram("hs_dcb",x,ROOT.RooFit.Binning(1*nBins,minx,maxx)) # 100*nBins
#hs_dcb.Scale(nSig*recfrac*100)
hs_dcb.Scale(nSig*recfrac)
g_dcb = ROOT.TGraph(hs_dcb)

# Signal MC:
mc = w.data("signalRooDataSet_ch10_2022")
frame = x.frame(minx,maxx);
mc.plotOn(frame, ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2), ROOT.RooFit.Binning(nBins,minx,maxx))
hmc = frame.getHist()
hmc.Scale(0.1) # For compatibility with 100 fb normalization

plt.style.use(hep.style.CMS)
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.text("Simulation", loc=0, ax=ax, fontsize=30)
hep.cms.lumitext("%s fb$^{-1}$ (2022) (13.6 TeV)"%(lumi), ax=ax, fontsize=30, fontname=None)
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
ax.errorbar(x, y, xerr=[x_err_low, x_err_high], yerr=[y_err_low, y_err_high], fmt='o', color='black', label="Signal simulation", ms = 8, capsize=2)
bwidth = x[1] - x[0]

#ax.plot(g_gauss.GetX(), g_gauss.GetY(), label='Gaussian', color='dodgerblue', lw = 3, ls=':')
#ax.plot(g_dcb.GetX(), g_dcb.GetY(), label='Double Crystal Ball', color='blue', lw = 3, ls=':')
#ax.plot(g_signal.GetX(), g_signal.GetY(), label='Total signal fit', color='magenta', lw = 3)
ax.plot(g_gauss.GetX(), g_gauss.GetY(), label='Gaussian', color='#e42536', lw = 3, ls=':')
ax.plot(g_dcb.GetX(), g_dcb.GetY(), label='Double Crystal Ball', color='#f89c20', lw = 3, ls=':')
ax.plot(g_signal.GetX(), g_signal.GetY(), label='Total signal fit', color='#5790fc', lw = 3) 
ax.text(0.03, 0.95, 'Dimuon', fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
ax.text(0.03, 0.88, r"$l_{{xy}} \in [0.2,1]$ cm", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.8, r"Isolated", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.74, r"$p^{{\mu\mu}}_{T} > 25$ GeV", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.60, r"$H\rightarrow Z_D Z_D$", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
#ax.text(0.03, 0.54, r"$m_{Z_D} = 5$ GeV, $c\tau_{0}^{Z_{D}} = 1$ cm", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.52, r"$m_{Z_D} = 5$ GeV", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.44, r"$c\tau_{0}^{Z_{D}} = 1$ cm", fontsize=24, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.set_ylabel(r'Events / %.2f GeV'%(bwidth), fontsize=28)
ax.set_xlabel(r'$m_{\mu\mu}$ [GeV]', fontsize=28)
ax.set_xlim(minx, maxx)
ax.set_ylim(0, 1.2) # 0, 3.5
ax.set_xticklabels(ax.get_xticklabels(), fontsize=25)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=25)
ax.legend(loc='upper right', fontsize = 24, frameon = False, ncol=1)
fig.savefig("paperPlots/Figure_010-b.png", dpi=140)
fig.savefig("paperPlots/Figure_010-b.pdf", dpi=140)

if hepdata_input:
    data_hep = {}
    data_hep['mass_binned_values'] = []
    data_hep['data_values'] = []
    data_hep['data_unc_low'] = []
    data_hep['data_unc_high'] = []
    for i in range(len(x)):
        data_hep['mass_binned_values'].append((x[i] - x_err_low[i], x[i] + x_err_high[i]))
        data_hep['data_values'].append(y[i])
        data_hep['data_unc_low'].append(y_err_low[i])
        data_hep['data_unc_high'].append(y_err_high[i])
    data_hep['Gaussian']          = list(g_gauss.GetY())
    data_hep['DoubleCrystalBall'] = list(g_dcb.GetY())
    data_hep['TotalSignalFit']    = list(g_signal.GetY())
    with open('paperPlots/hepdata_Figure_010-b.pkl', 'wb') as f:
        pickle.dump(data_hep, f)


#############
############## Figure 10 a) new
#############

lumi=34.6
f = ROOT.TFile("datacards_HTo2ZdTo2mu2x_Norm0.001_standard_Mar-23-2026_2022_NO-CONVERGE/higgsCombine_mdf_M5_ctau10_2022.MultiDimFit.mH120_BASELINE.root")
w = f.Get("w")
w.loadSnapshot("MultiDimFit")
x = w.var("mfit")
minx = x.getMin()
maxx = x.getMax()

ch_real = "ch10" 
ch_datacard = "ch9" # Here it's 9 for combine but 10 for the real name because we omitted osv region in datacard creation

data_all = w.data("data_obs")
data = data_all.reduce(f"CMS_channel==CMS_channel::{ch_datacard}")
hd = x.createHistogram("hd",ROOT.RooFit.Binning(100,minx,maxx))                
data.fillHistogram(hd,ROOT.RooArgList(x))

# Background pdfs:
nBins = 100
nBG = data.sumEntries() # 6
bpdf = w.pdf("shapeBkg_background_ch9") # ch 6
hbpdf = bpdf.createHistogram("hbpdf",x,ROOT.RooFit.Binning(1*nBins,minx,maxx)) # 100*nBins
hbpdf.Scale(w.var(f"shapeBkg_background_{ch_datacard}__norm").getVal())
gbpdf = ROOT.TGraph(hbpdf)
#
#nPDF = w.cat("pdf_index_ch9_2022").numTypes()
pdf_names = ['bernstein', 'powerlaw', 'exponential']
gp = []
pn = []
for pdf_name in pdf_names:
    pdf = w.pdf(f"background_{pdf_name}_{ch_real}_2022")
    if "exponential"==pdf_name:
        pn.append("Exponential (post-fit)")
    elif "powerlaw"==pdf_name:
       pn.append("Power-law (post-fit)")
    elif "bernstein"==pdf_name:
       pn.append("Bernstein, n = 2 (best post-fit)")
    else:
       pn.append("Uniform")
    hp.append(pdf.createHistogram("hp_%s"%pdf_name,x,ROOT.RooFit.Binning(1*nBins,minx,maxx))) # 100*nBins
    hp[-1].Scale(nBG)
    gp.append(ROOT.TGraph(hp[-1]))

# Signal (post-fit)
w.loadSnapshot("clean")
pdf_sig = w.pdf(f"shapeSig_signal_{ch_datacard}")
n_sig = w.function(f"n_exp_bin{ch_datacard}_proc_signal").getVal()
hsig = pdf_sig.createHistogram("hsig",x,ROOT.RooFit.Binning(1*nBins,minx,maxx)) # 100*nBins
print(n_sig) # 100 fb
hsig.Scale(n_sig*100) # scaling because postfit is zero
gsig = ROOT.TGraph(hsig)


# Data graph:
g_data = ROOT.TGraphAsymmErrors()
plotUtils.ConvertToPoissonGraph(hd, g_data, drawZeros=True, drawXerr=False)

# Plot:
fig, ax = plt.subplots(1, 1, figsize=(11, 8))
hep.cms.text("", loc=0, ax=ax, fontsize=30)
hep.cms.lumitext("%s fb$^{-1}$ (2022) (13.6 TeV)"%(lumi), ax=ax, fontsize=30, fontname=None)
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
ax.errorbar(x, y, xerr=[x_err_low, x_err_high], yerr=[y_err_low, y_err_high], fmt='o', color='black', label="Data", ms = 8, capsize=2)
bwidth = x[1] - x[0]
# Post-fit (just for checking because overlaps with the Bernstein)
#ax.plot(gbpdf.GetX(), gbpdf.GetY(), label='Post-fit background', color='yellow', lw = 3)
#
# Signal (post-fit)
ax.plot(gsig.GetX(), gsig.GetY(), label='Signal (pre-fit, $\sigma =$ 100 fb)', color='#3f90da', lw = 3)
# Pre-fit bkg pdfs
for p,pdf_name in enumerate(pdf_names):
    if "exponential"==pdf_name:
        col='#ffa90e'
        style = 'dashed'
        label = pn[p]
    elif "powerlaw"==pdf_name:
        col='#bd1f01'
        style = 'dashed'
        label = pn[p]
    elif "bernstein"==pdf_name:
        col='#94a4a2'
        col='#964a8b'
        style = 'solid' # Because it's the one picked
        label = pn[p] 
    else:
        col='slategrey'
    ax.plot(gp[p].GetX(), gp[p].GetY(), label=label, color=col, lw = 3, linestyle=style)
    ax.set_ylim(0, 2*max(y))
#
ax.text(0.03, 0.95, 'Dimuon', fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, fontweight='bold')
ax.text(0.03, 0.88, r"$l_{{xy}} \in [0.2,1]$ cm", fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.8, r"Isolated", fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.text(0.03, 0.74, r"$p^{{\mu\mu}}_{T} > 25$ GeV", fontsize=25, color='black', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
ax.set_ylabel(r'Events / %.2f GeV'%(bwidth), fontsize=28)
ax.set_xlabel(r'$m_{\mu\mu}$ [GeV]', fontsize=28)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=25)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=25)
ax.set_xlim(minx, maxx)
ax.set_ylim(0, 30) # overwrites what was put before
ax.legend(loc='upper right', fontsize = 25, frameon = False, ncol=1)
fig.savefig("paperPlots/Figure_010-a.png", dpi=140)
fig.savefig("paperPlots/Figure_010-a.pdf", dpi=140)
