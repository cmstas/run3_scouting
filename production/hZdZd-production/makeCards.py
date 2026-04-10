import os
import sys
from utils import *
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--model", default="mass_epsilon_gamma_ctau.txt", help="Table with the model")
parser.add_argument("--mode", default="lifetime", help="Can also be 'epsilon'")
args = parser.parse_args()

filename = args.model
mode = args.mode
inputdir = "card-templates/"
tmp_customizecards = "LL_HAHM_MS_400_kappa_0p01_MZd_ZDMASS_eps_EPSILON_customizecards.dat"
tmp_extramodels    = "LL_HAHM_MS_400_kappa_0p01_MZd_ZDMASS_eps_EPSILON_extramodels.dat"
tmp_proc_card      = "LL_HAHM_MS_400_kappa_0p01_MZd_ZDMASS_eps_EPSILON_proc_card.dat"
tmp_run_card       = "LL_HAHM_MS_400_kappa_0p01_MZd_ZDMASS_eps_EPSILON_run_card.dat"

with open(inputdir + tmp_customizecards, 'r') as file_:
    txt_customizecards = file_.read()

with open(inputdir + tmp_extramodels, 'r') as file_:
    txt_extramodels = file_.read()

with open(inputdir + tmp_proc_card, 'r') as file_:
    txt_proc_card = file_.read()

with open(inputdir + tmp_run_card, 'r') as file_:
    txt_run_card = file_.read()

## Pick the model txt sile
grid = parse_table(filename)
im = 0.0
model_grid = []
for i in range(1, len(grid)):
    if grid[i][0]!=im:
        im = grid[i][0]
        model_grid.append([])
        model_grid[-1].append(grid[i][0])
        model_grid[-1].append([])
    model_grid[-1][1].append(grid[i][1])
        
print("Grid to producel, obtained from: {}".format(filename))
print(model_grid)

if not os.path.isdir('hZdZd/'):
    os.makedirs('hZdZd/')
bashfile =  open('hZdZd/runCards.sh', 'w')
for p,point in enumerate(grid):
    if p==0: continue
    mass = str(point[0])
    epsilon = str(point[1])
    ctau = str(point[3])
    if mode == "epsilon":
        bashtxt = './gridpack_generation.sh LL_HAHM_MS_400_kappa_0p01_MZd_{ZDMASS}_eps_{EPSILON} cards/hZdZd/hZdZd_mZd_{ZDMASS}_eps_{EPSILON}\n'.format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon)
        bashfile.write("""echo ">>>>>> GENERATING NEW GRID PACK FOR MZD = {ZDMASS} AND EPSILON = {EPSILON}"\n""".format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon))
        bashfile.write(bashtxt)
        outdir = 'hZdZd/hZdZd_mZd_{ZDMASS}_eps_{EPSILON}/'.format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon)
        customizecards = tmp_customizecards.replace('ZDMASS', '{ZDMASS}').replace('EPSILON', '{EPSILON}').format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon)
        extramodels = tmp_extramodels.replace('ZDMASS', '{ZDMASS}').replace('EPSILON', '{EPSILON}').format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon)
        proc_card = tmp_proc_card.replace('ZDMASS', '{ZDMASS}').replace('EPSILON', '{EPSILON}').format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon)
        run_card = tmp_run_card.replace('ZDMASS', '{ZDMASS}').replace('EPSILON', '{EPSILON}').format(ZDMASS = mass.replace('.', 'p'), EPSILON = epsilon)
    if mode == "lifetime":
        bashtxt = './gridpack_generation.sh LL_HAHM_MS_400_kappa_0p01_MZd_{ZDMASS}_ctau_{CTAU} cards/hZdZd/hZdZd_mZd_{ZDMASS}_ctau_{CTAU} condor\n'.format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau)
        bashfile.write("""echo ">>>>>> GENERATING NEW GRID PACK FOR MZD = {ZDMASS} AND CTAU = {CTAU}"\n""".format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau))
        bashfile.write(bashtxt)
        outdir = 'hZdZd/hZdZd_mZd_{ZDMASS}_ctau_{CTAU}/'.format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau)
        customizecards = tmp_customizecards.replace('ZDMASS', '{ZDMASS}').replace('eps_EPSILON', 'ctau_{CTAU}').format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau)
        extramodels = tmp_extramodels.replace('ZDMASS', '{ZDMASS}').replace('eps_EPSILON', 'ctau_{CTAU}').format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau)
        proc_card = tmp_proc_card.replace('ZDMASS', '{ZDMASS}').replace('eps_EPSILON', 'ctau_{CTAU}').format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau)
        run_card = tmp_run_card.replace('ZDMASS', '{ZDMASS}').replace('eps_EPSILON', 'ctau_{CTAU}').format(ZDMASS = mass.replace('.', 'p'), CTAU = ctau)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    # Note: Cards are written in terms of mass - epsilon although the name of the card changes in each case
    with open(outdir + customizecards, 'w') as file_:
        out_customizecards = txt_customizecards.format(ZDMASS = mass, EPSILON = epsilon) # not replace the '.'
        file_.write(out_customizecards)
        file_.close()
    with open(outdir + extramodels, 'w') as file_:
        out_extramodels = txt_extramodels # No need to format (?)
        file_.write(out_extramodels)
        file_.close()
    with open(outdir + proc_card, 'w') as file_:
        out_proc_card = txt_proc_card.format(ZDMASS = mass.replace('.', 'p'), EPSILON = ctau) # CHECK CHECK
        out_proc_card = out_proc_card.replace('_eps_', '_ctau_')
        file_.write(out_proc_card)
        file_.close()
    with open(outdir + run_card, 'w') as file_:
        out_run_card = txt_run_card # No need to format (?)
        file_.write(out_run_card)
        file_.close()

bashfile.close()

