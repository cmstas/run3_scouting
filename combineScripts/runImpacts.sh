#!/bin/bash
# script to run preliminary sets of tests on different selections of the search regions
# datacard is the datacard that you select
# directory is the basename of the dirs containing this datacard for a given search region selection
dir=$1
tag=$2
datacard=$3
m=$4
model=$5
rmin=$6
mask=$7
inj=%8

# more variables
name="-n _${model}_M${m}_${tag}"

###
## Initial fits
###
options="--cminDefaultMinimizerStrategy 0 -t -1"
#
eval "combine -M FitDiagnostics ${dir}/${datacard} ${options} --expectSignal 0 ${name}_t0 -m ${m} --forceRecreateNLL --rMin ${rmin} ${mask}"
eval "python3 ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics_${model}_M${m}_${tag}_t0.root -g plots_${model}_m${m}_${tag}_t0.root >& fitResults_${model}_m${m}_${tag}_t0.txt"

### Impacts (signal=0)
options="--cminDefaultMinimizerStrategy 0 -t -1"
#
eval "combineTool.py -M Impacts -d ${dir}/${datacard} ${options} --expectSignal 0 ${name}_${tag}_t0 -m ${m} --doInitialFit --rMin ${mask}"
eval "combineTool.py -M Impacts -d ${dir}/${datacard} -o impacts_${model}_m${m}_${tag}_t0.json ${options} --expectSignal 0 ${name}_${tag}_t0 -m ${m} --doFits --parallel 20 --task-name ${model}_m${m}_${tag}_t0  >& /dev/null"
eval "combineTool.py -M Impacts -d ${dir}/${datacard} -m ${m} ${name}_${tag}_t0 -o impacts_${model}_m${m}_${tag}_t0.json"
eval "plotImpacts.py -i impacts_${model}_m${m}_${tag}_t0.json -o impacts_${model}_m${m}_${tag}_t0"

