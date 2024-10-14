#
#
mass=$1
ctau=$2
rmin=-1.5 # before -1.5
rinj=1.0
#
combine -M FitDiagnostics /home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Looper8p0/run3_scouting/datacards_all_Sep-27-2024_2022/card_combined_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_2022.root --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal $rinj -n _HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj} -m 2 --forceRecreateNLL --rMin $rmin
#
python3 $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -a fitDiagnostics_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj}.root -g plots_HTo2ZdTo2mu2x_M2.0_ctau10_t${rinj}.root >> fitResults_HTo2ZdTo2mu2x_M2.0_ctau10_t${rinj}.txt
#
combineTool.py -M Impacts -d /home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Looper8p0/run3_scouting/datacards_all_Sep-27-2024_2022/card_combined_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_2022.root --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal $rinj -n _HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj} -m 2 --doInitialFit --rMin $rmin
#
combineTool.py -M Impacts -d /home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Looper8p0/run3_scouting/datacards_all_Sep-27-2024_2022/card_combined_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_2022.root -o impacts_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj}.json --cminDefaultMinimizerStrategy 0 -t -1 --expectSignal $rinj -n _HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj} -m 2 --rMin $rmin --doFits --parallel 20 --task-name _HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj} >& /dev/null
#
combineTool.py -M Impacts -d /home/users/fernance/Run3-Analyses/SnT-Scouting/Code/Looper8p0/run3_scouting/datacards_all_Sep-27-2024_2022/card_combined_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_2022.root -m 2 -n _HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj} -o impacts_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj}.json
#
plotImpacts.py -i impacts_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj}.json -o impacts_HTo2ZdTo2mu2x_M${mass}_ctau${ctau}_t${rinj}
#
