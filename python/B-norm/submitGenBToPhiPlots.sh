#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)

usage()
{
    echo "Usage:"
    echo ""
    echo "  sh condor/runScoutingHistos_onCondor.sh ['notar'] input_dir output_dir"
    echo ""
    echo "The output_dir will be created in /ceph/cms/store/user/$USER/Run3ScoutingOutput/"
    echo "Control the jobs to be run by editing runScoutingHistos_onCondor.sub or the corresponding 2023 file"
    echo ""
    exit
}


export STARTDIR=$PWD

mkdir -p python/B-norm/logs
mkdir -p /ceph/cms/store/user/$USER/Run3ScoutingOutput/B-Studies

## Create package
cp python/B-norm/make_BToPhi_genStudy.py .
tar -chJf package_b.tar.gz make_BToPhi_genStudy.py

masses=("0p3" "0p4" "0p5" "0p6" "0p7" "0p9" "1p25" "1p5" "2p0" "2p85" "3p35" "4p0" "5p0")
for m in ${masses[@]}
do
    export MASS="${m}"
    condor_submit python/B-norm/submitGenBToPhiPlots.sub
done