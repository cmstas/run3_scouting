#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)

DIR=$1
OUT=$2
SIG=$3 # HTo2ZdTo2mu2x
LIM=$4 # asymptotic, toysObs, toysExp, toysEm2, toysEm1, toysEp1, toysEp2, sigExp, sigObs

MASS=2.0
CTAU=1

if [ $# -lt 5 ]
then
    MASS=2.0
    CTAU=1
elif [ $# -lt 6 ]
then
    MASS=$5
    CTAU=1
else
    MASS=$5
    CTAU=$6
fi

function stageout {
    COPY_SRC=$1
    COPY_DEST=$2
    retries=0
    COPY_STATUS=1
    until [ $retries -ge 10 ]
    do
        echo "Stageout attempt $((retries+1)): env -i X509_USER_PROXY=${X509_USER_PROXY} gfal-copy -p -f -t 7200 --verbose --checksum ADLER32 ${COPY_SRC} ${COPY_DEST}"
        env -i X509_USER_PROXY=${X509_USER_PROXY} gfal-copy -p -f -t 7200 --verbose --checksum ADLER32 ${COPY_SRC} ${COPY_DEST}
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
        echo "Removing output file because gfal-copy crashed with code $COPY_STATUS"
        env -i X509_USER_PROXY=${X509_USER_PROXY} gfal-rm --verbose ${COPY_DEST}
        REMOVE_STATUS=$?
        if [ $REMOVE_STATUS -ne 0 ]; then
            echo "Uhh, gfal-copy crashed and then the gfal-rm also crashed with code $REMOVE_STATUS"
            echo "You probably have a corrupt file sitting on hadoop now."
            exit 1
        fi
    fi
}

source /cvmfs/cms.cern.ch/cmsset_default.sh
tar xvf package.tar.gz
cd ScoutingRun3/
cd HiggsAnalysis/CombinedLimit
. env_standalone.sh
cd ../../

#cd CMSSW_12_6_0/src
#scram b -j 8
#cmsenv
#cd HiggsAnalysis/CombinedLimit
#. env_standalone.sh
#cd ../../../../

ls -la

rm -rf ${OUT}
mkdir -p ${OUT}
bash combineScripts/submitLimits.sh ${DIR} ${OUT} ${SIG} ${LIM} ${MASS} ${CTAU}

for FILE in $(ls ${OUT})
do
  echo "File $FILE to be copied..."
  echo ""
  COPY_SRC="file://`pwd`/${OUT}/$FILE"
  COPY_DEST="davs://redirector.t2.ucsd.edu:1095/store/user/$USER/Run3ScoutingOutput/${OUT}/${FILE}"
  stageout $COPY_SRC $COPY_DEST
done
