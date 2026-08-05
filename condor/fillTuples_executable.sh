#!/bin/bash

# Worker-node executable for the fillTuplesScouting job (one job per sample).

set -e

SCRAMARCH=el8_amd64_gcc12
CMSSWVERSION=CMSSW_15_0_2

echo "=== Args forwarded to fillTuplesScouting.py: $@"
echo "=== Scratch dir: ${_CONDOR_SCRATCH_DIR:=$PWD}"
cd "$_CONDOR_SCRATCH_DIR"

ulimit -s unlimited
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=$SCRAMARCH
cd /cvmfs/cms.cern.ch/$SCRAMARCH/cms/cmssw/$CMSSWVERSION/src ; eval `scramv1 runtime -sh` ; cd -


export STARTDIR="$_CONDOR_SCRATCH_DIR"

export USER="${USER:-$(whoami)}"
export PWD="${PWD:-$(pwd)}"

# Reassemble the expected layout: ScoutingRun3/{fillTuplesScouting.py,utils,data}.
tar xzf package_fillTuples.tar.gz

cd ScoutingRun3
echo "=== python: $(which python3)"
python3 -c "import ROOT, numpy, correctionlib, awkward, uproot; from DataFormats.FWLite import Events, Handle; print('deps OK')"

echo "=== Running: python3 fillTuplesScouting.py $@ --condor --outDir $_CONDOR_SCRATCH_DIR/outputHistograms_2024"
python3 fillTuplesScouting.py "$@" --condor --outDir "$_CONDOR_SCRATCH_DIR/outputHistograms_2024"
RC=$?
echo "=== fillTuplesScouting.py exit code: $RC"
[ $RC -ne 0 ] && exit $RC

# Both output dirs already sit at the scratch top (tuples via STARTDIR, histos via
# --outDir) with their final names, so the .sub transfers them back as-is (no remap).
cd "$_CONDOR_SCRATCH_DIR"
echo "=== tuples produced:";     ls -ld tuples_*/ 2>/dev/null && ls -l tuples_*/ 2>/dev/null || echo "  (no tuples_*/ dir found!)"
echo "=== histograms produced:"; ls -l outputHistograms_2024/ 2>/dev/null || echo "  (none found!)"

echo "=== Done."
