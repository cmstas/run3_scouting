import os,sys,math
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import ROOT

def getLowerMask(lowerBound):
    window_size = 5.0
    rel_sigma = 0.018
    print(lowerBound / (1 + window_size*rel_sigma))
    return lowerBound / (1 + window_size*rel_sigma)

def getUpperMask(upperBound):
    window_size = 5.0
    rel_sigma = 0.018
    print(upperBound / (1 - window_size*rel_sigma))
    return upperBound / (1 - window_size*rel_sigma)

def returnBEfficiency(mass_value):
    b_masses = np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.25, 1.5, 2.0, 2.85, 3.35, 4.0, 4.6])
    b_effs = np.array([0.3109463377536955, 0.26847013244436435, 0.24992711206799884, 0.23842898102216356, 0.23993801096038092, 0.23418752437541582, 0.24130093865769678, 0.24386724386724387, 0.26277917030444703, 0.31348230996459736, 0.36339318819852745, 0.4446176059404579, 0.5748189563275079])
    graph = ROOT.TGraph(len(b_effs), np.array(b_masses), np.array(b_effs))
    spline = ROOT.TSpline3("spline_BToPhi_efficiency", graph)
    print(f"Efficiency for {mass_value} is {spline.Eval(mass_value)}")
    return spline.Eval(mass_value)


ROOT.gROOT.SetBatch(1)
drawObserved = True
drawPoints = False
maskSMResonances = True
NORMCONST = 0.01 # Needs to be consistent with what it was put on make_datacards.py e.g. if signal was scaled by NORMCONST xsec should be multiplied by it
typeOfLimit = "BRH" # "r", "xsec", "xsecBR" "BRH" 
xsec_base = 1.0 # in pb, used to normalize the MC
xsec_h = 59.8 # higgs cross section in pb at 13.6 GeV, used to normalize the MC
scaleToFullLumi = False
compare = True
doSmartScaling = True
hepdata_input=True

# In-line arguments
model = sys.argv[1]
limdir = sys.argv[2]
ctau = sys.argv[3]
year = sys.argv[4]
if len(sys.argv) > 5:
    limtype = sys.argv[5]
else:
    limtype = 'asymptotic'

if year=='2022':
    luminosity = 35
elif year=='2023':
    luminosity = 27
else:
    luminosity = 62.4

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

fin = open("%s/limits_%s_%s_%s.txt"%(limdir,model,limtype,year),"r")
for l in fin.readlines():
    if l.startswith("#"):
        continue
    ls = l.split(",")
    if ls[0]!=model:
        continue
    if float(ls[2])!=float(ctau):
        continue
    scale = 1.0
    # Smart scaling
    if doSmartScaling:
        if model=="HTo2ZdTo2mu2x":
            scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_asymptotic_vsMass_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
            with open(scalingFile) as fin:
                for ll in fin.readlines():
                    if ll.startswith("#"):
                        continue
                    lls = ll.split(",")
                    if (float(lls[1])== float(ls[1])) and (float(lls[2])== float(ls[2])):
                        e2m = float(lls[5])
                        NORMCONST = 0.01 * ( e2m / 0.6 )
                        print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                        xsec = xsec_base*NORMCONST
                        break
        if model=="BToPhi":
            #scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_1mm.txt' # Will have to merge
            #scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_10-100mm.txt'
            scalingFile = 'combineScripts/SmartLimitNorm/limits_BToPhi_asymptotic_allEras_vsCTau.txt' # Will have to merge
            with open(scalingFile) as fin:
                for ll in fin.readlines():
                    if ll.startswith("#"):
                        continue
                    lls = ll.split(",")
                    if (float(lls[1])== float(ls[1])) and (float(lls[2])== float(ls[2])):
                        e2m = float(lls[5])
                        NORMCONST = 1.0 * ( e2m / 0.6 )
                        print(" -> Using smart scaling of %.2f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                        xsec = xsec_base*NORMCONST
                        break

    else:
        xsec = xsec_base*NORMCONST
    if typeOfLimit=="xsec":
        scale = xsec
    if typeOfLimit=="BRH":
        if 'BToPhi' in model:
            eff_m = returnBEfficiency(float(ls[1])) 
            scale = xsec/(2.0 * 1.2890e+08 * eff_m) # Here the value of the cross section is harcoded
        else:
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
        #print(float(ls[1]), float(ls[4]), BR)
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
    l_dmu_Comb = None
    print("> Request to open files to compare")
    try:
        if model=="HTo2ZdTo2mu2x":
            if typeOfLimit=="BRH":
                l_dmu_13TeV = None
                l_dmu_13p6TeV = None
                l_dmu_Comb = None
                m_dmu = np.array([10., 20., 30., 40., 50.])
                if ctau=="1.00":
                    # Run 2 scouting
                    cfile = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Figure_8a.root")
                    cgobs = cfile.Get("Figure 8a/Graph1D_y1")
                    cgexp = cfile.Get("Figure 8a/Graph1D_y2")
                    l_dmu_13TeV   = np.array([7.2291e-05, 3.2762e-05, 3.5112e-05, 3.9441e-05, 3.6307e-05])
                    l_dmu_13p6TeV = np.array([8.8575e-05, 3.8366e-05, 3.9471e-05, 3.994e-05, 5.3028e-05])
                    l_dmu_Comb    = np.array([4.1748e-05, 1.8494e-05, 1.9962e-05, 2.0341e-05, 2.4934e-05])
                if ctau=="10.00":
                    l_dmu_13TeV   = np.array([5.6854e-05, 2.3299e-05, 2.4819e-05, 2.5004e-05, 2.9119e-05])
                    l_dmu_13p6TeV = np.array([6.7676e-05, 3.1077e-05, 2.8641e-05, 2.8811e-05, 2.7618e-05])
                    l_dmu_Comb    = np.array([3.3205e-05, 1.419e-05, 1.3834e-05, 1.452e-05, 1.5585e-05])
                if ctau=="100.00":
                    cfile = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Figure_8b.root")
                    cgobs = cfile.Get("Figure 8b/Graph1D_y1")
                    cgexp = cfile.Get("Figure 8b/Graph1D_y2")
                    l_dmu_13TeV   = np.array([0.00013573, 4.6619e-05, 2.7188e-05, 3.9799e-05, 3.8551e-05])
                    l_dmu_13p6TeV = np.array([0.00016167, 5.5121e-05, 4.5706e-05, 4.9023e-05, 3.6362e-05])
                    l_dmu_Comb    = np.array([7.9462e-05, 2.6091e-05, 2.0618e-05, 2.2415e-05, 1.9732e-05])
                if ctau=="1000.00":
                    l_dmu_Comb    = np.array([0.00045647, 0.00014209, 5.2258E-05, 6.4816E-05, 5.1325E-05])
        if model=="BToPhi":
            if ctau=="1.00":
                cfile = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Figure_6a.root")
                cgobs = cfile.Get("Figure 6a/Graph1D_y1")
                cgexp = cfile.Get("Figure 6a/Graph1D_y2")
            if ctau=="100.00":
                cfile = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Figure_6b.root")
                cgobs = cfile.Get("Figure 6b/Graph1D_y1")
                cgexp = cfile.Get("Figure 6b/Graph1D_y2")
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

# Plot the limit
plt.style.use(hep.style.CMS)
#
fig, ax = plt.subplots(figsize=(11, 8))
#
if drawObserved:
    ax.plot(massv, obsv, 'k-', label='Observed', linewidth=2, zorder=2)
#
ax.plot(massv, expv, 'r--', label='Expected', linewidth=2, zorder=2)
#
ax.fill_between(massv, m2sv, p2sv, color='#FFDF7Fff', label=r'95% CL expected', zorder=1) # #F5BB54
ax.fill_between(massv, m1sv, p1sv, color='#85D1FBff', label=r'68% CL expected', zorder=1) # #607641
#
if compare:
    if l_dmu_Comb is not None:
        #ax.plot(m_dmu, l_dmu_13TeV, linestyle='solid', color='magenta', label=r'Displaced dimuon (13 TeV, 97.6 $fb^{-1}$) [Observed]', linewidth=2)
        #ax.plot(m_dmu, l_dmu_13p6TeV, linestyle='solid', color='deepskyblue', label=r'Displaced dimuon (13.6 TeV, 36.6 $fb^{-1}$) [Observed]', linewidth=2)
        ax.plot(m_dmu, l_dmu_Comb, linestyle='solid', color='magenta', label=r'JHEP 05 (2024) 047', linewidth=2)
    if cfile is not None:
        m_cgexp = np.array(cgexp.GetX())
        l_cgexp = np.array(cgexp.GetY())
        print(m_cgexp)
        #indices = np.searchsorted(m_cgexp, [0.695, 1.18, 2.76, 4.28, 8.0, 11.5])
        if model=="HTo2ZdTo2mu2x":
            if float(ctau)==1.00:
                indices = np.searchsorted(m_cgexp, [0.695, 0.895, 0.91, 1.14, 2.76, 4.16, 8.32, 11.5]) # 1mm
            if float(ctau)==100.00:
                indices = np.searchsorted(m_cgexp, [0.695, 1.18, 2.76, 4.16, 8.48, 11.9]) # 100 mm
        if model=="BToPhi":
            if float(ctau)==1.00:
                indices = np.searchsorted(m_cgexp, [0.408, 0.615, 0.685, 0.885, 0.905, 1.14, 2.74, 4.12]) # 1mm
            if float(ctau)==100.00:
                indices = np.searchsorted(m_cgexp, [0.408, 0.615, 0.685, 0.885, 0.905, 1.14, 2.76, 4.12])  # 100 mm
        #indices = np.searchsorted(m_cgexp, [0.695, 1.18, 2.76, 4.16, 8.48, 11.9]) # 100 mm
        #indices = np.searchsorted(m_cgexp, [0.695, 0.895, 0.91, 1.14, 2.76, 4.16, 8.32, 11.5]) # 1mm
        segments_m_cgexp = np.split(m_cgexp, indices)
        segments_l_cgexp = np.split(l_cgexp, indices)
        print(segments_m_cgexp)
        ax.plot(segments_m_cgexp[0], segments_l_cgexp[0], 'b-', label=r'JHEP 04 (2022) 062', linewidth=2, zorder=10)
        #ax.plot(segments_m_cgexp[0], segments_l_cgexp[0], 'b-', label=r'JHEP 04 (2022) 062', linewidth=2)
        ax.plot(segments_m_cgexp[2], segments_l_cgexp[2], 'b-', linewidth=2, zorder=10)
        ax.plot(segments_m_cgexp[4], segments_l_cgexp[4], 'b-', linewidth=2, zorder=10)
        ax.plot(segments_m_cgexp[6], segments_l_cgexp[6], 'b-', linewidth=2, zorder=10)
        if model=="HTo2ZdTo2mu2x" and ctau!="100.00" and ctau!="1000.00":
            ax.plot(segments_m_cgexp[8], segments_l_cgexp[8], 'b-', linewidth=2, zorder=10)
        if model=="BToPhi":
            ax.plot(segments_m_cgexp[8], segments_l_cgexp[8], 'b-', linewidth=2, zorder=10)
#

# Masking
ax.axvspan(getLowerMask(0.41), getUpperMask(0.50), color='lightgray', alpha=1.0, zorder=2) # Ks
ax.axvspan(getLowerMask(0.51), getUpperMask(0.59), color='lightgray', alpha=1.0, zorder=2) # Eta
ax.axvspan(getLowerMask(0.73), getUpperMask(0.83), color='lightgray', alpha=1.0, zorder=2) # rho/w
ax.axvspan(getLowerMask(0.96), getUpperMask(1.08), color='lightgray', alpha=1.0, zorder=2) # phi
ax.axvspan(getLowerMask(2.91), getUpperMask(3.27), color='lightgray', alpha=1.0, zorder=2) # JPsi
ax.axvspan(getLowerMask(2.89), getUpperMask(3.33), color='lightgray', alpha=1.0, zorder=2) # JPsi
ax.axvspan(getLowerMask(3.47), getUpperMask(3.94), color='lightgray', alpha=1.0, zorder=2) # PSi2S
ax.axvspan(getLowerMask(8.88), getUpperMask(10.85), color='lightgray', alpha=1.0, zorder=2) # Upsilon


#ax.set_ylim(0.5*min(m2sv), 50.0*max(p2sv))
#ax.set_ylim(1e-6, 1e-1)
ax.set_axisbelow(False)
ax.tick_params(zorder=10)
#
if year!='allEras':
    hep.cms.label(loc=0, data=True, llabel="", lumi=luminosity, year=year, com=13.6)
else:
    hep.cms.label(loc=0, data=True, llabel="", lumi=luminosity, com=13.6)
#
if model=="HTo2ZdTo2mu2x":
    if ctau=='1.00':
        ctaulabel = '0.1'
    if ctau=='10.00':
        ctaulabel = '1'
    if ctau=='100.00':
        ctaulabel = '10'
    if ctau=='1000.00':
        ctaulabel = '100'
    legend = ax.legend(loc='upper right', title=r"$H\rightarrow Z_DZ_D$ ($c\tau =$ %s cm)"%(ctaulabel), fontsize=22, title_fontsize=22, frameon = True)
elif model=="BToPhi":
    if ctau=='1.00':
        ctaulabel = '0.1'
        location = 'upper left'
    if ctau=='10.00':
        ctaulabel = '1'
        location = 'upper right'
    if ctau=='100.00':
        ctaulabel = '10'
        location = 'upper right'
    legend = ax.legend(loc=location, title=r"$h_{b}\rightarrow \phi X$ ($c\tau =$ %s cm)"%(ctaulabel), fontsize=22, title_fontsize=22, frameon = True)

legend.get_title().set_weight('bold')
legend.set_zorder(10)
legend._legend_box.align = "left"
#
#
# Other details
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Mass [GeV]')
if model=="HTo2ZdTo2mu2x":
    ax.set_ylabel(r'95% CL upper limit on $\mathcal{B}$($H \rightarrow Z_D Z_D$)')
    ax.set_xlim(massv[0], massv[-1])
    ax.set_xlim(0.5, 50)
    if ctau=="1.00":
        ax.set_ylim(4e-6, 1e-1)
        ax.set_xticks([0.5, 1, 2, 5, 10, 20, 30, 50])
        ax.set_xticklabels(["0.5", "1", "2", "5", "10", "20", "30", "50"])
    if ctau=="10.00":
        ax.set_ylim(4e-6, 5e-1)
        ax.set_xticks([0.5, 1, 2, 5, 10, 20, 30, 50])
        ax.set_xticklabels(["0.5", "1", "2", "5", "10", "20", "30", "50"])
    if ctau=="100.00":
        ax.set_ylim(4e-6, 5)
        ax.set_xlim(1.5, 50)
        ax.set_xticks([2, 5, 10, 20, 30, 50])
        ax.set_xticklabels(["2", "5", "10", "20", "30", "50"])
    if ctau=="1000.00":
        ax.set_ylim(1e-5, 10)
        ax.set_xlim(2.0, 50)
        ax.set_xticks([2, 5, 10, 20, 30, 50])
        ax.set_xticklabels(["2", "5", "10", "20", "30", "50"])
elif "BToPhi" in model:
    ax.set_xlim(0.3, 4.6)
    ax.set_xticks([0.3, 0.4, 0.5, 0.6, 0.8, 1, 2, 3, 4])
    ax.set_xticklabels(["0.3", "0.4", "0.5", "0.6", "0.8", "1", "2", "3", "4"])
    if ctau=="1.00":
        ax.set_ylim(5e-11, 1e-5)
    if ctau=="10.00":
        ax.set_ylim(1e-11, 1e-5)
    if ctau=="100.00":
        ax.set_ylim(5e-12, 3e-3)
    ax.set_ylabel(r'95% CL limit on $\mathcal{B}$($h_{b} \rightarrow \phi X$)x$\mathcal{B}$($\phi \rightarrow \mu\mu$)')
    #ax.set_xlim(ctauv[0], ctauv[-1])


ax.set_axisbelow(False)
ax.tick_params(zorder=10)
#
#
if drawObserved:
    fig.savefig("%s/limits_%s_ctau%s_%s_alt_obs"%(limdir,model,ctau.replace('.','p'),typeOfLimit), dpi=140)
    fig.savefig("%s/limits_%s_ctau%s_%s_alt_obs.pdf"%(limdir,model,ctau.replace('.','p'),typeOfLimit), dpi=140)
else:
    fig.savefig("%s/limits_%s_ctau%s_%s_alt"%(limdir,model,ctau.replace('.','p'),typeOfLimit), dpi=140)
    fig.savefig("%s/limits_%s_ctau%s_%s_alt.pdf"%(limdir,model,ctau.replace('.','p'),typeOfLimit), dpi=140)

import pickle
if hepdata_input:
    if model=="HTo2ZdTo2mu2x":
        if ctau=="1.00":
            name = "Figure_011-a"
        if ctau=="10.00":
            name = "Figure_011-b"
        if ctau=="100.00":
            name = "Figure_011-c"
        if ctau=="1000.00":
            name = "Figure_011-d"
    if model=="BToPhi":
        if ctau=="1.00":
            name = "Figure_015-a"
        if ctau=="10.00":
            name = "Figure_015-b"
        if ctau=="100.00":
            name = "Figure_015-c"
    fig.savefig(f"paperPlots/{name}.png", dpi=140)
    fig.savefig(f"paperPlots/{name}.pdf", dpi=140)
    data_hep = {}
    data_hep['mass_values'] = massv
    data_hep['expected_values'] = expv
    data_hep['observed_values'] = obsv
    data_hep['p2sigma_values'] = p2sv
    data_hep['p1sigma_values'] = p1sv
    data_hep['m1sigma_values'] = m1sv
    data_hep['m2sigma_values'] = m2sv, 
    with open(f'paperPlots/hepdata_{name}.pkl', 'wb') as f:
        pickle.dump(data_hep, f)


