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
doRatio = True

# In-line arguments
model = sys.argv[1]
limfiles = sys.argv[2]
ctau = sys.argv[3]
labels = sys.argv[4]
year = sys.argv[5]

if year=='2022':
    luminosity = 35
elif year=='2023':
    luminosity = 27
else:
    luminosity = 27 + 35

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
#
#
basedir = '/ceph/cms/store/user/fernance/Run3ScoutingOutput'
files = ["%s/%s"%(basedir,limfile) for limfile in limfiles.split(',')]
#
all_labels = labels.split(',')
#
all_massv = []
all_obsv  = []
all_expv  = []
all_m1sv  = []
all_p1sv  = []
all_m2sv  = []
all_p2sv  = []
#
for filename in files:
    #
    massl = []
    obsl  = []
    expl  = []
    m2sl  = []
    m1sl  = []
    p1sl  = []
    p2sl  = []
    mext  = []
    pext  = []
    #
    fin = open(filename,"r")
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
        if 'NormSmart' in filename:
            print('Using smart normalization for ' + filename)
            if model=="HTo2ZdTo2mu2x":
                scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_asymptotic_vsMass_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
                with open(scalingFile) as fin:
                    for ll in fin.readlines():
                        if ll.startswith("#"):
                            continue
                        lls = ll.split(",")
                        if (float(lls[1])== float(ls[1])) and (float(lls[2])== float(ls[2])):
                            e2m = float(lls[5])
                            NORMCONST = 0.01 * ( e2m / 0.2 )
                            print(" -> Using smart scaling of %.2f for em2 limit of %.3f  to be 0.2" % (NORMCONST, e2m))
                            xsec = xsec_base*NORMCONST
                            break
        else:
            xsec = xsec_base*NORMCONST
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

    fin.close()

    massv = np.array(massl,"d")
    obsv  = np.array(obsl ,"d")
    expv  = np.array(expl ,"d")
    m1sv  = np.array(m1sl ,"d")
    p1sv  = np.array(p1sl ,"d")
    m2sv  = np.array(m2sl ,"d")
    p2sv  = np.array(p2sl ,"d")

    all_massv.append(massv)
    all_obsv.append(obsv)  
    all_expv.append(expv)  
    all_m1sv.append(m1sv)  
    all_p1sv.append(p1sv)  
    all_m2sv.append(m2sv)  
    all_p2sv.append(p2sv)  
    
# Plot the limits
limitname = ['Observed', '+$2\sigma$', '+$1\sigma$', '-$2\sigma$', '-$1\sigma$', 'Expected']
limitvalue = [all_obsv, all_p2sv, all_p1sv, all_m2sv, all_m1sv, all_expv]
limitlabel = ['obs', 'p2s', 'p1s', 'm2s', 'm1s', 'exp']
for j in range(6):
    plt.style.use(hep.style.CMS)
    #
    if doRatio:
        fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05}, sharex=True, figsize=(11, 10))
    else:
        fig, ax = plt.subplots(figsize=(11, 8))
    #
    styles = ['-', '--']
    mstyles = ['x', 'o']
    colors = ['red', 'blue']
    for i in range(2):
        ax.plot(all_massv[i], limitvalue[j][i], marker=mstyles[i], linestyle=styles[i], color=colors[i], label=r'%s (%s)'%(limitname[j], all_labels[i]), linewidth=2, zorder=2)    #

    # Masking
    ax.axvspan(getLowerMask(0.41), getUpperMask(0.50), color='lightgray', alpha=1.0, zorder=2) # Ks
    ax.axvspan(getLowerMask(0.51), getUpperMask(0.59), color='lightgray', alpha=1.0, zorder=2) # Eta
    ax.axvspan(getLowerMask(0.73), getUpperMask(0.83), color='lightgray', alpha=1.0, zorder=2) # rho/w
    ax.axvspan(getLowerMask(0.96), getUpperMask(1.08), color='lightgray', alpha=1.0, zorder=2) # phi
    ax.axvspan(getLowerMask(2.91), getUpperMask(3.27), color='lightgray', alpha=1.0, zorder=2) # JPsi
    ax.axvspan(getLowerMask(2.89), getUpperMask(3.33), color='lightgray', alpha=1.0, zorder=2) # JPsi
    ax.axvspan(getLowerMask(3.47), getUpperMask(3.94), color='lightgray', alpha=1.0, zorder=2) # PSi2S
    ax.axvspan(getLowerMask(8.88), getUpperMask(10.85), color='lightgray', alpha=1.0, zorder=2) # Upsilon

    # Other details:
    if typeOfLimit=="BRH":
        ax.set_yscale('log')
        ax.set_ylabel(r'95% CL upper limit on Br($h \rightarrow Z_d Z_d$)')
        ax.set_ylim(2e-6, 1)
    elif typeOfLimit=="r":
        ax.set_yscale('linear')
        ax.set_ylabel(r"95% CL upper limit on r")
        ax.set_ylim(0, 2.5)

    ax.set_xscale('log')
    ax.set_xlabel('Mass [GeV]')
    ax.set_xlim(massv[0], massv[-1])
    ax.set_xlim(0.5, 50)
    if ctau=='100.00':
        ax.set_xlim(1.5, 50)
        ax.set_xticks([2, 5, 10, 20, 30, 50])
        ax.set_xticklabels(["2", "5", "10", "20", "30", "50"])
    if ctau=='1000.00':
        ax.set_xlim(2.0, 50)
        ax.set_xticks([2, 5, 10, 20, 30, 50])
        ax.set_xticklabels(["2", "5", "10", "20", "30", "50"])

    ax.set_axisbelow(False)
    ax.tick_params(zorder=10)
    #
    if year!='allEras':
        hep.cms.label(loc=0, data=True, llabel="Preliminary", lumi=luminosity, year=year, com=13.6, ax=ax)
    else:
        hep.cms.label(loc=0, data=True, llabel="Preliminary", lumi=luminosity, com=13.6, ax=ax)
    #
    if model=="HTo2ZdTo2mu2x":
        legend = ax.legend(loc='upper right', title=r"$H\rightarrow Z_DZ_D$ ($c\tau =$ %s mm)"%(ctau), fontsize=15, title_fontsize=16, frameon = True, ncol=2)
    legend.get_title().set_weight('bold')
    legend.set_zorder(10)
    legend._legend_box.align = "left"
    #
    #
    if doRatio:
        common = np.intersect1d(all_massv[0], all_massv[1])
        index_a = [np.where(all_massv[0] == val)[0][0] for val in common]
        index_b = [np.where(all_massv[1] == val)[0][0] for val in common]
        print(index_a)
        mass_ab = np.array([all_massv[0][x] for x in index_a])
        print(mass_ab)
        val_a = np.array([limitvalue[j][0][x] for x in index_a])
        val_b = np.array([limitvalue[j][1][x] for x in index_b])
        #print(len(index_a), len(index_b))
        ax_ratio.plot(mass_ab, val_a/val_b, marker=mstyles[i], linestyle=styles[i], color=colors[i], label=r'%s (%s)'%(limitname[j], all_labels[i]), linewidth=2, zorder=2)    #
        ax_ratio.set_xlabel('Mass [GeV]')
        ax_ratio.set_ylabel('Ratio')
        ax.set_xlabel('')
    #
    #
    if not os.path.exists('limitComparison_vsMass'):
        os.makedirs('limitComparison_vsMass')
    #
    fig.savefig("limitComparison_vsMass/limitsComparison_%s_ctau%s_%s_%s"%(model,ctau.replace('.','p'),typeOfLimit,limitlabel[j]), dpi=140)


