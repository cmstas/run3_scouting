#!/bin/bash

# Submit the BDT working-point job to HTCondor (UCSD UAF).
#
# Usage:
#   sh condor/BDT_onCondor.sh ['notar']
#
#   notar : skip rebuilding package_BDT.tar.gz (reuse the existing one)
#
# Output: when each job finishes, condor delivers its results unpacked to
#   <repo>/BDT/working_point_<bkgrej>/   (no manual extraction needed).

export STARTDIR=$PWD
mkdir -p condor/plotting_logs

if [ ! -d tuples_parking_nochi2 ]; then
    echo "ERROR: tuples_parking_nochi2/ not found in $STARTDIR -- nothing to transfer."
    exit 1
fi

if [ "$1" != "notar" ]; then
    echo "Creating package_BDT.tar.gz ..."
    sh condor/BDT_create_package.sh
fi

if [ ! -f package_BDT.tar.gz ]; then
    echo "ERROR: package_BDT.tar.gz missing (run without 'notar' to build it)."
    exit 1
fi

condor_submit condor/BDT_onCondor.sub
