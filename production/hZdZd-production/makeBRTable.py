import os
import sys
import math
import pickle
from utils import parse_table

### THIS SCRIPT IS ONLY FOR BR HTML FILES IN A VERY SPECIFIC FORMAT. LENGTHS AND PARAMS ARE HARDCODED AND NEED TO BE CHECKED
### INPUT SHOULD BE A DIR CONTAINING THE RESULTS IN HTML FORMAT LIKE THIS: http://uaf-10.t2.ucsd.edu/~fernance/SnT-Run3Scouting/Tables/results_xsec/
### ALSO NEED TO GIVE THE TABULED BR VALUES FOR ZD->LL IF MASS < 10 GEV

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--results", default="/home/users/fernance/public_html/SnT-Run3Scouting/Tables/results_brs_ctau/", help="Results with brs from MadGraph")
parser.add_argument("--mode", default="lifetime", help="Can also be 'epsilon'")
args = parser.parse_args()

resultspath = args.results
mode = args.mode

# To be used specially at low mass
corr = parse_table('model-tables/HiggsedDarkPhoton_BrTableData.txt')

xsecs_file = open('mass_xsecs.txt', 'w')
brs_file = open('mass_brs.txt', 'w')
brs_corr_file = open('mass_corr_brs.txt', 'w')

if mode=="epsilon":
   xsecs_file.write('mZd\tEpsilon\tXS_MUMU\tXS_EE\tXS_TAUTAU\tXS_UUBAR\tXS_DDBAR\tXS_SSBAR\tXS_CCBAR\tXS_BBBAR\tXS_MUNUMUNUBAR\tXS_ENUENUBAR\tXS_TAUNUTAUNUBAR\n')
   xsecs_line = '{}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\n' 
   brs_file.write('mZd\tEpsilon\t\tBR_MUMU\t\tBR_EE\t\tBR_TAUTAU\tBR_UUBAR\tBR_DDBAR\tBR_SSBAR\tBR_CCBAR\tBR_BBBAR\tBR_MUNUMUNUBAR\tBR_ENUENUBAR\tBR_TAUNUTAUNUBAR\n')
   brs_line = '{}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\n' 
   brs_corr_file.write('mZd\tEpsilon\t\tBR_MUMU\t\tBR_EE\t\tBR_TAUTAU\tBR_UUBAR\tBR_DDBAR\tBR_SSBAR\tBR_CCBAR\tBR_BBBAR\tBR_MUNUMUNUBAR\tBR_ENUENUBAR\tBR_TAUNUTAUNUBAR\n')
   brs_corr_line = '{}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\n' 

if mode=="lifetime":
   xsecs_file.write('mZd\tctau\tXS_MUMU\tXS_EE\tXS_TAUTAU\tXS_UUBAR\tXS_DDBAR\tXS_SSBAR\tXS_CCBAR\tXS_BBBAR\tXS_MUNUMUNUBAR\tXS_ENUENUBAR\tXS_TAUNUTAUNUBAR\n')
   xsecs_line = '{}\t{:.0f}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\n' 
   brs_file.write('mZd\tctau\tBR_MUMU\t\tBR_EE\t\tBR_TAUTAU\tBR_UUBAR\tBR_DDBAR\tBR_SSBAR\tBR_CCBAR\tBR_BBBAR\tBR_MUNUMUNUBAR\tBR_ENUENUBAR\tBR_TAUNUTAUNUBAR\n')
   brs_line = '{}\t{:.0f}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\n' 
   brs_corr_file.write('mZd\tctau\tBR_MUMU\t\tBR_EE\t\tBR_TAUTAU\tBR_UUBAR\tBR_DDBAR\tBR_SSBAR\tBR_CCBAR\tBR_BBBAR\tBR_MUNUMUNUBAR\tBR_ENUENUBAR\tBR_TAUNUTAUNUBAR\n')
   brs_corr_line = '{}\t{:.0f}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\t{:.4e}\n' 


filelist = os.listdir(resultspath)
filelist.sort()

for file in filelist:
    if 'html' not in file or 'swp' in file:
        continue
    smass = (file.split('process_mZd_')[1]).split('_')[0]
    print(file)
    if 'p' in smass:
        smass = smass.replace('p', '.')
    param = 0.0
    if mode=="epsilon":
        param = float((file.split('eps_')[1]).split('.')[0])
    if mode=="lifetime":
        param = float((file.split('ctau_')[1]).split('.')[0])
    info = open(resultspath + file)
    results = []
    xsecs = []
    for l in info.readlines():
        if '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' not in l:
            continue
        results.append(l)
        encoded = l.replace('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>s= ', '')
        encoded =  float(encoded.split('&#177')[0])
        xsecs.append(encoded)
    XS_MUMU          = xsecs[7]
    XS_EE            = xsecs[6]
    XS_TAUTAU        = xsecs[8]
    XS_UUBAR         = xsecs[1]
    XS_DDBAR         = xsecs[2] / 2.0
    XS_SSBAR         = xsecs[2] / 2.0
    XS_CCBAR         = xsecs[4]
    XS_BBBAR         = xsecs[5]
    XS_MUNUMUNUBAR   = xsecs[3] / 3.0
    XS_ENUENUBAR     = xsecs[3] / 3.0
    XS_TAUNUTAUNUBAR = xsecs[3] / 3.0
    # Note: xsecs[0] == sum(xsecs[1:]) so neutrino and dd&ss cross sections are inclusive in flavor
    brs = [x/xsecs[0] for x in xsecs]
    BR_LL            = brs[7] + brs[6] # Only for later computations
    BR_MUMU          = brs[7]
    BR_EE            = brs[6]
    BR_TAUTAU        = brs[8]
    BR_UUBAR         = brs[1]
    BR_DDBAR         = brs[2] / 2.0
    BR_SSBAR         = brs[2] / 2.0
    BR_CCBAR         = brs[4]
    BR_BBBAR         = brs[5]
    BR_MUNUMUNUBAR   = brs[3] / 3.0
    BR_ENUENUBAR     = brs[3] / 3.0
    BR_TAUNUTAUNUBAR = brs[3] / 3.0
    # Now the corrected ones!
    true_ref = []
    for r,ref in enumerate(corr):
        if r==0: continue
        mZd_ref = ref[0]
        mZd_sref = mZd_ref[:]
        if '.' == mZd_sref[-1]:
            mZd_sref = mZd_sref[:-1]
        if smass==mZd_ref or smass==mZd_sref or float(smass)==float(mZd_sref):
            true_ref = ref
            break
        if r==len(corr)-1 and len(true_ref)<1:
            print('Mass %s not available, skipping...'% smass) 
    BRp_LL = float(true_ref[2])
    BRp_MUMU          = BRp_LL / 2.0
    BRp_EE            = BRp_LL / 2.0
    BRp_TAUTAU        = BR_TAUTAU * (1. - BRp_LL) / (1. - BR_LL)
    BRp_UUBAR         = BR_UUBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_DDBAR         = BR_DDBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_SSBAR         = BR_SSBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_CCBAR         = BR_CCBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_BBBAR         = BR_BBBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_MUNUMUNUBAR   = BR_MUNUMUNUBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_ENUENUBAR     = BR_ENUENUBAR * (1. - BRp_LL) / (1. - BR_LL)
    BRp_TAUNUTAUNUBAR = BR_TAUNUTAUNUBAR * (1. - BRp_LL) / (1. - BR_LL)

    final_xsec_line = xsecs_line.format(smass, param, XS_MUMU, XS_EE, XS_TAUTAU, XS_UUBAR, XS_DDBAR, XS_SSBAR, XS_CCBAR, XS_BBBAR, XS_MUNUMUNUBAR, XS_ENUENUBAR, XS_TAUNUTAUNUBAR)
    xsecs_file.write(final_xsec_line)
    final_br_line = brs_line.format(smass, param, BR_MUMU, BR_EE, BR_TAUTAU, BR_UUBAR, BR_DDBAR, BR_SSBAR, BR_CCBAR, BR_BBBAR, BR_MUNUMUNUBAR, BR_ENUENUBAR, BR_TAUNUTAUNUBAR)
    brs_file.write(final_br_line)
    final_br_corr_line = brs_corr_line.format(smass, param, BRp_MUMU, BRp_EE, BRp_TAUTAU, BRp_UUBAR, BRp_DDBAR, BRp_SSBAR, BRp_CCBAR, BRp_BBBAR, BRp_MUNUMUNUBAR, BRp_ENUENUBAR, BRp_TAUNUTAUNUBAR)
    brs_corr_file.write(final_br_corr_line)


xsecs_file.close()
brs_file.close()
