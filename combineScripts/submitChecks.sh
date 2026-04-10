#!/bin/bash

export useSignalMC=1
d=`date +%b-%d-%Y`
#inputDate="Sep-29-2022"
inputDate="Oct-07-2022"

echo ">>> submitChecks.sh is running......"

indir=$1
outdir=$2
model=$3
period=$4
#eval "cp ./utils/index.php ${outdir}"

mass=2.0
ctau=1
channels=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42)

if [ $# -lt 5 ]
then
    mass=2.0
    ctau=1.00
elif [ $# -lt 6 ]
then
    mass=$5
    ctau=0
elif [ $# -lt 7 ]
then
    mass=$5
    ctau=$6
else
    mass=$5
    ctau=$6
    if [[ $7 == 1 ]]; then
    	channels=(1 2)
    elif [[ $7 == 2 ]]; then
        channels=(3 4 5 6)
    elif [[ $7 == 3 ]]; then
        channels=(7 8 9 10)
    elif [[ $7 == 4 ]]; then
        channels=(11 12 13 14)
    elif [[ $7 == 5 ]]; then
        channels=(15 16 17 18)
    elif [[ $7 == 6 ]]; then
        channels=(19 20 21 22)
    elif [[ $7 == 7 ]]; then
        channels=(23 24 25 26)
    elif [[ $7 == 8 ]]; then
        channels=(27 28 29 30)
    elif [[ $7 == 9 ]]; then
        channels=(31 32 33 34)
    elif [[ $7 == 10 ]]; then
        channels=(35 36 37 38)
    elif [[ $7 == 11 ]]; then
        channels=(39 40 41 42)
    fi
fi

toys=200
if (( $(echo "$mass < 4.0" | bc -l) )); then
    toys=100
    echo "Using reduced number of toys"
fi

allmasses=()
if [ ${useSignalMC} == 1 ]
then
    if [ ${model} == "HTo2ZdTo2mu2x" ]
    then
        if [ $# -gt 5 ]
        then
            allmasses=(${allmasses} ${mass})
            allCTaus=(${allCTaus} ${ctau})
        else
            allmasses=(0.5 0.7 1.5 2.0 2.5 5.0 6.0 7.0 8.0 12.0 14.0 16.0 20.0 22.0 24.0 30.0 34.0 40.0 44.0 50.0)
            allCTaus=(1 10 100)
        fi
    fi
fi

#channels=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42)
#channels=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 41)
#channels=(9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 41)

options="--cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=1 -t -1 --rMin -1 --X-rtd TMCSO_PseudoAsimov=5000"
for m in ${allmasses[@]}
do
    for t in ${allCTaus[@]}
    do
        if [ ${model} != "nomodel" ]
        then
            if [ ${model} == "HTo2ZdTo2mu2x" ] && [ ${t} -gt 10 ] && [ ${m} -lt 1.0]
            then
                continue
            fi
            ### Fit diagnostics
            #name="-n _${model}_M${m}"
            #options="--cminDefaultMinimizerStrategy 0 --rMin -1 --toysFrequentist" 
            ##options="--cminDefaultMinimizerStrategy 0 -t -1 --rMin -1 --toysFrequentist" 
            #options=${options}" --X-rtd MINIMIZER_freezeDisassociatedParams"
            ##options=${options}" --X-rtd TMCSO_PseudoAsimov=5000"
            #### (signal=0)
            #eval "combine -M FitDiagnostics ${indir}/card_combined_${model}_M${m}_allyears.root ${options} --expectSignal 0 ${name}_t0 -m ${m} --forceRecreateNLL"
            #eval "python ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics_${model}_M${m}_t0.root -g ${outdir}/plots_${model}_m${m}_t0.root >& ${outdir}/fitResults_${model}_m${m}_t0.txt"
            #### (signal=1)
            #eval "combine -M FitDiagnostics ${indir}/card_combined_${model}_M${m}_allyears.root ${options} --expectSignal 1 ${name}_t1 -m ${m} --forceRecreateNLL"
            #eval "python ${CMSSW_BASE}/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics_${model}_M${m}_t1.root -g ${outdir}/plots_${model}_m${m}_t1.root >& ${outdir}/fitResults_${model}_m${m}_t1.txt"
            #
            #### Impacts (signal=0)
            #name="-n ${model}_M${m}"
            #options="--cminDefaultMinimizerStrategy 0 --rMin -3"
            ##options="--cminDefaultMinimizerStrategy 0 -t -1 --rMin -5"
            ##options=${options}" --toysFrequentist"
            ##options=${options}" --X-rtd TMCSO_PseudoAsimov=5000"
            #eval "combineTool.py -M Impacts -d ${indir}/card_combined_${model}_M${m}_allyears.root ${options} --expectSignal 0 ${name}_t0 -m ${m} --doInitialFit"
            #eval "combineTool.py -M Impacts -d ${indir}/card_combined_${model}_M${m}_allyears.root -o ${outdir}/impacts_${model}_m${m}_t0.json ${options} --expectSignal 0 ${name}_t0 -m ${m} --doFits --parallel 20 --task-name ${model}_m${m}_t0 >& /dev/null"
            #eval "combineTool.py -M Impacts -d ${indir}/card_combined_${model}_M${m}_allyears.root -m ${m} ${name}_t0 -o ${outdir}/impacts_${model}_m${m}_t0.json ${options}"
            #eval "plotImpacts.py -i ${outdir}/impacts_${model}_m${m}_t0.json -o ${outdir}/impacts_${model}_m${m}_t0"
            #
            #### Impacts (signal=1)
            #options="--cminDefaultMinimizerStrategy 0 --rMin -3"
            ##options="--cminDefaultMinimizerStrategy 0 -t -1 --rMin -5"
            ##options=${options}" --toysFrequentist"
            ##options=${options}" --X-rtd TMCSO_PseudoAsimov=5000"
            #eval "combineTool.py -M Impacts -d ${indir}/card_combined_${model}_M${m}_allyears.root ${options} --expectSignal 1 ${name}_t1 -m ${m} --doInitialFit"
            #eval "combineTool.py -M Impacts -d ${indir}/card_combined_${model}_M${m}_allyears.root -o ${outdir}/impacts_${model}_m${m}_t1.json ${options} --expectSignal 1 ${name}_t1 -m ${m} --doFits --parallel 20 --task-name ${model}_m${m}_t1 >& /dev/null"
            #eval "combineTool.py -M Impacts -d ${indir}/card_combined_${model}_M${m}_allyears.root -m ${m} ${name}_t1 -o ${outdir}/impacts_${model}_m${m}_t1.json ${options}"    
            #eval "plotImpacts.py -i ${outdir}/impacts_${model}_m${m}_t1.json -o ${outdir}/impacts_${model}_m${m}_t1"
            #
            #### Data-card validation
            #eval "ValidateDatacards.py ${indir}/card_combined_${model}_M${m}_allyears.root --jsonFile ${outdir}/validation_${model}_M${m}.json"
            
            ### Goodness-of-fit test (saturated algorithm)
            echo "Starting loop over channels......."
            for nch in ${channels[@]}
            do
                seed=${m%.*}
                #eval "combine -M GoodnessOfFit ${indir}/card_combined_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -m ${m}"
                #eval "combine -M GoodnessOfFit ${indir}/card_combined_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -m ${m} --toysFrequentist"
                #eval "combine -M GoodnessOfFit ${indir}/card_combined_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -t 1 -s ${seed} -m ${m} --toysFrequentist"
                #eval "combineTool.py -M CollectGoodnessOfFit --input higgsCombineTest.GoodnessOfFit.mH${seed}.root higgsCombineTest.GoodnessOfFit.mH${seed}.${seed}.root -o ${outdir}/gof_sb_${model}_M${m}.json -m ${m}"
                #eval "plotGof.py ${outdir}/gof_sb_${model}_M${m}.json --statistic saturated -o ${outdir}/gof_plot_sb_${model}_M${m} --m ${m}.0 --title-left='${model}, M=${m} GeV, S+B fit'"
                
                echo "combine -M GoodnessOfFit ${indir}/card_ch${nch}_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -m ${m} -n _ch${nch} --fixedSignalStrength=0"
                eval "combine -M GoodnessOfFit ${indir}/card_ch${nch}_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -m ${m} -n _ch${nch} --fixedSignalStrength=0"
                echo "combine -M GoodnessOfFit ${indir}/card_ch${nch}_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -m ${m} -n _ch${nch} --toysFrequentist --fixedSignalStrength=0"
                eval "combine -M GoodnessOfFit ${indir}/card_ch${nch}_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -m ${m} -n _ch${nch} --toysFrequentist --fixedSignalStrength=0"
                echo "combine -M GoodnessOfFit ${indir}/card_ch${nch}_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -t ${toys} -s ${seed} -m ${m} -n _ch${nch} --toysFrequentist --fixedSignalStrength=0"
                eval "combine -M GoodnessOfFit ${indir}/card_ch${nch}_${model}_M${m}_ctau${t}_${period}.root --algo=saturated -t ${toys} -s ${seed} -m ${m} -n _ch${nch} --toysFrequentist --fixedSignalStrength=0"
                #eval "combineTool.py -M CollectGoodnessOfFit --input higgsCombineTest.GoodnessOfFit.mH${seed}.root higgsCombineTest.GoodnessOfFit.mH${seed}.${seed}.root -o ${outdir}/gof_${model}_M${m}.json -m ${m}"
                #eval "plotGof.py ${outdir}/gof_${model}_M${m}.json --statistic saturated -o ${outdir}/gof_plot_${model}_M${m} --m ${m}.0 --title-left='${model}, M=${m} GeV, B-only fit'"
            done
        fi
    done
done

#if [ -d "~/public_html/Zprime/${outdir}" ]
#then
#    eval "rm ${outdir}/*.png"
#    eval "cp ${outdir}/* ~/public_html/Zprime/${outdir}/"
#else
#    eval "rm ${outdir}/*.png"
#    eval "cp -r ${outdir} ~/public_html/Zprime/"
#fi

eval "mv higgsCombine*.root ${outdir}/"
#eval "rm fitDiagnostics*.root"
