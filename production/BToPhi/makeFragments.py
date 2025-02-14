import os
import sys
import argparse
from datetime import date

### Initial setup 
mphi_grid = [0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.25, 1.5, 2.0, 2.85, 3.35, 4.0, 5.0]
ctau_grid = [0.1, 1.0, 10.0, 100.0]

#fragmentTEMPLATE = 'fragment-templates/BToPhi_MPhi-MPHI_ctau-CTAUmm_TuneCP5_13p6TeV-pythia8_noFilter_cfi.py' # should be common for both
#fragmentNAME = 'BToPhi_MPhi-{MPHI}_ctau-{CTAU}mm_TuneCP5_13p6TeV-pythia8_noFilter_cfi.py'
fragmentTEMPLATE = 'fragment-templates/BToPhi_MPhi-MPHI_ctau-CTAUmm_TuneCP5_13p6TeV-pythia8_cfi.py' # should be common for both
fragmentNAME = 'BToPhi_MPhi-{MPHI}_ctau-{CTAU}mm_TuneCP5_13p6TeV-pythia8_cfi.py'

with open(fragmentTEMPLATE, 'r') as file_:
    fragmentTEXT = file_.read()

user = os.environ.get("USER")
today = date.today().strftime("%b-%d-%Y")
output = 'outputFragments_' + today + '/'
if not os.path.isdir(output):
    os.makedirs(output)
print('> Output fragments will be saved in: ' + output) 

### Process the masses
for mphi in mphi_grid:
    for ctau in ctau_grid:
        if ctau != 0.0:
            MPHI = str(mphi)
            CTAU = str(ctau)
            temp_txt = fragmentTEXT.format(MPHI=MPHI, CTAU=CTAU)
            out_fragment = fragmentNAME.format(MPHI=MPHI.replace('.','p'), CTAU=CTAU.replace('.', 'p'))
        else:
            MPHI = str(mphi)
            temp_txt = fragmentTEXT.format(MPHI=MPHI, CTAU="1e-14")
            out_fragment = fragmentNAME.format(MPHI=MPHI.replace('.','p'), CTAU='0p0')
        with open(output + out_fragment, 'w') as file_:
            file_.write(temp_txt)
            file_.close()

