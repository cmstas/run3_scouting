import os
import sys
import argparse
from datetime import date
from utils import *

### Init 

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--dir", default="/ceph/cms/store/user/fernance/Run3ScoutingProduction/hZdZd/Gridpacks_v2/", help="Path to gridpacks")
parser.add_argument("--br", default="mass_corr_brs.txt", help="Table with the branching ratios")
parser.add_argument("--model", default="mass_epsilon_gamma_ctau.txt", help="Table with the model")
parser.add_argument("--mode", default="lifetime", help="Can also be 'epsilon'")
args = parser.parse_args()

### Initial setup 

# Branchin ratios (todo)
brs = parse_table(args.br)

#fragmentTEMPLATE = 'fragment-templates/HTo2ZdTo2mu2x_MZd-ZDMASS_Epsilon-EPSILON_TuneCP5_13p6TeV_pythia8_cff.py' # should be common for both
fragmentTEMPLATE = 'fragment-templates/HTo2ZdTo2mu2x_MZd-ZDMASS_Epsilon-EPSILON_TuneCP5_13p6TeV_pythia8_cff_noExtLHEP.py' # should be common for both
if args.mode=="epsilon":
    fragmentNAME = 'HTo2ZdTo2mu2x_MZd-{ZDMASS}_Epsilon-{EPSILON}_TuneCP5_13p6TeV_pythia8_cff.py'
elif args.mode=="lifetime":
    fragmentNAME = 'HTo2ZdTo2mu2x_MZd-{ZDMASS}_ctau-{CTAU}mm_TuneCP5_13p6TeV_pythia8_cff.py'

with open(fragmentTEMPLATE, 'r') as file_:
    fragmentTEXT = file_.read()

gridpack_loc = args.dir
user = os.environ.get("USER")
today = date.today().strftime("%b-%d-%Y")
output = 'outputFragments_' + today + '/'
if not os.path.isdir(output):
    os.makedirs(output)

print('> Reading gridpacks in: ' + gridpack_loc) 
print('> Output fragments will be saved in: ' + output) 

#
### Process the masses
grid = parse_table(args.model)
model_grid = []
for i in range(1, len(grid)):
    model_grid.append([grid[i][0], grid[i][1], grid[i][3]])
print(model_grid)

for p in model_grid:
    smZd = str(p[0])
    #
    # General parameters:
    ZDMASS           = p[0]
    EPSILON          = p[1]
    LIFETIME         = p[2]
    #
    # Branching ratios:
    true_ref = []
    for b,br in enumerate(brs):
        mZd_ref = br[0] # mass label
        if smZd==mZd_ref:
            true_ref = br
            break
        if b==len(brs)-1 and len(true_ref)<1:
            print('Mass %s not available, skipping...'% smZd)
            print('THIS SHOULD NEVER HAPPEN, REVISIT THE CONFIGURATION')
    BR_MUMU          = true_ref[2]
    BR_EE            = true_ref[3]
    BR_TAUTAU        = true_ref[4]
    BR_UUBAR         = true_ref[5]
    BR_DDBAR         = true_ref[6]
    BR_SSBAR         = true_ref[7]
    BR_CCBAR         = true_ref[8]
    BR_BBBAR         = true_ref[9]
    BR_MUNUMUNUBAR   = true_ref[10]
    BR_ENUENUBAR     = true_ref[11]
    BR_TAUNUTAUNUBAR = true_ref[12]
    if args.mode=="epsilon":
        GRIDPACK = gridpack_loc + 'LL_HAHM_MS_400_kappa_0p01_MZd_{ZDMASS}_eps_{EPSILON}_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'.format(ZDMASS = ZDMASS.replace('.', 'p'), EPSILON = EPSILON)
    if args.mode=="lifetime":
        GRIDPACK = gridpack_loc + 'LL_HAHM_MS_400_kappa_0p01_MZd_{ZDMASS}_ctau_{CTAU}_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'.format(ZDMASS = ZDMASS.replace('.', 'p'), CTAU = LIFETIME)

    temp_txt = fragmentTEXT.format(GRIDPACK = GRIDPACK,
                                   ZDMASS = ZDMASS,
                                   EPSILON = EPSILON,
                                   LIFETIME = LIFETIME,
                                   BR_MUMU = BR_MUMU,
                                   BR_EE = BR_EE,
                                   BR_TAUTAU = BR_TAUTAU,
                                   BR_UUBAR = BR_UUBAR,
                                   BR_DDBAR = BR_DDBAR,
                                   BR_SSBAR = BR_SSBAR,
                                   BR_CCBAR = BR_CCBAR,
                                   BR_BBBAR = BR_BBBAR,
                                   BR_MUNUMUNUBAR = BR_MUNUMUNUBAR,
                                   BR_ENUENUBAR = BR_ENUENUBAR,
                                   BR_TAUNUTAUNUBAR = BR_TAUNUTAUNUBAR)

    if args.mode=="epsilon":
       out_fragment = fragmentNAME.format(ZDMASS = ZDMASS.replace('.', 'p'), EPSILON = EPSILON)
    if args.mode=="lifetime":
       out_fragment = fragmentNAME.format(ZDMASS = ZDMASS.replace('.','p'), CTAU = LIFETIME)
    with open(output + out_fragment, 'w') as file_:
        file_.write(temp_txt)
        file_.close()

