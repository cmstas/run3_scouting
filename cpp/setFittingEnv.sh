export SCRAM_ARCH=slc7_amd64_gcc10
cmsrel CMSSW_12_6_0
pushd CMSSW_12_6_0/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
pushd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v9.1.0
scramv1 b clean; scramv1 b # always make a clean build
popd
scram b
popd
