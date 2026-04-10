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
            allmasses=(0.5 0.7 1.5 2.0 2.5 5.0 6.0 7.0 8.0 12.0 14.0 16.0 20.0 22.0 24.0 30.0 34.0 40.0 44.0 50.0)
            allCTaus=(1 10 100)
        fi
    fi
    if [ ${model} == "BToPhi" ]
    then
        if [ $# -gt 6 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            allmasses=(0.5 0.7 1.5 2.0 2.5 5.0 6.0 7.0 8.0 12.0 14.0 16.0 20.0 22.0 24.0 30.0 34.0 40.0 44.0 50.0)
            allCTaus=(1 10 100)
        fi
    fi
    if [ ${model} == "ScenarioA" ] || [ ${model} == "ScenarioB1" ] || [ ${model} == "ScenarioB2" ]
    then
        if [ $# -gt 6 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            allmasses=("4.000_M1.330" "5.000_M2.400")
            allCTaus=(0.10 1.00 10.00 100.00)
        fi
    fi
fi


options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 -v 0"
#options="--cminDefaultMinimizerStrategy 0 -v 0 --rMax 10"
#options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams -v 0"
for m in ${allmasses[@]}
do
    for t in ${allCTaus[@]}
    do
        if [ ${model} != "nomodel" ]
        then
            name="-n _${which}_${model}_M${m}_ctau${t}"
            card="card_combined_${model}_M${m}_ctau${t}_${period}.root"
            limitfile="higgsCombine_${which}_${model}_M${m}_ctau${t}.AsymptoticLimits.mH125.root"
            eval "combineTool.py -M AsymptoticLimits ${indir}/${card} ${options} ${name} -m 125 --parallel 16 >& ${outdir}/lim_asymptotic_${model}_m${m}_ctau${t}_${period}.txt"
            # Get limit values for next limit derivation
            eval $(root -b -q "combineScripts/getLimitResults.C(\"${limitfile}\")" | grep '^LIM' | tr -d '\r')
            echo "Values of asymptotics: "
            echo $LIM0
            echo $LIM1
            echo $LIM2
            echo $LIM3
            echo $LIM4
            if [ ${which} == "toysObs" ]
            then
		        RMIN=$(echo "0.5 * ${LIM0}" | bc -l)
		        RMAX=$(echo "1.5 * ${LIM4}" | bc -l)
                RABS=$(echo "0.01 * ${LIM5}" | bc -l)
		        echo "${LIM0}, ${LIM1}, ${LIM2}, ${LIM3}, ${LIM4}, ${LIM5}"
                echo "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125"
                #eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 100 --rMin ${RMIN} --rMax ${RMAX} ${options} ${name} -m 125"
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysExp" ]
            then
		        RMIN=$(echo "0.5 * ${LIM2}" | bc -l)
		        RMAX=$(echo "1.5 * ${LIM2}" | bc -l)
                RABS=$(echo "0.01 * ${LIM2}" | bc -l)
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125 --expectedFromGrid=0.5 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEm1" ]
            then
		        RMIN=$(echo "0.1 * ${LIM1}" | bc -l)
		        RMAX=$(echo "2.0 * ${LIM1}" | bc -l)
                RABS=$(echo "0.01 * ${LIM1}" | bc -l)
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125 --expectedFromGrid=0.16 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEp1" ]
            then
		        RMIN=$(echo "0.5 * ${LIM3}" | bc -l)
		        RMAX=$(echo "1.5 * ${LIM3}" | bc -l)
                RABS=$(echo "0.01 * ${LIM3}" | bc -l)
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125 --expectedFromGrid=0.84 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEm2" ]
            then
		        RMIN=$(echo "0.1 * ${LIM0}" | bc -l)
		        RMAX=$(echo "2.0 * ${LIM0}" | bc -l)
                RABS=$(echo "0.01 * ${LIM0}" | bc -l)
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125 --expectedFromGrid=0.025 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "toysEp2" ]
            then
		        RMIN=$(echo "0.5 * ${LIM4}" | bc -l)
		        RMAX=$(echo "1.5 * ${LIM4}" | bc -l)
                RABS=$(echo "0.01 * ${LIM4}" | bc -l)
                eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T 500 --rMin ${RMIN} --rMax ${RMAX} --rAbsAcc=${RABS} ${options} ${name} -m 125 --expectedFromGrid=0.975 >& ${outdir}/lim_${which}_${model}_m${m}_ctau${t}_${period}.txt"
            elif [ ${which} == "grid" ]
            then
                NTOY=500
		        #RMIN=$(echo "0.5 * ${LIM0}" | bc -l)
		        RMIN=$(echo "0.1 * ${LIM0}" | bc -l)
		        RMAX=$(echo "1.5 * ${LIM4}" | bc -l)
                INT=$(echo "${RMAX} - ${RMIN}" | bc -l)
                STEP=$(echo "0.01 * ${INT}" | bc -l)
                echo $RMIN
                echo $RMAX
                echo $INT
                echo $STEP
                if [ $# -lt 8 ]
                then
                    # Run a grid of 100 r points well defined in one go
                    echo "Running grid from ${RMIN} to ${RMAX} in steps of ${STEP}"
                    echo "combineTool.py ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T ${NTOY} ${options} ${name} --saveHybridResult -m 125 --clsAcc 0 --singlePoint ${RMIN}:${RMAX}:${STEP} --iterations 2"
                    eval "combineTool.py ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T ${NTOY} ${options} ${name} --saveHybridResult -m 125 --clsAcc 0 --singlePoint ${RMIN}:${RMAX}:${STEP} --iterations 2"
                    hadd higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root higgsCombine_${which}_${model}_M${m}*.root
                    eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root -m 125 ${options} --expectedFromGrid=0.025 >& ${outdir}/lim_toysEm2_${model}_m${m}_ctau${t}_${period}.txt"
                    eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root -m 125 ${options} --expectedFromGrid=0.16 >& ${outdir}/lim_toysEm1_${model}_m${m}_ctau${t}_${period}.txt"
                    eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root -m 125 ${options} --expectedFromGrid=0.84 >& ${outdir}/lim_toysEp1_${model}_m${m}_ctau${t}_${period}.txt"
                    eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root -m 125 ${options} --expectedFromGrid=0.975 >& ${outdir}/lim_toysEp2_${model}_m${m}_ctau${t}_${period}.txt"
                    eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root -m 125 ${options} --expectedFromGrid=0.5 >& ${outdir}/lim_toysExp_${model}_m${m}_ctau${t}_${period}.txt"
                    eval "combine ${indir}/${card} -M HybridNew --LHCmode LHC-limits --readHybridResults --grid=higgsCombine_${model}_M${m}_ctau${t}_${period}_merged.root -m 125 ${options} >& ${outdir}/lim_toysObs_${model}_m${m}_ctau${t}_${period}.txt"
                    rm higgsCombine*.root
                elif [ $# -lt 9 ]
                then
                    # Run point NUM of the 100 r points (only)
                    name="-n _${which}_${model}_M${m}_ctau${t}"
                    NTOY=2000 #3000
                    NUM=$8
                    DELTA=$(echo "${NUM} * ${STEP}" | bc -l)
                    POINT=$(echo "${RMIN} + ${DELTA}" | bc -l)
                    echo "Running point ${POINT} of grid from ${RMIN} to ${RMAX} in steps of ${STEP}"
                    echo "combineTool.py ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T ${NTOY} ${options} ${name} --saveHybridResult -m 125 --clsAcc 0 --singlePoint ${POINT} --iterations 2 -s -1 -H AsymptoticLimits"
                    eval "combineTool.py ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T ${NTOY} ${options} ${name} --saveHybridResult -m 125 --clsAcc 0 --singlePoint ${POINT} --iterations 2 -s -1 -H AsymptoticLimits"
                    mv higgsCombine*HybridNew*.root ${outdir}
                else
                    # Run from point MINNUM to MAXNUM of the 100 r points (only)
                    name="-n _${which}_${model}_M${m}_ctau${t}"
                    NTOY=2000
                    MINNUM=$8
                    MAXNUM=$9
                    MINDELTA=$(echo "${MINNUM} * ${STEP}" | bc -l)
                    MAXDELTA=$(echo "${MAXNUM} * ${STEP}" | bc -l)
                    IRMIN=$(echo "${RMIN} + ${MINDELTA}" | bc -l)
                    IRMAX=$(echo "${RMIN} + ${MAXDELTA}" | bc -l)
                    echo "Running grid from ${MINNUM} to ${MAXNUM} in steps of ${STEP}"
                    echo "combineTool.py ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T ${NTOY} ${options} ${name} --saveHybridResult -m 125 --clsAcc 0 --singlePoint ${IRMIN}:${IRMAX}:${STEP} --iterations 2"
                    eval "combineTool.py ${indir}/${card} -M HybridNew --LHCmode LHC-limits -T ${NTOY} ${options} ${name} --saveHybridResult -m 125 --clsAcc 0 --singlePoint ${IRMIN}:${IRMAX}:${STEP} --iterations 2"
                    mv higgsCombine*HybridNew*.root ${outdir}
                fi
            elif [ ${which} == "sigExp" ]
            then
                eval "combine ${indir}/${card} -M Significance ${options} ${name} -m ${m} --uncapped=1 --rMin=-5 --rMax=5 -t -1 --expectSignal=1 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            elif [ ${which} == "sigObs" ]
            then
                eval "combine ${indir}/card_combined_${model}_M${m}_allyears.root -M Significance ${options} ${name} -m ${m} --uncapped=1 --rMin=-5 --rMax=5 >& ${outdir}/lim_${which}_${model}_m${m}.txt"
            fi
            #rm higgsCombine*_${which}_${model}_M${m}*.root
        fi
    done
done
