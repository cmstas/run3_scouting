import os,sys,math
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import ROOT
import matplotlib.colors as mcolors

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
NORMCONST = 0.1 # Needs to be consistent with what it was put on make_datacards.py e.g. if signal was scaled by NORMCONST xsec should be divided by it
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
year = sys.argv[3]

if year=='2022':
    luminosity = 35
elif year=='2023':
    luminosity = 27
else:
    luminosity = 27 + 35

massl = []
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

fin = open("%s/limits_%s_%s.txt"%(limdir,model,year),"r")
for l in fin.readlines():
    if l.startswith("#"):
        continue
    ls = l.split(",")
    if ls[0]!=model:
        continue
    # PROVISIONAL WHILE OTHER POINTS ARE RUNNING!
    if float(ls[1])< 4.999:
        continue
    #
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
    if "Scenario" not in model:
        massl.append(float(ls[1]))
        ctaul.append(float(ls[2]))
        obsl .append(scale*float(ls[3]))
        expl .append(scale*float(ls[4]))
        m2sl .append(scale*float(ls[5]))
        m1sl .append(scale*float(ls[6]))
        p1sl .append(scale*float(ls[7]))
        p2sl .append(scale*float(ls[8]))
    else:
        print('Dark QCD not supported for 2-dimensional plot, exiting...')
        sys.exit()
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

massv = np.array(massl,"d")
ctauv = np.array(ctaul,"d")
obsv  = np.array(obsl ,"d")
expv  = np.array(expl ,"d")
m1sv  = np.array(m1sl ,"d")
p1sv  = np.array(p1sl ,"d")
m2sv  = np.array(m2sl ,"d")
p2sv  = np.array(p2sl ,"d")

values_mass = np.unique(massv)
values_ctau = np.unique(ctauv)

nmass = len(values_mass)
nctau = len(values_ctau)

values_obs = np.full((nctau, nmass), np.nan)
values_exp = np.full((nctau, nmass), np.nan)
for m_ in range(0, nmass):
    for t_ in range(0, nctau):
        values_obs[t_, m_] = obsv[m_*nctau + t_]
        values_exp[t_, m_] = expv[m_*nctau + t_]

print(values_exp)

# Plot the limit
plt.style.use(hep.style.CMS)
#
fig, ax = plt.subplots(figsize=(12, 7))
#
norm = mcolors.LogNorm(vmin=1e-6, vmax=1)
#
if drawObserved:
    c = ax.contourf(values_mass, values_ctau, values_obs, levels=np.logspace(-6, 0, 7), norm=norm, cmap="viridis")
else:
    c = ax.contourf(values_mass, values_ctau, values_exp, levels=np.logspace(-6, 0, 7), norm=norm, cmap="viridis")
#
cbar = fig.colorbar(c, ax=ax, label=r'95% CL upper limit on Br($h \rightarrow Z_d Z_d$)')
#cbar.ax.set_yticklabels([r"$10^{-6}$", r"$10^{-5}$", r"$10^{-4}$", r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$", "1"])
#

# Other details
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel(r'Lifetime $c\tau$ [mm]')
ax.set_xlabel(r'Mass [GeV]')

ax.set_xticks([5., 7., 10., 20., 30., 40., 50.], minor=False)
ax.set_xticklabels(['5', '7', '10', '20', '30', '40', '50'])
ax.xaxis.set_major_formatter(plt.ScalarFormatter())
ax.xaxis.set_minor_locator(plt.NullLocator())

# Masking
#ax.axvspan(getLowerMask(0.41), getUpperMask(0.50), color='lightgray', alpha=1.0, zorder=10) # Ks
#ax.axvspan(getLowerMask(0.51), getUpperMask(0.59), color='lightgray', alpha=1.0, zorder=10) # Eta
#ax.axvspan(getLowerMask(0.73), getUpperMask(0.83), color='lightgray', alpha=1.0, zorder=10) # rho/w
#ax.axvspan(getLowerMask(0.96), getUpperMask(1.08), color='lightgray', alpha=1.0, zorder=10) # phi
#ax.axvspan(getLowerMask(2.91), getUpperMask(3.27), color='lightgray', alpha=1.0, zorder=10) # JPsi
#ax.axvspan(getLowerMask(2.89), getUpperMask(3.33), color='lightgray', alpha=1.0, zorder=10) # JPsi
#ax.axvspan(getLowerMask(3.47), getUpperMask(3.94), color='lightgray', alpha=1.0, zorder=10) # PSi2S
ax.axvspan(getLowerMask(8.88), getUpperMask(10.85), color='lightgray', alpha=1.0, zorder=1) # Upsilon

#
hep.cms.label(loc=0, data=True, llabel="Work in progress", lumi=luminosity, com=13.6)
#
#if model=="HTo2ZdTo2mu2x":
#    legend = ax.legend(loc='upper right', title=r"$H\rightarrow Z_DZ_D$ ($m_{Z_D} =$ %.1f GeV)"%(float(mass)), fontsize=15, title_fontsize=15, frameon = True)
#legend.get_title().set_ha('left') 
#legend.get_title().set_weight('bold')
#
if drawObserved:
    fig.savefig("%s/limits_%s_2D_%s_alt_obs"%(limdir,model,typeOfLimit), dpi=140)
