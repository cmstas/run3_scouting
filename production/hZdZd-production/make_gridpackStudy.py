import ROOT
import os,sys,json
from datetime import date    
import numpy as np
import argparse
from tqdm import tqdm
from DataFormats.FWLite import Events, Handle
import mplhep as hep
import matplotlib.pyplot as plt

MUON_MASS = 0.10566
user = os.environ.get("USER")
today= date.today().strftime("%b-%d-%Y")

def getValues(histo):
    values = []
    errors = []
    bins = []
    for n in range(1, histo.GetNbinsX()+1):
        values.append(histo.GetBinContent(n))
        errors.append(histo.GetBinError(n))
        bins.append(histo.GetBinLowEdge(n))
    bins.append(histo.GetBinLowEdge(n) + histo.GetBinWidth(n))
    return np.array(values), np.array(errors), np.array(bins)

def getGenInfo(events):
    ghandle = Handle('std::vector<reco::GenParticle>')
    glabel  = ("genParticles")
    #
    th1f_ptZd = ROOT.TH1F('ptZd', '', 40, 0, 100)
    th1f_lxyZd = ROOT.TH1F('lxyZd', '', 35, 0, 70)
    th1f_lZd = ROOT.TH1F('lZd', '', 35, 0, 70)
    th1f_mZd = ROOT.TH1F('mZd', '', 60, 13, 15)
    th1f_ptZd.Sumw2()
    th1f_lxyZd.Sumw2()
    th1f_lZd.Sumw2()
    th1f_mZd.Sumw2()
    #
    for en,e in tqdm(enumerate(events), total=events.size(), desc="Processing", unit="event"):
        #
        e.getByLabel(glabel,ghandle)
        genParticles = ghandle.product()
        #
        for gn,g in enumerate(genParticles):
            if not (g.isLastCopy()):
                continue
            if abs(g.pdgId())==1023: # Dark photon
                th1f_ptZd.Fill(g.pt())
                th1f_mZd.Fill(g.mass())
                vx_i = g.vx()
                vy_i = g.vy()
                vz_i = g.vz()
                for dn in range(g.numberOfDaughters()):
                    if (abs(g.daughter(dn).pdgId())==13):
                        vx_f = g.daughter(dn).vx()
                        vy_f = g.daughter(dn).vy()
                        vz_f = g.daughter(dn).vz()
                        th1f_lxyZd.Fill(((vx_f-vx_i)**2.0 + (vy_f-vy_i)**2.0)**0.5)
                        th1f_lZd.Fill(((vx_f-vx_i)**2.0 + (vy_f-vy_i)**2.0 + (vz_f-vz_i)**2.0)**0.5)
                        break
    #
    th1f_ptZd.Scale(1./th1f_ptZd.Integral())
    th1f_mZd.Scale(1./th1f_mZd.Integral())
    th1f_lxyZd.Scale(1./th1f_lxyZd.Integral())
    th1f_lZd.Scale(1./th1f_lZd.Integral())
    #
    return [th1f_ptZd, th1f_lxyZd, th1f_lZd, th1f_mZd]


# Load the events
file_bw15 = 'configs/output_gensim_bw15.root'
file_bw15k = 'configs/output_gensim_bw15000.root'
#
events_bw15 = Events(file_bw15)
events_bw15k = Events(file_bw15k)
#
histograms_bw15 = getGenInfo(events_bw15)
histograms_bw15k = getGenInfo(events_bw15k)
xlabel = [r'Dark photon $Z_{D}$ $p_{T}$ (GeV)', r'Dark photon $Z_{D}$ $l_{xy}$ (cm)', r'Dark photon $Z_{D}$ $L$ (cm)', r'Dark photon $Z_{D}$ mass $m_{Z_{D}}$ (GeV)']
name = ['Zd_pt', 'Zd_lxy', 'Zd_L', 'Zd_mass']
#
for h in range(0, len(histograms_bw15)):
    plt.style.use(hep.style.CMS)
    fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05}, sharex=True, figsize=(10, 10))
    hep.cms.label("Preliminary", data=False, year='2022', ax=ax)
    # errors and ratio
    h_bw15, e_bw15, b_bw15= getValues(histograms_bw15[h])
    h_bw15k, e_bw15k, b_bw15k= getValues(histograms_bw15k[h])
    ratio = histograms_bw15k[h].Clone('Ratio')
    ratio.Divide(histograms_bw15[h])
    h_ratio, e_ratio, b_ratio= getValues(ratio)
    #
    hep.histplot(h_bw15, b_bw15, color="teal", label = r'bwcutoff=15', histtype="step", ax=ax)
    hep.histplot(h_bw15k, b_bw15k, color="orange", label = r'bwcutoff=15000', histtype="step", ax=ax)
    ax.legend(loc='upper right', fontsize = 18, frameon = True, ncol=1, title=r'$h\rightarrow Z_DZ_D$ $(Z_D\rightarrow\mu\mu)$', title_fontsize=20)
    if 'mass' in name[h] or 'pt' in name[h]:
        ax.set_ylabel(r'Normalized event yield / %.1f GeV'%(b_bw15[1] - b_bw15[0]), fontsize=24)
    else:
        ax.set_ylabel(r'Normalized event yield / %.1f cm'%(b_bw15[1] - b_bw15[0]), fontsize=24)
    ax.set_xlim(b_bw15[0], b_bw15[-1])
    #
    pratio = b_ratio + 0.5*(b_ratio[1] - b_ratio[0])
    ax_ratio.errorbar(pratio[:-1], h_ratio, yerr=e_ratio, xerr=0.5*(b_ratio[1] - b_ratio[0]), fmt='o', capsize=5, color='k', markersize=8)
    ax_ratio.set_xlabel(xlabel[h])
    ax_ratio.set_ylabel('Ratio')
    ax_ratio.set_ylim(0.0, 2.0)
    ax_ratio.set_xlim(b_bw15[0], b_bw15[-1])
    #
    fig.savefig('%s.png'%(name[h]), dpi=140)



#### Write histograms
#foname = "%s/histograms_GEN_%s_all.root"%(outdir,args.year)
#if args.inSample!="*":
#    if args.inFile!="*":
#        foname = "%s/histograms_GEN_file%s_%s_%s"%(outdir,args.inFile,args.inSample,args.year)
#    else:
#        foname = "%s/histograms_GEN_%s_%s"%(outdir,args.inSample,args.year)
#if index>=0:
#    foname = foname+("_%d"%index)
#fout = ROOT.TFile(foname+".root","RECREATE")
#fout.cd()
#for h in h1d:
#    h.Write()
#for h in h2d:
#    h.Write()
#fout.Close()
