import os,sys
import ROOT
import json
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
from matplotlib.patches import Patch

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

useSignalMC = False

if len(sys.argv)<3:
    print("Please, specify model and limit directory.")
    exit(1)

model = sys.argv[1]
indir = sys.argv[2]
year = sys.argv[3]
fitDir = sys.argv[4]
outdir = 'GOF_%s'%(year) 
if not os.path.exists(outdir):
    os.makedirs(outdir)

#fitDir = 'fitResults_2022'

# We remove the 2
#masses =  [0.5, 0.7, 1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]
masses =  [1.5, 2.0, 2.5, 5.0, 6.0, 7.0, 8.0, 14.0, 16.0, 20.0, 22.0, 24.0, 30.0, 34.0, 40.0, 44.0, 50.0]

# Search regions - channels
dNames = []
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p0to0p2_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy0p2to1p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso0_pthigh")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_ptlow")
dNames.append("d_Dimuon_lxy1p0to2p4_iso1_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso0_pthigh")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_ptlow")
dNames.append("d_Dimuon_lxy2p4to3p1_iso1_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy3p1to7p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy7p0to11p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy11p0to16p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso0_pthigh")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_ptlow")
dNames.append("d_Dimuon_lxy16p0to70p0_iso1_pthigh")
dNames.append("d_Dimuon_lxy0p0to0p2_non-pointing")
dNames.append("d_Dimuon_lxy0p2to1p0_non-pointing")
dNames.append("d_Dimuon_lxy1p0to2p4_non-pointing")
dNames.append("d_Dimuon_lxy2p4to3p1_non-pointing")
dNames.append("d_Dimuon_lxy3p1to7p0_non-pointing")
dNames.append("d_Dimuon_lxy7p0to11p0_non-pointing")
dNames.append("d_Dimuon_lxy11p0to16p0_non-pointing")
dNames.append("d_Dimuon_lxy16p0to70p0_non-pointing")


### Goodness of fit (Background-only)
channel_dict = {}
channel_dict["3"] = [0,1]
channel_dict["4"] = [0,2]
channel_dict["5"] = [0,3]
channel_dict["6"] = [0,4]

channel_dict["7"] = [1,1]
channel_dict["8"] = [1,2]
channel_dict["9"] = [1,3]
channel_dict["10"] = [1,4]

channel_dict["11"] = [2,1]
channel_dict["12"] = [2,2]
channel_dict["13"] = [2,3]
channel_dict["14"] = [2,4]

channel_dict["15"] = [3,1]
channel_dict["16"] = [3,2]
channel_dict["17"] = [3,3]
channel_dict["18"] = [3,4]

channel_dict["19"] = [4,1]
channel_dict["20"] = [4,2]
channel_dict["21"] = [4,3]
channel_dict["22"] = [4,4]

channel_dict["23"] = [5,1]
channel_dict["24"] = [5,2]
channel_dict["25"] = [5,3]
channel_dict["26"] = [5,4]

channel_dict["27"] = [6,1]
channel_dict["28"] = [6,2]
channel_dict["29"] = [6,3]
channel_dict["30"] = [6,4]

channel_dict["31"] = [7,1]
channel_dict["32"] = [7,2]
channel_dict["33"] = [7,3]
channel_dict["34"] = [7,4]


channel_dict["35"] = [0,5]
channel_dict["36"] = [1,5]
channel_dict["37"] = [2,5]
channel_dict["38"] = [3,5]
channel_dict["39"] = [4,5]
channel_dict["40"] = [5,5]
channel_dict["41"] = [6,5]
channel_dict["42"] = [7,5]


cat = [r'non-isolated, $p_{T}^{\mu\mu} < 25$ GeV', r'non-isolated, $p_{T}^{\mu\mu} > 25$ GeV', r'isolated, $p_{T}^{\mu\mu} < 25$ GeV', r'isolated, $p_{T}^{\mu\mu} > 25$ GeV', 'Non-pointing']
lxycat = [r'$l_{xy}\in[0.0, 0.2]$ cm, ', r'$l_{xy}\in[0.2, 1.0]$ cm, ', r'$l_{xy}\in[1.0, 2.4]$ cm, ', r'$l_{xy}\in[2.4, 3.1]$ cm, ', r'$l_{xy}\in[3.1, 7]$ cm, ', r'$l_{xy}\in[7, 11]$ cm, ', r'$l_{xy}\in[11, 16]$ cm, ', r'$l_{xy}\in[16, 7.0]$ cm, ']

fig, axes = plt.subplots(8, 5, figsize=(14, 14), sharex=True, sharey=True)

p_values_zero = []
p_values_low = []
p_values_med = []
p_values_high = []

for d in dNames:
    ch=-1
    if d=="d_FourMu_sep":
        ch=1
    elif d=="d_FourMu_osv":
        ch=2
    elif d=="d_Dimuon_lxy0p0to0p2_iso0_ptlow":
        ch=3
    elif d=="d_Dimuon_lxy0p0to0p2_iso0_pthigh":
        ch=4
    elif d=="d_Dimuon_lxy0p0to0p2_iso1_ptlow":
        ch=5
    elif d=="d_Dimuon_lxy0p0to0p2_iso1_pthigh":
        ch=6
    elif d=="d_Dimuon_lxy0p2to1p0_iso0_ptlow":
        ch=7
    elif d=="d_Dimuon_lxy0p2to1p0_iso0_pthigh":
        ch=8
    elif d=="d_Dimuon_lxy0p2to1p0_iso1_ptlow":
        ch=9
    elif d=="d_Dimuon_lxy0p2to1p0_iso1_pthigh":
        ch=10
    elif d=="d_Dimuon_lxy1p0to2p4_iso0_ptlow":
        ch=11
    elif d=="d_Dimuon_lxy1p0to2p4_iso0_pthigh":
        ch=12
    elif d=="d_Dimuon_lxy1p0to2p4_iso1_ptlow":
        ch=13
    elif d=="d_Dimuon_lxy1p0to2p4_iso1_pthigh":
        ch=14
    elif d=="d_Dimuon_lxy2p4to3p1_iso0_ptlow":
        ch=15
    elif d=="d_Dimuon_lxy2p4to3p1_iso0_pthigh":
        ch=16
    elif d=="d_Dimuon_lxy2p4to3p1_iso1_ptlow":
        ch=17
    elif d=="d_Dimuon_lxy2p4to3p1_iso1_pthigh":
        ch=18
    elif d=="d_Dimuon_lxy3p1to7p0_iso0_ptlow":
        ch=19
    elif d=="d_Dimuon_lxy3p1to7p0_iso0_pthigh":
        ch=20
    elif d=="d_Dimuon_lxy3p1to7p0_iso1_ptlow":
        ch=21
    elif d=="d_Dimuon_lxy3p1to7p0_iso1_pthigh":
        ch=22
    elif d=="d_Dimuon_lxy7p0to11p0_iso0_ptlow":
        ch=23
    elif d=="d_Dimuon_lxy7p0to11p0_iso0_pthigh":
        ch=24
    elif d=="d_Dimuon_lxy7p0to11p0_iso1_ptlow":
        ch=25
    elif d=="d_Dimuon_lxy7p0to11p0_iso1_pthigh":
        ch=26
    elif d=="d_Dimuon_lxy11p0to16p0_iso0_ptlow":
        ch=27
    elif d=="d_Dimuon_lxy11p0to16p0_iso0_pthigh":
        ch=28
    elif d=="d_Dimuon_lxy11p0to16p0_iso1_ptlow":
        ch=29
    elif d=="d_Dimuon_lxy11p0to16p0_iso1_pthigh":
        ch=30
    elif d=="d_Dimuon_lxy16p0to70p0_iso0_ptlow":
        ch=31
    elif d=="d_Dimuon_lxy16p0to70p0_iso0_pthigh":
        ch=32
    elif d=="d_Dimuon_lxy16p0to70p0_iso1_ptlow":
        ch=33
    elif d=="d_Dimuon_lxy16p0to70p0_iso1_pthigh":
        ch=34
    elif d=="d_Dimuon_lxy0p0to0p2_non-pointing":
        ch=35
    elif d=="d_Dimuon_lxy0p2to1p0_non-pointing":
        ch=36
    elif d=="d_Dimuon_lxy1p0to2p4_non-pointing":
        ch=37
    elif d=="d_Dimuon_lxy2p4to3p1_non-pointing":
        ch=38
    elif d=="d_Dimuon_lxy3p1to7p0_non-pointing":
        ch=39
    elif d=="d_Dimuon_lxy7p0to11p0_non-pointing":
        ch=40
    elif d=="d_Dimuon_lxy11p0to16p0_non-pointing":
        ch=41
    elif d=="d_Dimuon_lxy16p0to70p0_non-pointing":
        ch=42    
    catExtB = "_ch%d_%s"%(ch,year)
    channel = str(ch)
    p_values = []
    m_values = []
    colors = []
    for m in masses:
        # Get workspace
        finame = "%s/%s_Signal_HTo2ZdTo2mu2x_MZd-%s_ctau-1.00mm_%s_workspace.root"%(fitDir,d,str(m).replace('.','p'), year)
        # Open input file with workspace
        f = ROOT.TFile(finame)
        print("> Opened file: %s"%(finame))
        # Retrieve workspace from file
        w = f.Get('wfit')
        #print("> Workspace contents:")
        #w.Print()
        # Retrieve background normalization
        nBG = w.var("roomultipdf%s_norm"%catExtB).getValV()
        #
        mass = str(m)
        mass = mass.replace('.0', '')
        output_json = "%s/gof_%s_ch%s_M%s.json"%(outdir, model, channel,  mass)
        if not os.path.exists(output_json):
            seed = str(int(m))
            ### Generate summary
            command = "combineTool.py -M CollectGoodnessOfFit --input %s/higgsCombine_ch%s.GoodnessOfFit.mH%s.root %s/higgsCombine_ch%s.GoodnessOfFit.mH%s.%s.root -o %s -m %s"%(indir, channel, mass, indir, channel, mass, seed, output_json, mass)
            print(command)
            try:
                os.system(command)
            except OSError:
                print("Point %f for %s wont be included"%(m,d))
                continue
        try:
            with open(output_json, 'r') as file:
                data = json.load(file)
                p_values.append(data[next(iter(data))]["p"])
        except FileNotFoundError:
            print("Point %f for %s wont be included"%(m,d))
            continue            
        if nBG < 1:
            colors.append('tab:red')
            p_values_zero.append(data[next(iter(data))]["p"])
        elif nBG >= 1 and nBG < 10:
            colors.append('tab:orange')
            p_values_low.append(data[next(iter(data))]["p"])
        elif nBG >= 10 and nBG < 100:
            colors.append('tab:blue')
            p_values_med.append(data[next(iter(data))]["p"])
        else:
            colors.append('tab:green')
            p_values_high.append(data[next(iter(data))]["p"])
        m_values.append(m)

    i = channel_dict[str(channel)][0]
    j = channel_dict[str(channel)][1]-1
    ax = axes[i, j]
    ax.scatter(np.array(m_values), np.array(p_values), c=colors, s=4)
    ax.set_xscale('log')
    ax.set_xlim(0.4, 60.)
    #ax.set_yscale('log')
    #ax.set_ylim(0.001, 3.0)
    ax.set_ylim(0.0, 1.25)
    y_ticks = [0, 0.25, 0.5, 0.75, 1.0]
    #y_ticks = [0.001, 0.01, 0.1, 1.0]
    y_labels = ['0', '0.25', '0.5', '0.75', '1']
    #y_labels = ['0.001', '0.01', '0.1', '1.0']
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    #ax.text(0.5, 1.6, lxycat[i]+cat[j], fontsize=6)
    ax.text(0.5, 1.1, lxycat[i]+cat[j], fontsize=6)
    ax.grid(True)
    # Masking
    ax.axvspan(getLowerMask(0.41), getUpperMask(0.50),  color='lightgray', alpha=1.0) # Ks
    ax.axvspan(getLowerMask(0.51), getUpperMask(0.59),  color='lightgray', alpha=1.0) # Eta
    ax.axvspan(getLowerMask(0.73), getUpperMask(0.83),  color='lightgray', alpha=1.0) # rho/w
    ax.axvspan(getLowerMask(0.96), getUpperMask(1.08),  color='lightgray', alpha=1.0) # phi
    ax.axvspan(getLowerMask(2.91), getUpperMask(3.27),  color='lightgray', alpha=1.0) # JPsi
    ax.axvspan(getLowerMask(2.89), getUpperMask(3.33),  color='lightgray', alpha=1.0) # JPsi
    ax.axvspan(getLowerMask(3.47), getUpperMask(3.94),  color='lightgray', alpha=1.0) # PSi2S
    ax.axvspan(getLowerMask(8.88), getUpperMask(10.85), color='lightgray', alpha=1.0) # Upsilon
legend_labels = ['0 events', '0-10 events', '10-100 events', 'More than 100 events']  # Colores que desees
legend_colors = ['tab:red', 'tab:orange', 'tab:blue', 'tab:green']
legend_elements = [Patch(facecolor=color, label=label) for color, label in zip(legend_colors, legend_labels)]
fig.legend(handles=legend_elements, loc='upper left', ncol=4, fontsize=14, bbox_to_anchor=(0.12, 0.968))
#fig.suptitle('Goodness of fit', fontsize=20)
fig.text(0.9, 0.94, "%s (13.6 TeV)"%year, ha='right', fontsize=15)
fig.text(0.5, 0.04, r'Dimuon invariant mass $m_{\mu\mu}$ (GeV)', ha='center', fontsize=18)
fig.text(0.04, 0.5, 'p-value', va='center', rotation='vertical', fontsize=18)

plt.subplots_adjust(hspace=0.0, wspace=0.0, top=0.93)
fig.savefig('gof_summary_%s.png'%year, dpi=160)

# histogram for p_value distribution:
hep.style.use("CMS")
fig_p, axes_p = plt.subplots(1, 1, figsize=(10, 8))
bins_p = np.linspace(0., 1.04, 27)
hist_zero, _ = np.histogram(p_values_zero, bins=bins_p)
hist_low, _ = np.histogram(p_values_low, bins=bins_p)
hist_med, _ = np.histogram(p_values_med, bins=bins_p)
hist_high, _ = np.histogram(p_values_high, bins=bins_p)
data = [hist_zero, hist_low, hist_med, hist_high]
hep.histplot(data, bins=bins_p, ax=axes_p, stack=True, histtype='fill', edgecolor='k', color=['tab:red', 'tab:orange', 'tab:blue', 'tab:green'], label=['nBG = 0', r'1 $\leq$ nBG < 10',  r'10 $\leq$ nBG < 100',  r'nBG $\geq$ 100'])
axes_p.set_ylabel('Counts')
axes_p.set_xlabel('p-value')
axes_p.legend(frameon=True)
hep.cms.label("Internal", data=True, year='2022', com='13.6')
fig_p.savefig('gof_pvalues_%s.png'%year, dpi=160)








