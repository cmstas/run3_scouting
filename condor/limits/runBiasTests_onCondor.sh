#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)

usage()
{
    echo "Usage:"
    echo ""
    echo "  sh utils/condor_limits/runLimits_onCondor.sh input_dir output_dir period"
    echo ""
    echo "The output_dir will be created in /ceph/cms/store/user/$USER/ZPrimeSnTOutput/"
    echo "Control the jobs to be run by editing runLimits_onCondor.sub"
    echo ""
    exit
}

if [ -z $1 ]; then usage; fi

export SCOUTINGSNTINPUTDIRLIM=$1
export SCOUTINGSNTOUTPUTDIRLIM=$2
export PERIOD=$3
export EXPECTEDLIM=$4
export SCOUTINGEXPECTEDLIM=$(basename "$EXPECTEDLIM")
export RINJ=$5
export HOMEDIR=$PWD

echo "Creating dirs..."

mkdir -p condor/limits/bias_logs
mkdir -p /ceph/cms/store/user/$USER/Run3ScoutingOutput/$SCOUTINGSNTOUTPUTDIRLIM

cp $EXPECTEDLIM .

echo "Creating the package..."
#sh condor/limits/create_package.sh $SCOUTINGSNTINPUTDIRLIM $SCOUTINGEXPECTEDLIM fitResults_${PERIOD}
sh condor/limits/create_package.sh $SCOUTINGSNTINPUTDIRLIM $SCOUTINGEXPECTEDLIM

echo "Submission started"
condor_submit condor/limits/runBiasTests_onCondor.sub
