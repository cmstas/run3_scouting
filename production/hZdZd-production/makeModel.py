import os
import sys
import math
import pickle
from utils import parse_table

#
# Partial width for a fermion [Eq.(2.12)]
# Not used here but can be useful to keep just in case
def computePartGamma(mZd, mf, gL, gR):
    Nc = 3.0 # Assuming 3 colors
    term1 = Nc / (24.0*math.pi*mZd)
    term2 = math.sqrt(1.0 - (4.0*mf**2)/(mZd**2))
    term3 = mZd**2 * (gL**2 + gR**2)
    term4 = mf**2 * (-6.0*gL*gR + gL**2 + gR**2)
    value = term1 * term2 * (term3 - term4)
    return value


# Constants
CHSLASH = 0.19733e-15 # GeV*m

# Get br table data for the dark photon decay
info = parse_table('model-tables/HiggsedDarkPhoton_BrTableData.txt')

########## File with mass / epsilon / ctau
#
# Init the file
model_file = open('mass_epsilon_gamma_ctau.txt', 'w')
model_file.write('mZd (GeV)\tEpsilon\t\tGammaZd (GeV)\t\tctau (mm)\n')

## Select mode: if "lifetime" ir creates a (m, ctau) grid and if "epsilon" a (m, epsilon) one!
mode = "lifetime" # or epsilon

if mode=="epsilon":

    #
    # Init the grid
    biggrid = False
    model_grid = [] # mass : [epsilon values]
    if biggrid:
        masses = [0.7, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        epsilon = [1e-08, 2e-08, 3e-08, 4e-08, 5e-08, 6e-08, 7e-08, 8e-08, 9e-08]
        epsilon += [1e-07, 2e-07, 3e-07, 4e-07, 5e-07, 6e-07, 7e-07, 8e-07, 9e-07]
        epsilon += [1e-06, 2e-06, 3e-06, 4e-06, 5e-06, 6e-06, 7e-06, 8e-06, 9e-06]
        for mass in masses:
            point = [mass]
            point.append(epsilon)
            model_grid.append(point)
    else:
        model_grid.append([0.7, [5e-06, 2e-06, 5e-07, 2e-07]])
        model_grid.append([1,   [5e-06, 2e-06, 5e-07, 2e-07]])
        model_grid.append([2,   [9e-07, 4e-07]])
        model_grid.append([3,   [3e-06, 1e-06, 3e-07, 1e-07]])
        model_grid.append([5,   [5e-07, 2e-07]])
        model_grid.append([7,   [1e-06, 6e-07, 2e-07, 7e-08]])
        model_grid.append([10,  [5e-07, 1e-07]])
        model_grid.append([20,  [2e-07, 5e-08]])

    #
    # Init the loop
    for model in model_grid:
        mZd = model[0]
        smZd = str(mZd)
        epsilon_list = model[1]
        true_ref = []
        for r,ref in enumerate(info):
            mZd_ref = ref[0]
            mZd_sref = mZd_ref[:]
            if '.' == mZd_sref[-1]:
                mZd_sref = mZd_sref[:-1]
            if smZd==mZd_ref or smZd==mZd_sref:
                true_ref = ref
                break
            if r==len(info)-1 and len(true_ref)<1:
                print('Mass %s not available, skipping...'% smZd)
        if len(true_ref) > 0:
            sgammaZd_over_eps = true_ref[1]
            gammaZd_over_eps = float(sgammaZd_over_eps)
            for epsilon in epsilon_list:
                # For model file
                gammaZd = gammaZd_over_eps * epsilon * epsilon
                sgammaZd = str(gammaZd)
                lifetime = CHSLASH * 1000. / gammaZd
                sepsilon = str(epsilon)
                slifetime = str(lifetime)
                outline = "{}\t\t{:.0e}\t\t{:.5e}\t\t{:.3f}\n".format(smZd, epsilon, gammaZd, lifetime)
                model_file.write(outline)

if mode=="lifetime":

    # Mass-lifetime prop
    mass_proposal = [] # in GeV
    mass_proposal += [0.5, 0.7]
    mass_proposal += [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
    mass_proposal += [12.0, 14.0, 16.0, 20.0]
    mass_proposal += [22.0, 24.0]
    mass_proposal += [32.0, 34.0, 38.0]
    mass_proposal += [42.0, 46.0, 50.0]

    ctau_proposal = [1, 10, 100, 1000] # in mm (only integers or change string formatting below to not loose precision)

    ctau_grid = []

    for mass in mass_proposal:
        mZd = mass
        smZd = str(mZd)
        true_ref = []
        for r,ref in enumerate(info):
            if r==0: continue
            mZd_ref = ref[0]
            mZd_sref = mZd_ref[:]
            if '.' == mZd_sref[-1]:
                mZd_sref = mZd_sref[:-1]
            if smZd==mZd_ref or smZd==mZd_sref or float(mZd_ref)==mZd:
                true_ref = ref
                break
            if r==len(info)-1 and len(true_ref)<1:
                print('Mass %s not available, skipping...'% smZd)
        if len(true_ref) > 0:
            sgammaZd_over_eps = true_ref[1]
            gammaZd_over_eps = float(sgammaZd_over_eps)
            epsilon_grid = []
            for ctau in ctau_proposal:
                # For model file
                gammaZd = CHSLASH * 1000. / ctau
                epsilon = (gammaZd / gammaZd_over_eps)**0.5
                sgammaZd = str(gammaZd)
                lifetime = ctau
                epsilon_grid.append(epsilon)
                sepsilon = str(epsilon)
                slifetime = str(lifetime)
                outline = "{}\t\t{:.3e}\t\t{:.5e}\t\t{:.0f}\n".format(smZd, epsilon, gammaZd, lifetime)
                model_file.write(outline)

model_file.close()

