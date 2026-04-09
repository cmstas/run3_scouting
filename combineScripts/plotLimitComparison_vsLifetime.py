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
doSignalNormalization = True # Only valid if typeOfLimit=="r" -> Normalized the signal of the datacard to 1
xsec_base = 1.0 # in pb, used to normalize the MC
xsec_h = 59.8 # higgs cross section in pb at 13.6 GeV, used to normalize the MC
scaleToFullLumi = False
compare = True
doSmartScaling = True
doRatio = False

# In-line arguments
model = sys.argv[1]
limfiles = sys.argv[2]
mass = sys.argv[3]
labels = sys.argv[4]
year = sys.argv[5]
if len(sys.argv) > 6:
    print('CAUTION: This can only be used if both limits were obtained with the same datacards. Please abort if this is not the case.')
    datacards = sys.argv[6]
else:
    datacards = ''

if year=='2022':
    luminosity = 34.6
elif year=='2023':
    luminosity = 27.8
else:
    luminosity = 62.4

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
basedir = '/home/users/fernance//Run3-Analyses/SnT-Scouting/Code/Final/run3_scouting/'
files = ["%s/%s"%(basedir,limfile) for limfile in limfiles.split(',')]
#
all_labels = labels.split(',')
#
all_ctauv = []
all_obsv  = []
all_expv  = []
all_m1sv  = []
all_p1sv  = []
all_m2sv  = []
all_p2sv  = []
# Others:
all_nZB         = [] # Counts the number of Zero Background regions in the search
all_totalSignal = [] # Counts the total signal distributed in every SR considered in the datacard
#
for filename in files:
    #
    ctaul = []
    obsl  = []
    expl  = []
    m2sl  = []
    m1sl  = []
    p1sl  = []
    p2sl  = []
    mext  = []
    pext  = []
    nZB         = []
    totalSignal = []
    #
    fin = open(filename,"r")
    for l in fin.readlines():
        if l.startswith("#"):
            continue
        ls = l.split(",")
        if ls[0]!=model:
            continue
        if "Scenario" not in model:
            if float(ls[1])!=float(mass):
                continue
        else:
            if float(ls[1])!=float(mass.split(',')[0]):
                continue
            if float(ls[2])!=float(mass.split(',')[1]):
                continue
        scale = 1.0
        print(mass)
        # Smart scaling
        #if 'NormSmart' in filename:
        if True:
            print('Using smart normalization for ' + filename)
            if model=="HTo2ZdTo2mu2x":
                scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_HTo2ZdTo2mu2x_NormSmart_Apr-28-2025_vsCTau_asymptotic_allEras/limits_HTo2ZdTo2mu2x_allEras.txt'
                with open(scalingFile) as fin:
                    for ll in fin.readlines():
                        if ll.startswith("#"):
                            continue
                        lls = ll.split(",")
                        if (float(lls[1])== float(ls[1])) and (float(lls[2])== float(ls[2])):
                            e2m = float(lls[5])
                            NORMCONST = 0.01 * ( e2m / 0.6 )
                            print(" -> Using smart scaling of %.2f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                            xsec = xsec_base*NORMCONST
                            break
        else:
            xsec = xsec_base*NORMCONST
        # Branching ratio:
        BR = 1.0
        if model=="HTo2ZdTo2mu2x":
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
        if typeOfLimit=="xsec":
            scale = xsec
        if typeOfLimit=="BRH":
            scale = xsec/xsec_h
        elif typeOfLimit=="xsecBR":
            if model=="HTo2ZdTo2mu2x":
                scale = xsec*BR

        if "Scenario" not in model:
            ctaul.append(float(ls[2]))
            obsl .append(scale*float(ls[3]))
            expl .append(scale*float(ls[4]))
            m2sl .append(scale*float(ls[5]))
            m1sl .append(scale*float(ls[6]))
            p1sl .append(scale*float(ls[7]))
            p2sl .append(scale*float(ls[8]))
            ctau = float(ls[2])
        else:
            ctaul.append(float(ls[3]))
            obsl .append(scale*float(ls[4]))
            expl .append(scale*float(ls[5]))
            m2sl .append(scale*float(ls[6]))
            m1sl .append(scale*float(ls[7]))
            p1sl .append(scale*float(ls[8]))
            p2sl .append(scale*float(ls[9]))
            ctau = float(ls[3])

        ## Datacard things:
        nZB_value = 0
        totalSignal_value = 0.0
        if datacards!='':
            datacard = '%s/card_combined_%s_M%.3f_ctau%.2f_%s.root'%(datacards, model, float(mass), ctau, year)
            tfile = ROOT.TFile.Open(datacard)
            workspace = tfile.Get('w')
            for var_name in workspace.allVars():
                name = var_name.GetName()
                if "shapeBkg_background_" in name and name.endswith("_norm"):
                    var = workspace.var(name)
                    if var.getVal() < 0.99:
                        nZB_value += 1
            for funcs_name in workspace.allFunctions():
                name = funcs_name.GetName()
                if name.startswith("n_exp_") and name.endswith("proc_signal"):
                    fn = workspace.function(name)
                    totalSignal_value += fn.getVal()
        nZB.append(nZB_value)
        totalSignal.append(totalSignal_value)

        #print(mass, float(ls[2]), scale*float(ls[4]), totalSignal_value)

    fin.close()

    ctauv = np.array(ctaul,"d")
    obsv  = np.array(obsl ,"d")
    expv  = np.array(expl ,"d")
    m1sv  = np.array(m1sl ,"d")
    p1sv  = np.array(p1sl ,"d")
    m2sv  = np.array(m2sl ,"d")
    p2sv  = np.array(p2sl ,"d")
    nZBv         = np.array(nZB)
    totalSignalv = np.array(totalSignal)

    # To cm
    ctauv = ctauv * 0.1

    # Normalize signal:
    if typeOfLimit=="r" and doSignalNormalization:
        obsv = obsv*totalSignalv
        expv = expv*totalSignalv
        m1sv = m1sv*totalSignalv
        p1sv = p1sv*totalSignalv
        m2sv = m2sv*totalSignalv
        p2sv = p2sv*totalSignalv


    # Final sets of values to be appended
    all_ctauv.append(ctauv)
    all_obsv.append(obsv)  
    all_expv.append(expv)  
    all_m1sv.append(m1sv)  
    all_p1sv.append(p1sv)  
    all_m2sv.append(m2sv)  
    all_p2sv.append(p2sv)
    all_nZB.append(nZBv)
    all_totalSignal.append(nZBv)  
    

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
    styles = ['-', '--', ':']
    mstyles = ['x', 'o', 's']
    colors = ['red', 'blue', 'green']
    for i in range(len(files)):
        ax.plot(all_ctauv[i], limitvalue[j][i], marker=mstyles[i], linestyle=styles[i], color=colors[i], label=r'%s (%s)'%(limitname[j], all_labels[i]), linewidth=2, zorder=2)    #

    # Other details:
    if typeOfLimit=="BRH":
        ax.set_yscale('log')
        ax.set_ylabel(r'95% CL upper limit on Br($h \rightarrow Z_d Z_d$)')
        ax.set_ylim(2e-6, 1)
    elif typeOfLimit=="r":
        ax.set_yscale('linear')
        ax.set_ylabel(r"95% CL upper limit on r")
        ax.set_ylim(0, 5)

    ax.set_xscale('log')
    ax.set_xlabel(r'Lifetime $c\tau$ [cm]')
    ax.set_xlim(ctauv[0], ctauv[-1])
    if doRatio:
        ax_ratio.set_xscale('log')
        ax.set_xlabel('')
        ax_ratio.set_xlabel(r'Lifetime $c\tau$ [cm]')
        ax_ratio.set_xlim(ctauv[0], ctauv[-1])
        ax_ratio.set_ylabel('Ratio')

    ax.set_axisbelow(False)
    ax.tick_params(zorder=10)
    #
    if year!='allEras':
        hep.cms.label(loc=0, data=True, llabel="Preliminary", lumi=luminosity, year=year, com=13.6, ax=ax)
    else:
        hep.cms.label(loc=0, data=True, llabel="Preliminary", lumi=luminosity, com=13.6, ax=ax)
    #
    if model=="HTo2ZdTo2mu2x":
        legend = ax.legend(loc='upper right', title=r"$H\rightarrow Z_DZ_D$ ($m_{Z_D} =$ %.1f GeV, Br($Z_D \rightarrow \mu\mu$) = %.3f)"%(float(mass), float(BR)), fontsize=15, title_fontsize=15, frameon = True)
    elif model=="ScenarioA":
        legend = ax.legend(loc='upper right', title=r"Scenario A ($m_{\pi} =$ %.2f GeV, $m_{A} =$ %.2f GeV)"%(float(mass.split(',')[0]), float(mass.split(',')[1])), fontsize=15, title_fontsize=15, frameon = True)
    elif model=="ScenarioB1":
        legend = ax.legend(loc='upper right', title=r"Scenario B ($m_{\pi} =$ %.2f GeV, $m_{A} =$ %.2f GeV)"%(float(mass.split(',')[0]), float(mass.split(',')[1])), fontsize=15, title_fontsize=15, frameon = True)

    legend.get_title().set_weight('bold')
    legend.set_zorder(10)
    legend._legend_box.align = "left"
    #
    #
    if doRatio:
        common = np.intersect1d(all_ctauv[0], all_ctauv[1])
        index_a = [np.where(all_ctauv[0] == val)[0][0] for val in common]
        index_b = [np.where(all_ctauv[1] == val)[0][0] for val in common]
        print(index_a)
        ctau_ab = np.array([all_ctauv[0][x] for x in index_a])
        nZB_ab = np.array([all_nZB[0][x] for x in index_a])
        print(ctau_ab)
        val_a = np.array([limitvalue[j][0][x] for x in index_a])
        val_b = np.array([limitvalue[j][1][x] for x in index_b])
        #print(len(index_a), len(index_b))
        ax_ratio.plot(ctau_ab, val_a/val_b, marker=mstyles[i], linestyle=styles[i], color=colors[i], label=r'%s (%s)'%(limitname[j], all_labels[i]), linewidth=2, zorder=2)    #
    #
    #
    if not os.path.exists('limitComparison_vsCTau'):
        os.makedirs('limitComparison_vsCTau')
    #
    fig.savefig("limitComparison_vsCTau/limitsComparison_%s_mass%s_%s_%s"%(model,mass.replace('.', 'p'),typeOfLimit,limitlabel[j]), dpi=140)

    # Extras
    if datacards!='':
        fig, ax = plt.subplots(figsize=(11, 8))
        ax.scatter(nZB_ab, val_a/val_b, s=20, alpha=0.8)
        ax.set_xlabel("Number of zero-background regions")
        ax.set_ylabel("Ratio between Toys/Asymptotic")
        fig.savefig("limitComparison_vsCTau/limitsScatter_%s_mass%s_%s_%s"%(model,mass.replace('.', 'p'),typeOfLimit,limitlabel[j]), dpi=140)

