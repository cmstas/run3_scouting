#!/bin/bash

SCRAMARCH=el9_amd64_gcc12
CMSSWVERSION=CMSSW_15_0_2

OUTDIR=$1
YEAR=$2
PROCESS=$3
STARTFILE=$4
NFILES=$5
ISCONDOR=1
FROMCRAB=${6:-1}

function stageout {
    COPY_SRC=$1
    COPY_DEST=$2
    retries=0
    COPY_STATUS=1
    until [ $retries -ge 10 ]
    do
        echo "Stageout attempt $((retries+1)): env -i X509_USER_PROXY=${X509_USER_PROXY} xrdcp -f ${COPY_SRC} ${COPY_DEST}"
        env -i X509_USER_PROXY=${X509_USER_PROXY} xrdcp -f ${COPY_SRC} ${COPY_DEST}
        COPY_STATUS=$?
        if [ $COPY_STATUS -ne 0 ]; then
            echo "Failed stageout attempt $((retries+1))"
        else
            echo "Successful stageout with $retries retries"
            break
        fi
        retries=$[$retries+1]
        echo "Sleeping for 5m"
        sleep 5m
    done
    if [ $COPY_STATUS -ne 0 ]; then
        echo "xrdcp failed after 10 retries with code $COPY_STATUS"
        exit 1
    fi
}

ulimit -s unlimited
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/$SCRAMARCH/cms/cmssw/$CMSSWVERSION/src ; eval `scramv1 runtime -sh` ; cd -

env -i X509_USER_PROXY=${X509_USER_PROXY} xrdcp -f root://eosuser.cern.ch//${STARTDIR}/package.tar.gz package.tar.gz
tar xvf package.tar.gz
cd ScoutingRun3/cpp
echo $OUTDIR $YEAR $PROCESS $STARTFILE $NFILES $ISCONDOR $FROMCRAB
./main.exe $OUTDIR $YEAR $PROCESS $STARTFILE $NFILES $ISCONDOR $FROMCRAB

for FILE in $(ls $OUTDIR);
do
  echo "File $FILE to be copied..."
  COPY_SRC="file://`pwd`/${OUTDIR}/$FILE"
  COPY_DEST="root://eosuser.cern.ch//${STARTDIR}/${OUTDIR}/$FILE"
  stageout $COPY_SRC $COPY_DEST
done;
