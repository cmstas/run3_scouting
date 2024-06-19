CMSSWVERSION=CMSSW_12_6_0
TAG=v9.1.0
if [ $# -gt 0 ]
then
    if [ $1=="EL8" ]
    then
        CMSSWVERSION=CMSSW_13_3_0
        TAG=v10.0.0
    fi
fi

cmsrel $CMSSWVERSION
pushd $CMSSWVERSION/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
pushd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout $TAG
scramv1 b clean; scramv1 b # always make a clean build
popd
scram b
popd
