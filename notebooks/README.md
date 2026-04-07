# Notebooks

To plot the main figures for the paper and supplementary material.

## From UAF

To use in uaf-2 (or other remote machine) first tunnel through ssh in your local:
```
ssh -N -L 8893:localhost:8893 username@uaf-2.t2.ucsd.edu
```

and within this directory in your remote:
```
SCRAMARCH=el8_amd64_gcc10
CMSSWVERSION=CMSSW_12_6_0
source env/bin/activate
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/$SCRAMARCH/cms/cmssw/$CMSSWVERSION/src ; eval `scramv1 runtime -sh` ; cd -
jupyter notebook --no-browser --port=8893
```

Which can be activated using:
```
source init.sh
```

## From VS-Code (recommended)

First you can `cmsenv` in your favorite release and then you have to create the kernel:
```
python3 -m venv venv_root
source venv_root/bin/activate
pip install --upgrade pip
pip install ipykernel jupyter
```

## Main paper plots


## Fit plots


## Limit plot
