#!/bin/bash

ulimit -s unlimited
export useSignalMC=1

indir=$1
outdir=$2
model=$3
which=$4
period=$5

mass=2.0
ctau=1
if [ $# -lt 6 ]
then
    mass=2.0
    ctau=1
elif [ $# -lt 7 ]
then
    mass=$6
    ctau=0
else
    mass=$6
    ctau=$7
fi


allmasses=()
if [ ${useSignalMC} == 1 ]
then
    if [ ${model} == "HTo2ZdTo2mu2x" ]
    then
        if [ $# -gt 6 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            allmasses=(0.5 0.7 1.5 2.0 2.5 5.0 6.0 7.0 8.0 12.0 14.0 16.0, 20.0 22.0 24.0 30.0 34.0 40.0 44.0 50.0)
            allCTaus=(1 10 100)
        fi
    fi
fi


#options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=1"
options="--cminDefaultMinimizerStrategy 0 -v 0 --rMax 10"
for m in ${allmasses[@]}
do
    for t in ${allCTaus[@]}
    do
        if [ ${model} != "nomodel" ]
        then
            if [ ${model} == "HTo2ZdTo2mu2x" ] && [ ${t} -gt 10 ] && [ ${m} -lt 1.0 ]
            then
                continue
            fi
            name="-n _${which}_${model}_M${m}"
            if [ ${which} == "asymptotic" ]
            then
                eval "combine -M AsymptoticLimits ${indir}/card_combined_${model}_M${m}_ctau${t}_${period}.root ${options} ${name} -m ${m} >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysObs" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M HybridNew --LHCmode LHC-limits -T 500 -i 2 --rAbsAcc=0.01 --rRelAcc=0.025 ${options} ${name} -m ${m} >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "toysExp" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M HybridNew --LHCmode LHC-limits -T 500 -i 2 --rAbsAcc=0.01 --rRelAcc=0.025 ${options} ${name} -m ${m} --expectedFromGrid=0.5 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "toysEm1" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M HybridNew --LHCmode LHC-limits -T 500 -i 2 --rAbsAcc=0.01 --rRelAcc=0.025 ${options} ${name} -m ${m} --expectedFromGrid=0.16 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "toysEp1" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M HybridNew --LHCmode LHC-limits -T 500 -i 2 --rAbsAcc=0.01 --rRelAcc=0.025 ${options} ${name} -m ${m} --expectedFromGrid=0.84 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "toysEm2" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M HybridNew --LHCmode LHC-limits -T 500 -i 2 --rAbsAcc=0.01 --rRelAcc=0.025 ${options} ${name} -m ${m} --expectedFromGrid=0.025 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "toysEp2" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M HybridNew --LHCmode LHC-limits -T 500 -i 2 --rAbsAcc=0.01 --rRelAcc=0.025 ${options} ${name} -m ${m} --expectedFromGrid=0.975 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "sigExp" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M Significance ${options} ${name} -m ${m} --uncapped=1 --rMin=-5 --rMax=5 -t -1 --expectSignal=1 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "sigObs" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M Significance ${options} ${name} -m ${m} --uncapped=1 --rMin=-5 --rMax=5 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            fi
            rm higgsCombine*_${which}_${model}_M${m}*.root
        fi
    done
done
