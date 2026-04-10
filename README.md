# Muon scouting

Full workflow is divided in several stages:
1. Production of skims reading from RAW/AODSIM. It processes and stores trigger and tracker information.
2. Production of ntuples reading from the skimmed datasets.
3. Analysis, including histogram plotting, fitting and limit derivation.
4. Statistics checks

Each part is described below, but **a set of example commands to reproduce some of the plots of the analysis is collected in Section [Running the analysis](#running-the-analysis).**

## Installation

Recommended machine and CMSSW version are uaf2-3-4 and CMSSW_13_3_0:

``` shell
git clone --recursive https://github.com/cmstas/run3_scouting.git
```

To keep consistency for the fitting and combine in both local and condor we use singularity:

```
cmssw-el8
cmsrel CMSSW_13_3_0
push CMSSW_13_3_0/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
pushd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v10.0.2
scramv1 b clean; scramv1 b # always make a clean build
popd
scram b
popd
```

## Skimming

The skimming code resides in `batch/`.

The skimming code runs on RAW data sets, and produces a skimmed RAW data set as output
with additional information, mainly:
- HLT and L1T flags;
- tracker information (number of expected muon tracker layers, position of displaced vertices relative to tracker modules).

## NTuple production: Looper (C++)

The C++ looper resides in `cpp/`.

The looper runs on skimmed RAW data sets, and produces a flat tree as output.
Please, refer to `README` in `cpp/` for further instructions.
Condor submission is set up in `condor/`.

Quick submission (for both 2022 and 2023):
```shell
runScoutingLooper_onCondor.sh looperOutput_Dec-04-2023
runScoutingLooper_onCondor.sh 2023 looperOutput_Dec-04-2023
```

## Histograms:

### Histogram filling:

Histograms are filled by `fillHistosScouting.py`, and written in a ROOT output file.
This PyROOT looper optionally applies selections on multi-muon system kinematics and displacement.
Condor submission is set up in `condor/`.

Histograms are defined in `utils/histDefinition.py`:
please, add your histograms there, following the existing structure.

Example to run the histogram filling for 2022 (default) and 2023:
``` shell
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Dec-04-2023/ outputHistograms_Dec-09-2023_allCuts
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Dec-04-2023/ outputHistograms_Dec-09-2023_allCuts
```

... with some selection e.g. the lxy range in [6.5, 11.0] cm:
``` shell
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Dec-04-2023/ outputHistograms_Dec-09-2023_6p5to11p0_allCuts --lxySel 6.5 11.0
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Dec-04-2023/ outputHistograms_Dec-09-2023_6p5to11p0_allCuts --lxySel 6.5 11.0
```

... with a cut not applied e.g the impact parameter selection:
``` shell
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Dec-04-2023/ outputHistograms_Dec-09-2023_6p5to11p0_noMuonIPSel --lxySel 6.5 11.0 --noMuonIPSel
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Dec-04-2023/ outputHistograms_Dec-09-2023_6p5to11p0_noMuonIPSel --lxySel 6.5 11.0 --noMuonIPSel
```

### Histogram plotting:

For plotting output histograms: `plotHistosScouting.py`.
E.g.:
- in order to plot/compare different eras from directory with same selection:
``` shell
python3 plotHistosScouting.py --inSamples Data --inDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_all/ --doRatio --shape --doRatio --logY
```
- in order to plot/compare data with different selection (i.e., from different directories), e.g., with different lxy selections on the dimuon system:
``` shell
python3 plotHistosScouting.py --inSamples Data --inMultiDir /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p95to3p25_relaxedSVselection_onlyDiMuon/ /ceph/cms/store/user/mmasciov/Run3ScoutingOutput/outputHistograms_Aug-02-2023_dimuonMass2p5to2p95-3p25to3p4_relaxedSVselection_onlyDiMuon/ --inMultiLeg "J/#psi" "J/#psi sidebands" --doRatio --relaxedSVSel --dimuonMassSel 2.5 3.4 --shape --doRatio --logY  --noPreSel --noFourMuon --noFourMuonOSV --outSuffix JPsi
```
- in order to make a simple comparison data and signal (assuming 1 pb xsec):
``` shell
python3 plotHistosScouting.py --inSamples Data Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-10mm Signal_ScenB1_30_9p9_4p8_ctau_10mm --inDir run3out/outputHistograms_Dec-09-2023_allCuts --logY --dimuonMassSel 0.0 11.0 --weightSignal --outSuffix 2022_weighted_allCuts
```
- in order to make a simple comparison data and signal (normalized to unity):
``` shell
python3 plotHistosScouting.py --inSamples Data Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-10mm Signal_ScenB1_30_9p9_4p8_ctau_10mm --inDir run3out/outputHistograms_Dec-09-2023_allCuts --logY --dimuonMassSel 0.0 11.0 --shape --outSuffix 2022_norm_allCuts
```


In order to get help with all (optional and required) arguments, just execute the script with no argument:
``` shell
python3 plotHistosScouting.py
```

### Other histogram manipulation scripts:
Other scripts to `hadd` histogram files from a directory, or to merge histograms with different selections (i.e., in different directories) are available in `scripts/`:
- `addHistosScouting.py`: to `hadd` histogram files from a directory;
- `mergeHistograms.py`: to merge histograms with different selections.

`bash` scripts to locally submit jobs are avaiable in the same directory.
E.g., to `hadd` histograms within a directory for all data sub-samples:
``` shell
source scripts/submitLocalAddHistosScouting.sh
```

## Fitting

### Description

### How to run

**Inputs:** A folder with the RooDataSets for data and (optionally) signal simulation.

To perform the fitting in the mass windows, modify the lines within ```cpp/doAll_fitDimuonMass.C``` to define ```model```, ```period``` and ```inDir```. With the examples below:
```
2022: period=2022, model="HTo2ZdTo2mu2x", inDir="/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_allCuts"
2023: period=2023, model="HTo2ZdTo2mu2x", inDir="/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_allCuts"
```

Then run once for each period:
```
root -b -q -l -n cpp/doAll_fitDimuonMass.C
```

<i> -> Remember to properly set the period and input paths inside before running </i>

----

**Output:** A set of workspaces with the dataset and the pdfs (for both background and signal). One workspace is defined per mass window.
These workspaces will be inside a folder of the form ```fitResults_HTo2ZdTo2mu2x_2022``` and ```fitResults_HTo2ZdTo2mu2x_2023``` (assuming you run for `model="HTo2ZdTo2mu2x"`).

If you look inside these dirs you will see something like:

```
[...]
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1000.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2022_workspace.root
[...]
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-20p0_ctau-1000.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-20p0_ctau-100.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-20p0_ctau-10.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso0_pthigh_Signal_HTo2ZdTo2mu2x_MZd-20p0_ctau-1.00mm_2022_workspace.root
[...]
d_Dimuon_lxy1p0to2p4_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1000.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-100.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-10.00mm_2022_workspace.root
d_Dimuon_lxy1p0to2p4_iso1_pthigh_Signal_HTo2ZdTo2mu2x_MZd-14p0_ctau-1.00mm_2022_workspace.root
[...]
```

----

Note 1: Since the fitting takes a lot of time, it is strongly suggested to run by using ```screen```.

Note 2 (probably not needed): In case you run on a sl7 node you can perform the fitting by using a singularity container:

```
cmssw-el8 --bind /ceph/cms/store/
cd CMSSW_13_3_0/src
cmsenv
cd ../../
root -b -q -l -n cpp/doAll_fitDimuonMass.C
```

## Datacard creation

2022 and 2023 are made independently from the workspaces created before, as an example for both years:

```
python3 make_datacards.py sta fitResults_2022_HTo2ZdTo2mu2 2022 HTo2ZdTo2mu2x
python3 make_datacards.py sta fitResults_2022_HTo2ZdTo2mu2 2022 HTo2ZdTo2mu2x
```

The normalization of the signal can be adjusted by using NORMCONST inside `make_datacards.py`. If you select `doSmartScaling=True` (required for toys) the normalization will be done per mass/ctau point to have a -2sigma limit over 0.6. 

Note: sta is an argument stating that we are initally considering all SRs (even though the ones that have very low significance vales are removed later on).

Then, to combine the eras you can run:
```
python3 combineScripts/combineDatacards.py <datacards_2022> <datacards_2023>
```

Note: Order is important, `<datacards_2023> <datacards_2022>` will **not** work.

**Up-to-date examples:**

```
python3 make_datacards.py sta /ceph/cms/store/group/Run3Scouting/Results/fitResults_2022_HTo2ZdTo2mu2_vsCTau_100bins 2022 HTo2ZdTo2mu2x
python3 make_datacards.py sta /ceph/cms/store/group/Run3Scouting/Results/fitResults_2023_HTo2ZdTo2mu2_vsCTau_100bins 2023 HTo2ZdTo2mu2x
```

**Up-to-date datacards:**

Datacards vs Ctau (two years and combined):

```
/ceph/cms/store/group/Run3Scouting/Results/datacards_HTo2ZdTo2mu2x_NormSmart_standard_Apr-28-2025_vsCTau_2022
/ceph/cms/store/group/Run3Scouting/Results/datacards_HTo2ZdTo2mu2x_NormSmart_standard_Apr-28-2025_vsCTau_2023
/ceph/cms/store/group/Run3Scouting/Results/datacards_HTo2ZdTo2mu2x_NormSmart_standard_Apr-28-2025_vsCTau_allEras
```
(these can be used in the next steps)

## Limit extraction

### Run the limits with condor

**Input:** You need a dir with the compiled datacards (ROOT format).

**Commands:** First you need a create a long voms proxy:

```
voms-proxy-init --voms cms --valid 192:00
```

and then the jobs will run with:

```
sh condor/limits/runLimits_onCondor.sh <datacard directory> <limit output directory> <year> <type>
```

The `<type>` argument picks the set of points and the way (asymptotic aproximation or through toys) in which the limits are to be derived. Existing configurations can be checked by doing:

```
sh condor/limits/runLimits_onCondor.sh
```

**Output:** The results of the limits will be saved in the specified `<limit output directory>` in the form of `.txt` files. So for example if you look into the output file you should see something like:

```
lim_asymptotic_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_asymptotic_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_asymptotic_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
lim_toysEm1_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_toysEm1_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_toysEm1_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
lim_toysEm2_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_toysEm2_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_toysEm2_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
lim_toysEp1_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_toysEp1_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_toysEp1_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
lim_toysEp2_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_toysEp2_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_toysEp2_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
lim_toysExp_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_toysExp_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_toysExp_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
lim_toysObs_HTo2ZdTo2mu2x_m50.000_ctau0.10_allEras.txt
lim_toysObs_HTo2ZdTo2mu2x_m50.000_ctau0.16_allEras.txt
lim_toysObs_HTo2ZdTo2mu2x_m50.000_ctau0.25_allEras.txt
[...]
```

Note: Notice that the `lim_toys*Obs*_HTo2ZdTo2mu2x_m*_ctau*_*.txt` files will only be available if you run with one configuration using toys.

----

**Experimental:** There is a new option to run the toys on a grid of `r` points for a single mass-lifetime combination. It will send 1 job for `r` point, so it is not really optimized, but it allows to handle high number of toys (~2000) which is important for the 2.5% band. To be adopted once the splitting is optimized. To run:

```
sh condor/limits/runLimits_ToyGrid_onCondor.sh <datacards> <limit output directory> <year>
```

Since the grid is determined during the job, no smart normalization should be required, but it was only tested with it.

Example:
```
sh condor/limits/runLimits_ToyGrid_onCondor.sh datacards_HTo2ZdTo2mu2x_NormSmart_standard_Apr-28-2025_vsCTau_allEras limits_HTo2ZdTo2mu2x_NormSmart-0p6_May-01-2025_vsCTau_toys_allEras_50GeV_2000T allEras
```

To test iteractively:
```
sh combineScripts/submitSmartToyLimits.sh <datacards> <datacards> HTo2ZdTo2mu2x grid allEras 50.000 100.00 <i>
```

inside `submitSmartToyLimits.sh` the number of toys and the granularity of the grid can be adjusted. The `r` range to run the limits is defined on-the-fly, the parameter `<i>` indicates the point of the grid within this range to do the computation, if omitted, it will run the limit on 100 points equally distributed along the `r` range.

### Read the limits

Once the jobs have finished running, you have to retrieve the results and put them into a `.txt` file that will be used for plotting later on. There are two scripts to be used depending on if the limits were generated with asymptotic or toys.

To wrap the limits results with **asymptotic**:
```
python3 combineScripts/readAsymptoticLimits.py <variable> <model> <limit output directory> <year>
```
where `<var>` can be either `mass` or `ctau` to indicate if the grid of the limits is to derive limits vs mass or lifetime and it should be consistent with the grid of masses/ctaus used to define the datacards and derived the limits. `<model>` indicates the model (`HTo2ZdTo2mu2x`, `BToPhi`, `ScenarioA` or `ScenarioB1`), `<limit output directory>` the absolute path of the dir in which limit results are saved and `<year>` should be `2022`, `2023` or `allEras`.

The limits for **toys** are derived in the same way but using a different script:
```
python3 combineScripts/readToysLimits.py <variable> <model> <limit output directory> <year>
```

Note: Also for toys, if limits were derived on an specific grid of `r`, the results are saved in the form of `.root` files with the r vs CL values. In such cases the needed input ``lim_toys*_HTo2ZdTo2mu2x_m*_ctau*_*.txt`` files will be automatically made by setting `doExtraction = True` inside `readToysLimits.py`.

----

In either case, the output will be a `limits_<model>_<year>.txt` file which would look like:

```
# model,mass,ctau,obs,exp,exp-2s,exp-1s,exp+1s,exp+1s
HTo2ZdTo2mu2x,50.000,0.10,1.5475,1.7500,0.6016,0.9963,3.0614,4.9154
HTo2ZdTo2mu2x,50.000,0.16,1.4674,1.6172,0.6064,0.9618,2.6873,4.0987
HTo2ZdTo2mu2x,50.000,0.25,1.3972,1.5078,0.6125,0.9413,2.3913,3.5396
HTo2ZdTo2mu2x,50.000,0.40,1.3728,1.4844,0.6262,0.9480,2.3127,3.3875
HTo2ZdTo2mu2x,50.000,0.63,1.4396,1.5859,0.6567,0.9979,2.5089,3.7200
HTo2ZdTo2mu2x,50.000,1.00,1.5715,1.7891,0.6849,1.0817,2.9586,4.5290
HTo2ZdTo2mu2x,50.000,1.60,1.7121,2.0000,0.7266,1.1643,3.4509,5.4857
HTo2ZdTo2mu2x,50.000,2.50,1.8220,2.1406,0.7526,1.2189,3.7789,6.1894
HTo2ZdTo2mu2x,50.000,4.00,1.9388,2.2656,0.7788,1.2783,4.0537,6.7787
HTo2ZdTo2mu2x,50.000,6.30,2.0545,2.3594,0.7926,1.3189,4.2779,7.1519
HTo2ZdTo2mu2x,50.000,10.00,2.2162,2.4844,0.8152,1.3759,4.5640,7.5313
HTo2ZdTo2mu2x,50.000,16.00,2.4155,2.6484,0.8483,1.4390,4.9076,8.0289
HTo2ZdTo2mu2x,50.000,25.00,2.6006,2.7812,0.8691,1.4966,5.2202,8.4321
HTo2ZdTo2mu2x,50.000,40.00,2.7898,2.8906,0.8920,1.5322,5.4946,8.7642
HTo2ZdTo2mu2x,50.000,63.00,3.0436,3.0312,0.9236,1.5987,5.8103,9.1910
HTo2ZdTo2mu2x,50.000,100.00,3.3199,3.1719,0.9540,1.6644,6.1304,9.6177
HTo2ZdTo2mu2x,50.000,160.00,3.5303,3.1875,0.9463,1.6642,6.1860,9.6653
HTo2ZdTo2mu2x,50.000,250.00,3.8027,3.2969,0.9788,1.7213,6.4245,9.9972
HTo2ZdTo2mu2x,50.000,400.00,4.1384,3.4531,1.0251,1.8029,6.7290,10.4710
HTo2ZdTo2mu2x,50.000,630.00,4.3749,3.5312,1.0621,1.8530,6.9094,10.7081
HTo2ZdTo2mu2x,50.000,1000.00,4.5887,3.6250,1.0762,1.8926,7.0640,10.9922
```

### Plots the limits

**Input:** The previously created `limits_<model>_<year>.txt` file.

To plot them you run two different scripts depending on if the limits are got vs mass or liftime:
```
python3 combineScripts/plot1DLimits_vsMass.py <model> <limit output directory> <ctau> <year>
```
and
```
python3 combineScripts/plot1DLimits_vsLifetime.py <model> <limit output directory> <mass> <year>
```

Examples:
```
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_HTo2ZdTo2mu2x_NormSmart_Apr-21-2025_vsMass_allEras 1 allEras
python3 combineScripts/plot1DLimits_vsLifetime.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_HTo2ZdTo2mu2x_NormSmart-0p6_May-01-2025_vsCTau_toys_allEras_50GeV_2000T 50.000 allEras
```

which will create the png limit plot.

## Statistics checks

### Bias tests

Running bias tests run for hZdZd model.

1) To run bias tests on a single point:
```
# python3 combineScripts/submitBiasTests.py datacards_all_Oct-19-2024_2022 output /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Sep-30-2024_2022/limits_HTo2ZdTo2mu2x_2022.txt HTo2ZdTo2mu2x 5 5 100
python3 combineScripts/submitBiasTests.py datacards_all_Oct-19-2024_2022 output /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Sep-30-2024_2022/limits_HTo2ZdTo2mu2x_2022.txt HTo2ZdTo2mu2x 5 5 100
```
Injecting $r_{in} = 5$, for $m_{Z_D} = 5$ GeV and $c\tau = 100$ mm.

2) To run over the whole masked grid use condor:
```
# sh condor/limits/runBiasTests_onCondor.sh <input datacards> <output dir> <year> <txt with asymptotic limits> <injected r>
sh condor/limits/runBiasTests_onCondor.sh datacards_all_Oct-20-2024_2022 biasTests_Oct-20-2024_r5 2022 /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Sep-30-2024_2022/limits_HTo2ZdTo2mu2x_2022.txt 5
```

3) To plot results and summary after running with condor. ```<input dir>``` is ```<output dir>``` from previous command.
```
# python3 python/plot_biasTestsSummary.py <input dir>
python3 python/plot_biasTestsSummary.py /ceph/cms/store/user/fernance/Run3ScoutingOutput/biasTests_Oct-20-2024_r5
```

## Running the analysis (start-to-end)

This set of commands assumed that we are **taking the ntuples as starting point** (skimmer and looper should have been run before). Latest sets of ntupels are available here:
```
2022: /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_2022_Feb-05-2024/
2023: /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_2023_May-26-2024/
```

**You may need to setup the environment as described above in the relevant setions**

### Plotting the variables and getting RooDataSets for invariant mass spectra

Init with:
```
source cpp/setup.sh
```

To obtain general plots for 2022 and 2023 you have to run the filler. Cuts are applied automatically, and $m_{\mu\mu}$ spectra are filled in the form of both ```TH1D```'s and a ```RooDataSet```s for each Signal Region (SR):
```
sh condor/runScoutingHistos_onCondor.sh /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_2022_Feb-05-2024 outputHistograms_Jun-14-2024_allCuts
sh condor/runScoutingHistos_onCondor.sh 2023 /ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_2023_May-26-2024/ outputHistograms_Jun-14-2024_allCuts
```

Then run the plotter on the generated outputs e.g.
```
python3 plotHistosScouting.py --inSamples Data Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10mm Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-10mm --inDir /ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_allCuts --logY --outSuffix 2022_allCuts_shape --year 2022 --extraLabelBold "Dimuon" --extraLabel "All cuts" --pdf (--shape)
python3 plotHistosScouting.py --inSamples Data Signal_HTo2ZdTo2mu2x_MZd-2p0_ctau-10mm Signal_HTo2ZdTo2mu2x_MZd-5p0_ctau-10mm Signal_HTo2ZdTo2mu2x_MZd-7p0_ctau-10mm --inDir /ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_allCuts --logY --outSuffix 2023_allCuts_shape --year 2023 --extraLabelBold "Dimuon" --extraLabel "All cuts" --pdf (--shape)
```

If you want to go directly to fitting, you can just fill the spectra and ```RooDataSet```'s in the filling step.


## Draft analysis code with uproot and coffea

This is a draft of some potential analysis code, based on uproot and coffea.
To install on the uaf, run `source bootstrap.sh` (only required once).
Then, `./shell` will start the singularity container.

Inside `scouting/`, run `python minimal.py`.
`
