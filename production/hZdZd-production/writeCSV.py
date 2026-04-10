import os
import csv
from utils import *
import argparse

### Script only enabled for ctau configuration



# Init line params
DATASET_ = "HTo2ZdTo2mu2x_MZd-{}_ctau-{:.0f}mm_TuneCP5_13p6TeV_madgraph-pythia8"
FRAGMENT_ = "genFragments/Generator/Pythia/HTo2ZdTo2mu2x_lowMass_extension/13p6TeV/HTo2ZdTo2mu2x_MZd-{}_ctau-{:.0f}mm_TuneCP5_13p6TeV_pythia8_cff.py"
GRIDPACK_ = "/eos/user/f/fernance/gridpacks/LLPScouting/LL_HAHM_extension/LL_HAHM_MS_400_kappa_0p01_MZd_{}_ctau_{:.0f}_el9_amd64_gcc11_CMSSW_13_2_9_tarball.tar.xz"

# Open and read model file
print("Grid to produce:")
#print(grid)
grid = []
mphi_grid = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, 16.0, 20.0, 22.0, 24.0]
ctau_grid = [1000]

for m in mphi_grid:
    for t in ctau_grid:
        mlabel = (str(m)).replace('.', 'p')
        tlabel = (str(t)).replace('.', 'p')
        grid.append([mlabel, '-', tlabel])

# Create the CSV file

with open("request_hZdZd.csv", "w") as file_:
    writer = csv.writer(file_)
    writer.writerow(["dataset","fragment","events","generator","gridpack"])
    for p,point in enumerate(grid):
        if p==0: 
            continue
        highstat = False
        mass = point[0]
        ctau = float(point[2])
        dataset = DATASET_.format(mass, ctau)
        fragment = FRAGMENT_.format(mass, ctau)
        events = "300000"
        generator = "madgraph"
        gridpack = GRIDPACK_.format(mass, ctau)
        writer.writerow([dataset,fragment,events,generator,gridpack])
        #line="{},{},{},{},{}".format(dataset, fragment, events, generator, gridpack)

#csv.close()
