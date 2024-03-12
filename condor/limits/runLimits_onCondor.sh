#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)

usage()
{
    echo "Usage:"
    echo ""
    echo "  sh utils/condor_limits/runLimits_onCondor.sh input_dir output_dir"
    echo ""
    echo "The output_dir will be created in /ceph/cms/store/user/$USER/ZPrimeSnTOutput/"
    echo "Control the jobs to be run by editing runLimits_onCondor.sub"
    echo ""
    exit
}

if [ -z $1 ]; then usage; fi

export SCOUTINGSNTINPUTDIRLIM=$1
export SCOUTINGSNTOUTPUTDIRLIM=$2
export HOMEDIR=$PWD

mkdir -p condor/limits/plotting_logs
mkdir -p /ceph/cms/store/user/$USER/Run3ScoutingOutput/$SCOUTINGSNTOUTPUTDIRLIM

sh condor/limits/create_package.sh $SCOUTINGSNTINPUTDIRLIM

condor_submit condor/limits/runLimits_onCondor.sub
