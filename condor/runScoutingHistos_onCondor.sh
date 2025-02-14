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

if [ -z $2 ]; then usage; fi

notar=0
year23=0
indir=""
outdir=""
extraflags=""

if [ $# -gt 1 ]
then
    if [ "$1" == "notar" ]
    then
        if [ "$2" == "2023" ]
        then
            notar=1
            year23=1
            indir=$3
            outdir=$4
        else
            notar=1
            indir=$2
            outdir=$3
        fi
    else
        if [ "$1" == "2023" ]
        then
            year23=1
            indir=$2
            outdir=$3
        else
            indir=$1
            outdir=$2
        fi
    fi
fi

offset=$(($notar+$year23+2))
i=1
for arg in "$@"
do
    if [ $i -gt ${offset} ]
    then
        extraflags="$extraflags $arg"
    fi
    i=$((i + 1))
done

export SCOUTINGINPUTDIR=${indir}
export SCOUTINGOUTPUTDIR=${outdir}
export SCOUTINGARGS=${extraflags}
export STARTDIR=$PWD

mkdir -p condor/plotting_logs
mkdir -p /ceph/cms/store/user/$USER/Run3ScoutingOutput/$SCOUTINGOUTPUTDIR

if [ ${notar} -gt 0 ]
then
   if [ ${year23} -gt 0 ]
   then
      #condor_submit condor/runScoutingHistos_onCondor2023.sub
      condor_submit condor/runScoutingHistos_dataOnly_onCondor2023.sub
   else
      #condor_submit condor/runScoutingHistos_onCondor.sub
      #condor_submit condor/runScoutingHistos_dataOnly_onCondor.sub
      condor_submit condor/runScoutingHistos_limited_onCondor.sub
      #condor_submit condor/runScoutingHistos_testSignal_onCondor.sub
   fi
else
   sh condor/create_package.sh
   if [ ${year23} -gt 0 ]
   then
      #condor_submit condor/runScoutingHistos_onCondor2023.sub
      condor_submit condor/runScoutingHistos_dataOnly_onCondor2023.sub
   else
      #condor_submit condor/runScoutingHistos_onCondor.sub
      #condor_submit condor/runScoutingHistos_dataOnly_onCondor.sub
      condor_submit condor/runScoutingHistos_limited_onCondor.sub
      #condor_submit condor/runScoutingHistos_testSignal_onCondor.sub
   fi
fi
