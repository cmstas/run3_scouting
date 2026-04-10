SCRAMARCH=el8_amd64_gcc10
CMSSWVERSION=CMSSW_12_6_0
source env/bin/activate
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/$SCRAMARCH/cms/cmssw/$CMSSWVERSION/src ; eval `scramv1 runtime -sh` ; cd -
jupyter notebook --no-browser --port=8893
