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
            #allmasses=(0.5 0.7 1.5 2.0 2.5 5.0 6.0 7.0 8.0 12.0 14.0 16.0 20.0 22.0 24.0 30.0 34.0 40.0 44.0 50.0)
            #allmasses=(30.000 40.000 50.000)
            allmasses=(2.000)
            #allCTaus=(0.10 0.16 0.25 0.40 0.63 1.00 1.60 2.50 4.00 6.30 10.00 16.00 25.00 40.00 63.00 100.00 160.00 250.00 400.00 630.00 1000.00)
            allCTaus=(0.10 0.16 0.25 0.40 0.63 1.00 1.60 2.50 4.00 6.30 10.00)
        fi
    fi
    if [ ${model} == "BToPhi" ]
    then
        if [ $# -gt 6 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            allmasses=(1.250 1.500 2.000)
            allCTaus=(0.10 0.16 0.25 0.40 0.63 1.00 1.60 2.50 4.00 6.30 10.00 16.00 25.00 40.00 63.00 100.00)
            #allmasses=(4.300 4.360 4.440 4.520 4.600)
            #allCTaus=(1.00 10.00 100.00)
        fi
    fi
    if [ ${model} == "ScenarioA" ] 
    then
        if [ $# -gt 6 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            #allmasses=("2.000_M0.670" "4.000_M1.330" "4.000_M1.900" "5.000_M2.400" "10.000_M2.000" "10.000_M4.900")
            allmasses=("2.000_M0.670" "4.000_M1.330" "1.000_M0.330" "5.000_M1.670" "6.000_M2.000" "7.500_M2.500" "12.000_M1.200")
            #allmasses=("2.000_M0.670" "4.000_M1.330")
            #allCTaus=(0.10 0.25 0.40 0.60 1.00 2.50 4.00 6.00 10.00 16.00 25.00 40.00 60.00 100.00)
            allCTaus=(1000.00)
        fi
    fi
    if [ ${model} == "ScenarioB1" ] 
    then
        if [ $# -gt 6 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            #allmasses=("2.000_M0.670" "4.000_M1.330")
            allmasses=("2.000_M0.670" "4.000_M1.330" "5.000_M1.670" "6.000_M2.000" "7.500_M2.500" "12.000_M1.200")
            #allCTaus=(0.10 0.25 0.40 0.60 1.00 2.50 4.00 6.00 10.00 16.00 25.00 40.00 60.00 100.00)
            allCTaus=(1000.00)
        fi
    fi
fi


echo $which
#options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=1"
#options="--cminDefaultMinimizerStrategy 0 -v 0 --rMax 10"
#options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams -v 0"
options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams -v 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2"
for m in ${allmasses[@]}
do
    for t in ${allCTaus[@]}
    do
        if [ ${model} != "nomodel" ]
        then
            #if [ ${model} == "HTo2ZdTo2mu2x" ] && [ ${t} -gt 10 ] && [ ${m} -lt 1.0 ]
            #then
            #    continue
            #fi
            name="-n _${which}_${model}_M${m}"
            card="card_combined_${model}_M${m}_ctau${t}_${period}.root"
            if [ ${which} == "asymptotic" ]
            then
                #eval "combine -M AsymptoticLimits ${indir}/${card} ${options} ${name} -m ${m} >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
                #eval "combine -M AsymptoticLimits ${indir}/${card} ${options} ${name} -m 125 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
                echo "combineTool.py -M AsymptoticLimits ${indir}/${card} ${options} ${name} -m 125 --parallel 16 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
                eval "combineTool.py -M AsymptoticLimits ${indir}/${card} ${options} ${name} -m 125 --parallel 16 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysObs" ]
            then
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -H AsymptoticLimits -T 100 --rMin 0.05 ${options} ${name} -m 125 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysExp" ]
            then
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -H AsymptoticLimits -T 10 --rMin 0.05 ${options} ${name} -m 125 --expectedFromGrid=0.5 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEm1" ]
            then
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -H AsymptoticLimits -T 100 --rMin 0.05 ${options} ${name} -m 125 --expectedFromGrid=0.16 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEp1" ]
            then
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -H AsymptoticLimits -T 100 --rMin 0.5 ${options} ${name} -m 125 --expectedFromGrid=0.84 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEm2" ]
            then
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -H AsymptoticLimits -T 100 --rMin 0.05 ${options} ${name} -m 125 --expectedFromGrid=0.025 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEp2" ]
            then
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -H AsymptoticLimits -T 100 --rMin 0.5 ${options} ${name} -m 125 --expectedFromGrid=0.975 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "sigExp" ]
            then
                eval "combine ${indir}/${card} -M Significance ${options} ${name} -m ${m} --uncapped=1 --rMin=-5 --rMax=5 -t -1 --expectSignal=1 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "sigObs" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M Significance ${options} ${name} -m ${m} --uncapped=1 --rMin=-5 --rMax=5 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            fi
            rm higgsCombine*_${which}_${model}_M${m}*.root
        fi
    done
done
