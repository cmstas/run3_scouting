import os,sys,math
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import ROOT

def getLowerMask(lowerBound):
    rel_sigma = 0.018
    return lowerBound / (1 + 5*rel_sigma)

def getUpperMask(upperBound):
    rel_sigma = 0.018
    return upperBound / (1 - 5*rel_sigma)


ROOT.gROOT.SetBatch(1)
drawObserved = True
drawPoints = True
maskSMResonances = True
NORMCONST = 1.0 # Needs to be consistent with what it was put on make_datacards.py e.g. if signal was scaled by NORMCONST xsec should be divided by it
typeOfLimit = "BRH" # "r", "xsec", "xsecBR" "BRH" 
xsec_base = 1.0 # in pb, used to normalize the MC
xsec_h = 59.8 # higgs cross section in pb at 13.6 GeV, used to normalize the MC
scaleToFullLumi = False
compare = True
luminosity = 35
doSmartScaling = True
hepdata_input = True

model = sys.argv[1]
limdir = sys.argv[2]
mass = sys.argv[3]
year = sys.argv[4]
if len(sys.argv) > 5:
    limtype = sys.argv[5]
else:
    limtype = 'asymptotic'

print("> Limits for model %s"%model)
#print("> Selected mass %.3f"%float(mass))
print("> Using limits computed with %s"%limtype)

if 'Scenario' in model:
    #xsec_h = 52.23
    xsec_h = 59.8 # For the PAS and before CWR it was 52.23 as EXO-24-008 are got with that. Now we re-scale that limits by 52.23/59.8 for consistency
elif 'HTo2ZdTo2mu2x' in model:
    xsec_h = 59.8
else:
    xsec_h = 1.2890e+08


if year=='2022':
    luminosity = 34.6
elif year=='2023':
    luminosity = 27.8
else:
    luminosity = 62.4

ctaul = []
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
    if "Scenario" in model:
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
    if "Scenario" not in model:
        if float(ls[1])!=float(mass):
            continue
    else:
        if float(ls[1])!=float(mass.split(',')[0]):
            continue
        if float(ls[2])!=float(mass.split(',')[1]):
            continue
    scale = 1.0
    # Smart scaling:
    if doSmartScaling:
        if model=="HTo2ZdTo2mu2x":
            scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_HTo2ZdTo2mu2x_NormSmart_Apr-28-2025_vsCTau_asymptotic_allEras/limits_HTo2ZdTo2mu2x_asymptotic_allEras.txt'
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
        if "Scenario" in model:
            if model=="ScenarioA":
                #scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_ScenarioA_Norm1p0-0p6_Jun-10-2025_vsCTau_asymptotic_allEras/limits_ScenarioA_asymptotic_allEras.txt'
                scalingFile = 'combineScripts/SmartLimitNorm/limits_ScenarioA_asymptotic_allEras_vsCTau.txt'
            elif model=="ScenarioB1":
                #scalingFile = '/ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_ScenarioB1_Norm1p0-0p6_Jun-10-2025_vsCTau_asymptotic_allEras/limits_ScenarioB1_asymptotic_allEras.txt'
                #scalingFile = 'results_ScenarioB1_asymptotic/limits_ScenarioB1_asymptotic_allEras.txt'
                scalingFile = 'combineScripts/SmartLimitNorm/limits_ScenarioB1_asymptotic_allEras_vsCTau.txt'
            with open(scalingFile) as fin:
                for ll in fin.readlines():
                    if ll.startswith("#"):
                        continue
                    lls = ll.split(",")
                    print(lls)
                    if (float(lls[1])== float(ls[1])) and (float(lls[2])== float(ls[2])) and (float(lls[3])== float(ls[3])):
                        e2m = float(lls[6])
                        NORMCONST = 10.0 * ( e2m / 0.6 ) # This one was used with 1.0
                        print(" -> Using smart scaling of %.5f for em2 limit of %.3f  to be 0.6" % (NORMCONST, e2m))
                        xsec = xsec_base*NORMCONST
                        break
        if model=="BToPhi":
            scalingFile = 'results_BToPhi_asymptotic/limits_BToPhi_asymptotic_allEras.txt'
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
    # Branching ratio:
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
    if typeOfLimit=="xsec":
        scale = xsec
    if typeOfLimit=="BRH":
        if 'BToPhi' in model:
            eff_m = 0.2627 # hardcoded -> to change
            scale = xsec/(2.0 * xsec_h * eff_m)
        else:
            scale = xsec/xsec_h
    elif typeOfLimit=="xsecBR":
        if model=="HTo2ZdTo2mu2x":
            scale = xsec*BR
        print(float(ls[1]), float(ls[4]), BR)
    #if scaleToFullLumi:
    #    scale = scale / math.sqrt(10.0)
    #if model=="HTo2ZdTo2mu2x" and float(ctau) > 10 and float(ls[1]) < 1.5:
    #    continue
    if "Scenario" not in model:
        ctaul.append(float(ls[2]))
        obsl .append(scale*float(ls[3]))
        expl .append(scale*float(ls[4]))
        m2sl .append(scale*float(ls[5]))
        m1sl .append(scale*float(ls[6]))
        p1sl .append(scale*float(ls[7]))
        p2sl .append(scale*float(ls[8]))
    else:
        ctaul.append(float(ls[3]))
        obsl .append(scale*float(ls[4]))
        expl .append(scale*float(ls[5]))
        m2sl .append(scale*float(ls[6]))
        m1sl .append(scale*float(ls[7]))
        p1sl .append(scale*float(ls[8]))
        p2sl .append(scale*float(ls[9]))

    if scaleToFullLumi:
        mext .append(scale*float(ls[4])/10.0)
        pext .append(scale*float(ls[4])/math.sqrt(10.0))

fin.close()

print(ctaul)
ctauv = np.array(ctaul,"d")
obsv  = np.array(obsl ,"d")
expv  = np.array(expl ,"d")
m1sv  = np.array(m1sl ,"d")
p1sv  = np.array(p1sl ,"d")
m2sv  = np.array(m2sl ,"d")
p2sv  = np.array(p2sl ,"d")

# To cm
ctauv = ctauv * 0.1

# Comparisons
cfile = None
cfile_run2 = None
if compare:
    print("> Request to open files to compare")
    try:
        if model=="HTo2ZdTo2mu2x":
            if typeOfLimit=="BRH":
                if float(mass)==2.0:
                    cfile_run2 = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Additional_Figure_14-2.root")
                    cgobs_run2 = cfile_run2.Get("Additional Figure 14/Graph1D_y1")
                if float(mass)==5.0:
                    cfile_run2 = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Additional_Figure_14-2.root")
                    cgobs_run2 = cfile_run2.Get("Additional Figure 14/Graph1D_y2")
                if float(mass)==12.0:
                    cfile_run2 = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Additional_Figure_14-2.root")
                    cgobs_run2 = cfile_run2.Get("Additional Figure 14/Graph1D_y3")
                if float(mass)==20.0:
                    cfile = ROOT.TFile("data/run-3/HEPData-ins2760892-v2-Figure_15_top_right.root")
                    cgobs = cfile.Get("Figure 15 top right/Graph1D_y1")
                    cfile_run2 = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Additional_Figure_14-2.root")
                    cgobs_run2 = cfile_run2.Get("Additional Figure 14/Graph1D_y4")
                if float(mass)==30.0:
                    cfile = ROOT.TFile("data/run-3/HEPData-ins2760892-v2-Figure_15_center_left.root")
                    cgobs = cfile.Get("Figure 15 center left/Graph1D_y1")
                if float(mass)==40.0:
                    cfile = ROOT.TFile("data/run-3/HEPData-ins2760892-v2-Figure_15_center_right.root")
                    cgobs = cfile.Get("Figure 15 center right/Graph1D_y1")
                    cfile_run2 = ROOT.TFile("data/run-2/scouting/HEPData-ins1997201-v2-Additional_Figure_14-2.root")
                    cgobs_run2 = cfile_run2.Get("Additional Figure 14/Graph1D_y5")
                if float(mass)==50.0:
                    cfile = ROOT.TFile("data/run-3/HEPData-ins2760892-v2-Figure_15_bottom_left.root")
                    cgobs = cfile.Get("Figure 15 bottom left/Graph1D_y1")
    except NameError:
        print("> Files not available")
        pass

# Plot the limit
plt.style.use(hep.style.CMS)
#
fig, ax = plt.subplots(figsize=(11, 8))
#
if drawObserved:
    if model=="HTo2ZdTo2mu2x" or model=="BToPhi" or ("Scenario" in model):
        ax.plot(ctauv, obsv, 'k-', label='Observed', linewidth=2)
    else:
        for i in range(len(m2sv)):
            if i==0:
                ax.plot(np.array([i+0.25, i+0.75]), np.array([obsv[i], obsv[i]]), 'k-', label='Observed', linewidth=2)
            else:
                ax.plot(np.array([i+0.25, i+0.75]), np.array([obsv[i], obsv[i]]), 'k-', linewidth=2)
            ax.plot(i+0.5, obsv[i], 'ko', linewidth=2)

#
if model=="HTo2ZdTo2mu2x" or model=="BToPhi" or ("Scenario" in model):
    ax.plot(ctauv, expv, 'r--', label='Expected', linewidth=2)
else:
    for i in range(len(m2sv)):
        if i==0:
            ax.plot(np.array([i+0.25, i+0.75]), np.array([expv[i], expv[i]]), 'r--', label='Expected', linewidth=2, zorder=10)
        else:
            ax.plot(np.array([i+0.25, i+0.75]), np.array([expv[i], expv[i]]), 'r--', linewidth=2, zorder=10)
#
if model=="HTo2ZdTo2mu2x" or model=="BToPhi" or ("Scenario" in model):
    ax.fill_between(ctauv, m2sv, p2sv, color='#FFDF7Fff', label=r'95% CL expected')
    ax.fill_between(ctauv, m1sv, p1sv, color='#85D1FBff', label=r'68% CL expected')
elif "Scenario" in model:
    # This was left here for the PAS:
    for i in range(len(m2sv)):
        if i==0:
            ax.fill_between(np.array([i+0.25, i+0.75]), np.array(m2sv[i], m2sv[i]), np.array(p2sv[i], p2sv[i]), color='#FFDF7Fff', label=r'$\pm 2\sigma$ expected')
            ax.fill_between(np.array([i+0.25, i+0.75]), np.array(m1sv[i], m1sv[i]), np.array(p1sv[i], p1sv[i]), color='#85D1FBff', label=r'$\pm 1\sigma$ expected')
        else:
            ax.fill_between(np.array([i+0.25, i+0.75]), np.array(m2sv[i], m2sv[i]), np.array(p2sv[i], p2sv[i]), color='#FFDF7Fff')
            ax.fill_between(np.array([i+0.25, i+0.75]), np.array(m1sv[i], m1sv[i]), np.array(p1sv[i], p1sv[i]), color='#85D1FBff')

#

if compare:
    if model=="HTo2ZdTo2mu2x":
        if cfile is not None:
            m_cgobs = np.array(cgobs.GetX())
            l_cgobs = np.array(cgobs.GetY())
            #ax.plot(m_cgobs, l_cgobs, linestyle='solid', color='magenta', label=r'Displaced dimuon with standard streams [JHEP 05 (2024) 047]', linewidth=2)
            ax.plot(m_cgobs, l_cgobs, linestyle='solid', color='magenta', label=r'JHEP 05 (2024) 047', linewidth=2)
        if cfile_run2 is not None:
            m_cgobs_run2 = np.array(cgobs_run2.GetX()) * 0.1 # To convert to cm
            l_cgobs_run2 = np.array(cgobs_run2.GetY())
            ax.plot(m_cgobs_run2, l_cgobs_run2, linestyle='solid', color='b', label=r'JHEP 04 (2022) 062', linewidth=2)
    elif model=="ScenarioA":
        exp_dqcd=None
        obs_dqcd=None
        ctau_dqcd = np.array([0.1, 0.25, 0.6, 1.0, 2.5, 6.0, 10.0, 25.0, 60.0, 100.0])*0.1
        if mass=="2.000,0.670":
            #exp_dqcd = np.array([566e-4, 38.66e-4, 70.33e-4, 506e-4])
            #obs_dqcd = np.array([564e-4, 38.47e-4, 50.19e-4, 338e-4])
            obs_dqcd = np.array([564.5, 116.89795831246300, 50.586655808447500, 38.47266704828810, 25.57347954821940, 31.961366575366400, 50.19046205717400, 133.65876994018500, 233.92782721256100, 338.35810835161000]) * 1e-4
            ctau_dqcd = np.array([0.1, 0.25, 0.6, 1.0, 2.5, 6.0, 10.0, 25.0, 100.0])*0.1
            obs_dqcd = [0.058047, 0.011649, 0.0050581, 0.0037699, 0.0025677, 0.003268, 0.0049698, 0.01291, 0.033911]
        if mass=="4.000,1.330":
            #exp_dqcd = np.array([120e-4, 8.32e-4, 6.93e-4, 52.65e-4])
            #obs_dqcd = np.array([112e-4, 8.24e-4, 5.58e-4, 42.46e-4])
            obs_dqcd = np.array([111.53804446649800, 38.141209412208400, 13.035149334448500, 8.243573208349200, 5.594615256780320, 4.577020182317160, 5.580153169933980, 10.015004439423300, 22.59313120955330, 42.46062579372980]) * 1e-4
            obs_dqcd = [0.011685, 0.0038461, 0.0013191, 0.00081411, 0.00054855, 0.00047414, 0.00056475, 0.0010337, 0.0022536, 0.0039586]
        if mass=="5.000,1.670":
            obs_dqcd = [0.0093685, 0.0036334, 0.0014107, 0.00098734, 0.00060506, 0.00078022, 0.00081346, 0.0015789, 0.0026745, 0.0053302]
        if mass=="6.000,2.000":
            obs_dqcd = [0.011919, 0.0040424, 0.0021333, 0.0011379, 0.00087753, 0.00064855, 0.00067843, 0.0010405, 0.0019276, 0.0029365]
        if mass=="7.500,2.500":
            obs_dqcd = [0.0089302, 0.003602, 0.0013767, 0.0009823, 0.00059094, 0.0003628, 0.00033989, 0.00053159, 0.00083619, 0.0014149]
        if obs_dqcd is not None:
            # This was for PAS:
            #for i in range(len(exp_dqcd)):
            #    if i==0:
            #        #ax.plot(np.array([i+0.25, i+0.75]), np.array([exp_dqcd[i], exp_dqcd[i]]), linestyle='--', color='b', label=r'Dark shower search [CMS-EXO-24-008] - expected', linewidth=2)
            #        ax.plot(np.array([i+0.25, i+0.75]), np.array([obs_dqcd[i], obs_dqcd[i]]), linestyle='-', color='b', label=r'Dark showers search [CMS-EXO-24-008]', linewidth=2)
            #    else:
            #        #ax.plot(np.array([i+0.25, i+0.75]), np.array([exp_dqcd[i], exp_dqcd[i]]), linestyle='--', color='b', linewidth=2)
            #        ax.plot(np.array([i+0.25, i+0.75]), np.array([obs_dqcd[i], obs_dqcd[i]]), linestyle='-', color='b', linewidth=2)
            #
            obs_dqcd = np.array(obs_dqcd) * 52.23/59.8 # Re-scale to match the cross-section
            ax.plot(ctau_dqcd, obs_dqcd, linestyle='-', color='b', linewidth=2, label='arXiv:2511.11888')
    elif model=="ScenarioB1":
        exp_dqcd=None
        obs_dqcd=None
        ctau_dqcd = np.array([0.1, 0.25, 0.6, 1.0, 2.5, 6.0, 10.0, 25.0, 60.0, 100.0])*0.1
        if mass=="2.000,0.670":
            #exp_dqcd = np.array([762e-4, 72.59e-4, 56.23e-4, 717e-4])
            #obs_dqcd = np.array([749e-4, 72.19e-4, 63.24e-4, 763e-4])
            exp_dqcd = np.array([762.724, 467.867, 121.50161659410600, 72.59705301899100, 51.66215543482190, 48.16585092493310, 56.234080227543300, 132.69614543725500, 281.4730373555630, 716.714]) * 1e-4
            obs_dqcd = np.array([749.419, 505.676, 117.25319332590200, 72.19470819943820, 49.480744223474700, 49.21072925404200, 63.24189862441060, 147.32799499589700, 295.0564841244640, 763.175]) * 1e-4
            obs_dqcd = np.array([0.074606, 0.052666, 0.012116, 0.0072142, 0.0046866, 0.0049116, 0.0062698, 0.014571, 0.029895, 0.075571])
        if mass=="4.000,1.330":
            #exp_dqcd = np.array([93e-4, 11.68e-4, 7.43e-4, 48.60e-4])
            #obs_dqcd = np.array([95.77e-4, 11.30e-4, 6.89e-4, 43.30e-4])
            exp_dqcd = np.array([93.16597808816320, 38.47310911611470, 16.032014312139900, 11.68053923948190, 8.501222146292210, 6.714959721403650, 7.426700829842280, 10.863922761829100, 25.865990711897500, 48.6014714996214]) * 1e-4
            obs_dqcd = np.array([95.77290970973740, 37.230325323389600, 15.994718620887000, 11.302165074674500, 7.812965891691010, 6.5747086243820400, 6.891911891201180, 10.17497250203900, 25.48556666587920, 43.30397859259640]) * 1e-4
            obs_dqcd = np.array([0.0094597, 0.0036753, 0.001616, 0.0010707, 0.00081821, 0.00063392, 0.00063446, 0.00099158, 0.0024976, 0.0044111])
        if mass=="5.000,1.670":
            obs_dqcd = np.array([0.023442, 0.0075397, 0.0036154, 0.0023318, 0.0010083, 0.00070601, 0.00080706, 0.001076, 0.0028209, 0.0052071])
        if mass=="6.000,2.000":
            obs_dqcd = np.array([0.010659, 0.0043772, 0.0024167, 0.0017237, 0.00093193, 0.000634, 0.00052568, 0.00078684, 0.0014133, 0.0022981])
        if mass=="7.500,2.500":
            obs_dqcd = np.array([0.017105, 0.0041106, 0.0031078, 0.00176, 0.00079958, 0.00055641, 0.00039961, 0.0004793, 0.00065893, 0.0010751])
        if obs_dqcd is not None:
            #for i in range(len(exp_dqcd)):
            #    if i==0:
            #        #ax.plot(np.array([i+0.25, i+0.75]), np.array([exp_dqcd[i], exp_dqcd[i]]), linestyle='--', color='b', label=r'Dark shower search [CMS-EXO-24-008] - expected', linewidth=2)
            #        ax.plot(np.array([i+0.25, i+0.75]), np.array([obs_dqcd[i], obs_dqcd[i]]), linestyle='-', color='b', label=r'Dark showers search [CMS-EXO-24-008]', linewidth=2)
            #    else:
            #        #ax.plot(np.array([i+0.25, i+0.75]), np.array([exp_dqcd[i], exp_dqcd[i]]), linestyle='--', color='b', linewidth=2)
            #        ax.plot(np.array([i+0.25, i+0.75]), np.array([obs_dqcd[i], obs_dqcd[i]]), linestyle='-', color='b', linewidth=2)
            obs_dqcd = np.array(obs_dqcd) * 52.23/59.8 # Re-scale to match the cross-section
            ax.plot(ctau_dqcd, obs_dqcd, linestyle='-', color='b', linewidth=2, label='arXiv:2511.11888')

# Other details
#if "Scenario" not in model:
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'$c\tau_{0}$ [cm]', fontsize=30)
if model=="HTo2ZdTo2mu2x":
    ax.set_ylabel(r'95% CL upper limit on  $\mathcal{B}$($H \rightarrow Z_D Z_D$)')
    ax.set_xlim(ctauv[0], ctauv[-1])
elif "Scenario" in model:
    ax.set_ylabel(r'95% CL upper limit on $\mathcal{B}$($H \rightarrow \Psi\bar{\Psi}$)', fontsize=30)
    ax.set_xlim(ctauv[0], ctauv[-1])
    #ax.set_xlim(0.15, len(ctauv) - 0.15)
    #xticks = np.arange(len(ctauv)) + 0.5
    #xticks_labels = [r"$10^{%i}$"%(int(math.log10(x))) for x in ctauv]
    #ax.set_xticks(xticks)
    #ax.set_xticklabels(xticks_labels)
elif "BToPhi" in model:
    ax.set_ylabel(r'95% CL limit on $\mathcal{B}$($B \rightarrow \phi X$)x $\mathcal{B} ($\phi \rightarrow \mu\mu$)')
    ax.set_xlim(ctauv[0], ctauv[-1])

if 'Scenario' in model:    
    ax.set_ylim(0.5*min(obs_dqcd), 90.0*max(p2sv))
#ax.set_ylim(1e-6, 1e-2)
#
if year!='allEras':
    hep.cms.label(loc=0, data=True, llabel="", lumi=luminosity, year=year, com=13.6)
else:
    hep.cms.label(loc=0, data=True, llabel="", lumi=luminosity, com=13.6)
#
if model=="HTo2ZdTo2mu2x":
    legend = ax.legend(loc='upper right', title=r"$H\rightarrow Z_DZ_D$ ($m_{Z_D} =$ %.0f GeV, Br($Z_D \rightarrow \mu\mu$) = %.3f)"%(float(mass), float(BR)), fontsize=20, title_fontsize=22, frameon = False)
elif model=="ScenarioA":
    legend = ax.legend(loc='upper left', title=r"Scenario A ($m_{\pi} =$ %g GeV, $m_{A} =$ %g GeV)" % (float(mass.split(',')[0]), float(mass.split(',')[1])), fontsize=20, title_fontsize=22, frameon = False)
    if obs_dqcd is not None and False: # deactivated
        ax.axvline(10., color='gray', ls=':', alpha=0.9)
elif model=="ScenarioB1":
    legend = ax.legend(loc='upper left', title=r"Scenario B1 ($m_{\pi} =$ %g GeV, $m_{A} =$ %g GeV)"%(float(mass.split(',')[0]), float(mass.split(',')[1])), fontsize=20, title_fontsize=22, frameon = False)
    if obs_dqcd is not None and False: # deactivated
        ax.axvline(10., color='gray', ls=':', alpha=0.9)
elif model=="BToPhi":
    legend = ax.legend(loc='upper right', title=r"$B\rightarrow \phi X$ ($m_{\phi} =$ %.0f GeV)"%(float(mass)), fontsize=22, title_fontsize=22, frameon = False)
#legend.get_title().set_ha('left') 
legend.get_title().set_weight('bold')
legend._legend_box.align = "left"
#
if "Scenario" not in model:
    if drawObserved:
        fig.savefig("%s/limits_%s_mass%s_%s_%s_obs"%(limdir,model,("%.1f"%float(mass)).replace('.','p'),typeOfLimit, limtype), dpi=140)
        fig.savefig("%s/limits_%s_mass%s_%s_%s_obs.pdf"%(limdir,model,("%.1f"%float(mass)).replace('.','p'),typeOfLimit, limtype), dpi=140)
    else:
        fig.savefig("%s/limits_%s_mass%s_%s_%s"%(limdir,model,("%.1f"%float(mass)).replace('.','p'),typeOfLimit, limtype), dpi=140)
        fig.savefig("%s/limits_%s_mass%s_%s_%s.pdf"%(limdir,model,("%.1f"%float(mass)).replace('.','p'),typeOfLimit, limtype), dpi=140)
else:
    if drawObserved:
        fig.savefig("%s/limits_%s_mass%s_%s_%s_%s_obs"%(limdir,model,mass.split(',')[0].replace('.','p'),mass.split(',')[1].replace('.','p'),typeOfLimit, limtype), dpi=140)
        fig.savefig("%s/limits_%s_mass%s_%s_%s_%s_obs.pdf"%(limdir,model,mass.split(',')[0].replace('.','p'),mass.split(',')[1].replace('.','p'),typeOfLimit, limtype), dpi=140)
    else:
        fig.savefig("%s/limits_%s_mass%s_%s_%s_%s"%(limdir,model,mass.split(',')[0].replace('.','p'),mass.split(',')[1].replace('.','p'),typeOfLimit, limtype), dpi=140)
        fig.savefig("%s/limits_%s_mass%s_%s_%s_%s.pdf"%(limdir,model,mass.split(',')[0].replace('.','p'),mass.split(',')[1].replace('.','p'),typeOfLimit, limtype), dpi=140)

import pickle
if hepdata_input:
    if model=="HTo2ZdTo2mu2x":
        if mass=="2.000":
            name = "Figure_012-a"
        if mass=="5.000":
            name = "Figure_012-b"
        if mass=="12.000":
            name = "Figure_012-c"
        if mass=="20.000":
            name = "Figure_012-d"
    if model=="ScenarioA":
        if mass=="2.000,0.670":
            name = "Figure_013-a"
        elif mass=="5.000,1.670":
            name = "Figure_013-b"
        elif mass=="7.500,2.500":
            name = "Figure_013-c"
    if model=="ScenarioB1":
        if mass=="2.000,0.670":
            name = "Figure_014-a"
        elif mass=="5.000,1.670":
            name = "Figure_014-b"
        elif mass=="7.500,2.500":
            name = "Figure_014-c"
    fig.savefig(f"paperPlots/{name}.png", dpi=140)
    fig.savefig(f"paperPlots/{name}.pdf", dpi=140)
    data_hep = {}
    data_hep['ctau_values'] = ctauv
    data_hep['expected_values'] = expv
    data_hep['observed_values'] = obsv
    data_hep['p2sigma_values'] = p2sv
    data_hep['p1sigma_values'] = p1sv
    data_hep['m1sigma_values'] = m1sv
    data_hep['m2sigma_values'] = m2sv, 
    with open(f'paperPlots/hepdata_{name}.pkl', 'wb') as f:
        pickle.dump(data_hep, f)


