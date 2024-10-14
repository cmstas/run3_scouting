import ROOT
import numpy
import copy
import os,sys
from datetime import date
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def getValues(histo):
    values = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(bins)

def plotBiasDistribution(name, h, fg, xlabel, ylabel = 'Number of toys', outDir = 'output_bias'):
        plt.style.use(hep.style.CMS)
        fig, ax = plt.subplots(figsize=(10, 10))
        bins = h.GetNbinsX()
        vx = [h.GetBinLowEdge(i) for i in range(1, bins + 1)]
        vx.append(h.GetBinLowEdge(bins) + h.GetBinWidth(bins))
        vy = [h.GetBinContent(i) for i in range(1, bins + 1)]
        vyerr = [h.GetBinError(i) for i in range(1, bins + 1)]
        x_fit = np.linspace(-5.0, 5.0, 1000)
        y_fit = [fg.Eval(xi) for xi in x_fit]
        quantiles = np.zeros(1)
        prob = np.array([0.5])
        h.GetQuantiles(1, quantiles, prob)
        hep.histplot(vy, bins=vx, ax=ax,histtype='step')
        ax.plot(x_fit, y_fit, label='Gaussian fit', color='tab:red')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend(loc='best', frameon = True)
        ax.text(0.65, 0.8, 'Fit parameters:', fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.text(0.65, 0.76, r' - Mean = %.2f $\pm$ %.2f'%(fg.GetParameter(1),fg.GetParError(1)), fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.text(0.65, 0.72, r' - Width = %.2f $\pm$ %.2f'%(fg.GetParameter(2),fg.GetParError(2)), fontsize=18, color='tab:red', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.text(0.03, 0.90, 'Mean = %.2f'%(h.GetMean()), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.text(0.03, 0.85, 'Median = %.2f'%(quantiles[0]), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.text(0.03, 0.81, 'std. dev = %.2f'%(h.GetStdDev()), fontsize=18, color='tab:blue', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        ax.text(0.03, 0.97, r'$r_{in} = %.0f x r_{+2\sigma} (r_{+2\sigma} = %.2f)$'%(float(r),expLim), fontsize=18, color='k', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        hep.cms.label("Internal", data=True, year=2022, com='13.6')
        fig.savefig("%s/bias_%s.png"%(outDir,name), dpi=140)

def plotDistribution(name, h, xlabel, ylabel = 'Number of toys', outDir = 'output_bias', line=None):
        plt.style.use(hep.style.CMS)
        fig, ax = plt.subplots(figsize=(10, 10))
        bins = h.GetNbinsX()
        vx = [h.GetBinLowEdge(i) for i in range(1, bins + 1)]
        vx.append(h.GetBinLowEdge(bins) + h.GetBinWidth(bins))
        vy = [h.GetBinContent(i) for i in range(1, bins + 1)]
        vyerr = [h.GetBinError(i) for i in range(1, bins + 1)]
        hep.histplot(vy, bins=vx, ax=ax,histtype='step')
        if line:
            ax.axvline(x=line, color='red', linestyle='--', label='Injected r = %.3f'%line)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend(loc='best', frameon = True)
        hep.cms.label("Internal", data=True, year=2022, com='13.6')
        fig.savefig("%s/bias_%s.png"%(outDir,name), dpi=140)

ROOT.gROOT.SetBatch(1)

user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

inDir = sys.argv[1]
thisDir = os.environ.get("PWD")

sigModel = "HTo2ZdTo2mu2x"

outDir = ("%s/plotsBias_"%(thisDir))+today
if not os.path.exists(outDir):
    os.makedirs(outDir)
os.system('cp '+os.environ.get("PWD")+'/utils/index.php '+outDir)

# not really needed here but will need them for the future tests per bin
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
if sigModel=="HTo2ZdTo2mu2x":
    sigMasses = [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
    sigMasses = [5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
    sigCTaus = [1, 10, 100]
    #sigMasses = [5.0]
    #sigCTaus = [10]
elif sigModel=="ScenarioB1":
    sigMasses = [1.33]
    sigCTaus = [0.1, 1, 10, 100]

# Fit types
fitTypes = ['envelope']

# Injected charge
rinj = [5]

## Loop to make the plots
for fit in fitTypes:
    for r in rinj:
        median_sig = []
        median_rel = []
        mean_sig = []
        mean_rel = []
        mass_xbins = []
        for _t,t in enumerate(sigCTaus):
            median_sig.append([])
            median_rel.append([])
            mean_sig.append([])
            mean_rel.append([])
            mass_xbins.append([])
            for m in sigMasses:
                ## Access the limit to know what was injected...
                expLim = 1.0 # provisional
                limFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Sep-30-2024_2022/limits_HTo2ZdTo2mu2x_2022.txt'
                if os.path.exists(limFile):
                    print('> Limit file opened successfully')
                    flim = open(limFile,"r")
                    for ll in flim.readlines():
                        if ll.split(",")[1]!=str(m) or ll.split(",")[2]!=str(t):
                            continue
                        expLim=float(ll.split(",")[8]) # Expected limit
                        break
                    flim.close()
                    print('> Found expected limit %f'%(expLim))
                else:
                    print('> Expected limit not found')
                ## Access results:
                try:
                    fd = ROOT.TFile.Open("%s/fitDiagnostics_%s_M%.1f_ctau%i_r%i_%s_combined.root"%(inDir,sigModel,m,t,r,fit))
                except OSError:
                    print('Skipping point...')
                    continue
                td = fd.Get("tree_fit_sb")
                hs = ROOT.TH1D("hs","",41,-6.1,6.1) # Bias wrt sigma
                hr = ROOT.TH1D("hr","",41,-3.0,3.0) # Bias wrt injected value
                hrout = ROOT.TH1D("hrout","",50,0,float(r)*expLim+5)
                hrLoErr = ROOT.TH1D("hrLoErr","",50,0,round(float(r)*expLim)+1)
                hrHiErr = ROOT.TH1D("hrHiErr","",50,0,round(float(r)*expLim)+1)
                # Draw
                #condition = "fit_status>-1 && abs(r-%f)<20.0 && (r-rLoErr)>0.11 && rHiErr>0 && rLoErr>0"%(float(r)*expLim)
                condition = "fit_status>-1 && rHiErr>0 && rLoErr>0"
                todraw = "(r-%f)/((rLoErr/rHiErr>3.0 || rHiErr/rLoErr>3.0) ? rErr : (r>%f ? rLoErr : rHiErr))>>hs"%(float(r)*expLim,float(r)*expLim)
                td.Draw(todraw,condition,"goff")
                todraw = "(r-%f)/%f>>hr"%(float(r)*expLim,float(r)*expLim)
                td.Draw(todraw,condition,"goff")
                td.Draw("r>>hrout",condition,"goff")
                td.Draw("rLoErr>>hrLoErr",condition,"goff")
                td.Draw("rHiErr>>hrHiErr",condition,"goff")
                # Fit
                fs = ROOT.TF1("fg","gaus",-5.0,5.0)
                fs.SetLineColor(2)
                hs.Fit(fs,"0L","",-5.0,5.0)
                fr = ROOT.TF1("fr","gaus",-2.5,2.5)
                fr.SetLineColor(2)
                hr.Fit(fs,"0L","",-2.5,2.5)
                print('Valid %i toys'%(hs.GetEntries()))
                squantiles = np.zeros(1)
                hs.GetQuantiles(1, squantiles, np.array([0.5]))
                rquantiles = np.zeros(1)
                hr.GetQuantiles(1, rquantiles, np.array([0.5]))
                mean_sig[_t].append(fs.GetParameter(1))
                median_sig[_t].append(squantiles[0])
                #mean_sig[_t].append(fr.GetParameter(1))
                #median_sig[_t].append(rquantiles[0])
                mass_xbins[_t].append(m)
                plotBiasDistribution('%s_M%.1f_ctau_%i_r%i_%s_combined'%(sigModel,m,t,r,fit), hs, fs, xlabel=r'$(r_{out} - r_{in})/\sigma_{r}$', outDir = outDir)
                #plotBiasDistribution('%s_M%.1f_ctau_%i_r%i_%s_combined_relative'%(sigModel,m,t,r,fit), hr, fr, xlabel=r'$(r_{out} - r_{in})/r_{in}$', outDir = outDir)
                plotDistribution('rout_%s_M%.1f_ctau_%i_r%i_%s_combined'%(sigModel,m,t,r,fit), hrout, xlabel=r'$r_{out}$', ylabel = 'Number of toys', outDir = outDir, line=float(r)*expLim)
                plotDistribution('rLoErr_%s_M%.1f_ctau_%i_r%i_%s_combined'%(sigModel,m,t,r,fit), hrLoErr, xlabel='rLoErr', ylabel = 'Number of toys', outDir = outDir, line=float(r)*expLim)
                plotDistribution('rHiErr_%s_M%.1f_ctau_%i_r%i_%s_combined'%(sigModel,m,t,r,fit), hrHiErr, xlabel='rHiErr', ylabel = 'Number of toys', outDir = outDir, line=float(r)*expLim)
        # Summary plot:
        plt.style.use(hep.style.CMS)
        colors = ['#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6', '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd']
        fig, ax = plt.subplots(figsize=(16, 5)) 
        fig.subplots_adjust(bottom=0.2, right=0.80)
        luminosity = 35
        hep.cms.label("Preliminary", data=True, lumi=luminosity, year=2022, com='13.6')
        fig.text(0.35, 0.9, r'Bias tests with $r_{in} = %i x r_{+2\sigma}$'%(r), color='black', fontsize = 14)
        ax.set_ylabel(r'Median of $(r_{out} - r_{in})/\sigma_{r}$', fontsize=20)
        ax.set_xlabel(r'Dimuon mass $m_{\mu\mu}$', fontsize=20)
        ax.set_ylim(-4, 4)
        ax.set_xscale('log')
        for _t,t in enumerate(sigCTaus):
            ax.plot(mass_xbins[_t], median_sig[_t], label=r'$c\tau = $%i mm'%(t), color=colors[_t],marker='o')
        ax.legend(loc='best', frameon = True, fontsize = 14)
        ## Save
        fig.savefig('%s/summary_median_%s_M%.1f_ctau_%i_r%i_%s_combined.png'%(outDir, sigModel,m,t,r,fit), dpi=140)
        
        






