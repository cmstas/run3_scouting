#!/bin/bash

cp $(voms-proxy-info -path) $HOME/x509proxy
export X509_USER_PROXY=$HOME/x509proxy

usage()
{
    echo "Usage:"
    echo ""
    echo "  sh condor/runScoutingLooper_DQCD_2024_onCondor.sh ['notar'] output_tag"
    echo ""
    echo "  output_tag : a label for the output directory, e.g. looperOutput_2024_May-04-2026"
    echo "  notar      : skip repackaging (use existing package.tar.gz)"
    echo ""
    echo "Output lands in: /store/group/Run3Scouting/<output_tag>/"
    echo ""
    exit
}

if [ -z "$1" ]; then usage; fi

notar=0
indir=""

if [ "$1" == "notar" ]; then
    notar=1
    indir=$2
else
    indir=$1
fi

if [ -z "$indir" ]; then usage; fi

export SCOUTINGOUTPUTDIR=${indir}
export STARTDIR=$PWD

echo "Output will be staged to: /store/group/Run3Scouting/${SCOUTINGOUTPUTDIR}"
mkdir -p /ceph/cms/store/group/Run3Scouting/${SCOUTINGOUTPUTDIR}
mkdir -p condor/plotting_logs

if [ ${notar} -eq 0 ]; then
    echo "Creating package..."
    sh condor/create_package_2024.sh
fi

condor_submit condor/runScoutingLooper_DQCD_2024_onCondor.sub
