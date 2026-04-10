#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)

OUT=$1
SIG=$2 # HTo2ZdTo2mu2x
PERIOD=$3 # Year
MASS=$4
#SIG=$3 # HTo2ZdTo2mu2x

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
cmssw-el8
tar xvf package.tar.gz
cd ScoutingRun3/

cmsrel CMSSW_13_3_0
cp -r HiggsAnalysis CMSSW_13_3_0/src
cd CMSSW_13_3_0/src
scramv1 b clean; scramv1 b
cmsenv
cd ../../

#ls -la

rm -rf ${OUT}
mkdir -p ${OUT}
#echo "combineScripts/submitFits.sh ${MASS} ${PERIOD}"
#bash combineScripts/submitFits.sh ${MASS} ${PERIOD}
echo "cpp/doAll_fitDimuonMass_onCondor.C(${MASS}, ${PERIOD})"
root -b -q -l -n "cpp/doAll_fitDimuonMass_onCondor.C(${MASS}, ${PERIOD})"


for FILE in $(ls fitResults_${PERIOD}_inCondor)
do
  echo "File $FILE to be copied..."
  echo ""
  COPY_SRC="file://`pwd`/${OUT}/$FILE"
  COPY_DEST="davs://redirector.t2.ucsd.edu:1095/store/user/$USER/Run3ScoutingOutput/${OUT}/${FILE}"
  stageout $COPY_SRC $COPY_DEST
done
