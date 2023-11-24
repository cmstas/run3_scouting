#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)
export SCRAM_ARCH=el8_amd64_gcc10
FRAGMENTS=$1
WORK=$PWD
CFGPATH="$PWD/configs"

# Set CMSSW ENV and cp fragments
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_11_patch3/src ] ; then
  echo release CMSSW_12_4_11_patch3 already exists
else
  scram p CMSSW CMSSW_12_4_11_patch3
fi
cd CMSSW_12_4_11_patch3/src
eval `scram runtime -sh`
mkdir -p Configuration/GenProduction/python
cd ../../
cp $FRAGMENTS/*.py CMSSW_12_4_11_patch3/src/Configuration/GenProduction/python/
cd CMSSW_12_4_11_patch3/src
scram b
cmsenv

# Create the cfg files
if [ -r $CFGPATH ] ; then
  echo "configs/ dir already exists"
else
  mkdir $CFGPATH
fi
EVENTS=200
SEED=$(($(date +%s) % 100 + 1));
for FILE in Configuration/GenProduction/python/*.py; do
    FILENAME="$(basename $FILE)"
    if [ $FILE == "Configuration/GenProduction/python/__init__.py" ]; then
        continue;
    fi
    prefix=${FILENAME%_TuneCP5_13p6TeV_pythia8_cff.*};
    suffix="_cfg.py"
    CFG="$prefix$suffix";
    ROOT="file:$prefix.root"
    cmsDriver.py $FILE --python_filename $CFG --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:output_gensim.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc -n $EVENTS;
    mv $CFG $CFGPATH;
done
