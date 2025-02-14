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

To run a set of fits just run:
```
cmssw-el8 --bind /ceph/cms/store/
cd CMSSW_13_3_0/src
cmsenv
cd ../../
root -b -q -l -n cpp/doAll_fitDimuonMass.C
```

**Remember to properly set the period and input paths inside before running**

## Limit extraction

### Combine in condor

Then launch with condor with:
```
sh condor/limits/runLimits_onCondor.sh <datacard directory> <limit output directory> <year>
```
model and other parameters are specified in the corresponding .sub file.

To wrap the limits results:
```
python3 combineScripts/readAsymptoticLimits.py <model> <limit output directory> <year>
```
which will create a txt file with the relevant upper limits in the previous limit output directory.

To plot them:
```
python3 combineScripts/plot1DLimits.py <model> <limit output directory> <ctau> <year>
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

### Fitting mass windows

Follow the steps above to run the fitting within a cmssw-el8 env.

To fit the mass windows, modify the lines within ```cpp/doAll_fitDimuonMass.C``` to define ```period``` and ```inDir```. With the examples below:
```
2022: period=2022, inDir=/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_allCuts
2023: period=2023, inDir=/ceph/cms/store/user/fernance/Run3ScoutingOutput/outputHistograms_Jun-14-2024_allCuts
```

Then run once for each period:
```
root -b -q -l -n cpp/doAll_fitDimuonMass.C
```
Which will create ```fitResults_2022``` and ```fitResults_2023```.

### Make datacards

```
python3 make_datacards.py 2022
python3 make_datacards.py 2023
```

### Limit extraction

Make sure you have followed the steps for setup in #{combine-in-condor} and
```
sh condor/limits/runLimits_onCondor.sh datacards_all_Jun-14-2024_2022 limits_Jun-14-2024_2022 2022
sh condor/limits/runLimits_onCondor.sh datacards_all_Jun-14-2024_2023 limits_Jun-14-2024_2023 2023
```

Then, for extracting the result in the output directories:
```
python3 combineScripts/readAsymptoticLimits.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2022 2022
python3 combineScripts/readAsymptoticLimits.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2023 2023
```

And finally for plotting (may be needed to change options in the script):
```
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2022 1 2022
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2022 10 2022
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2022 100 2022
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2023 1 2023
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2023 10 2023
python3 combineScripts/plot1DLimits_vsMass.py HTo2ZdTo2mu2x /ceph/cms/store/user/fernance/Run3ScoutingOutput/limits_Jun-14-2024_2023 100 2023
```

## Draft analysis code with uproot and coffea

This is a draft of some potential analysis code, based on uproot and coffea.
To install on the uaf, run `source bootstrap.sh` (only required once).
Then, `./shell` will start the singularity container.

Inside `scouting/`, run `python minimal.py`.
`
