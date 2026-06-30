#!/bin/bash

# Worker-node executable for the BDT

set -e

SCRAMARCH=el8_amd64_gcc12
CMSSWVERSION=CMSSW_15_0_2

echo "=== Args forwarded to workingpoint.py: $@"
echo "=== Scratch dir: ${_CONDOR_SCRATCH_DIR:=$PWD}"
cd "$_CONDOR_SCRATCH_DIR"

# CMSSW from cvmfs provides the python with xgboost / sklearn / uproot.
ulimit -s unlimited
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=$SCRAMARCH
cd /cvmfs/cms.cern.ch/$SCRAMARCH/cms/cmssw/$CMSSWVERSION/src ; eval `scramv1 runtime -sh` ; cd -

# Headless matplotlib + writable config/cache dirs on the worker.
export MPLBACKEND=Agg
export MPLCONFIGDIR="$_CONDOR_SCRATCH_DIR/mplconfig"
export XDG_CACHE_HOME="$_CONDOR_SCRATCH_DIR/cache"
mkdir -p "$MPLCONFIGDIR" "$XDG_CACHE_HOME"

# Reassemble the layout workingpoint.py expects: BDT/ and tuples dir.
tar xzf package_BDT.tar.gz
mv tuples_parking_nochi2 ScoutingRun3/.

cd ScoutingRun3/BDT
echo "=== python: $(which python3)"
python3 -c "import xgboost, sklearn, uproot; print('deps OK', xgboost.__version__, sklearn.__version__)"

echo "=== Running: python3 workingpoint.py $@"
python3 workingpoint.py "$@"
RC=$?
echo "=== workingpoint.py exit code: $RC"
[ $RC -ne 0 ] && exit $RC

cd "$_CONDOR_SCRATCH_DIR/ScoutingRun3/BDT"
echo "=== Output dirs produced:"; ls -d working_point_* 2>/dev/null || echo "  (none found!)"
mv working_point_* "$_CONDOR_SCRATCH_DIR/"

echo "=== Done."
