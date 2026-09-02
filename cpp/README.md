# Looper

## 2022/2023

```bash
source setup.sh
make rootDict   # first time only
make
./main.exe OUTDIR YEAR SAMPLE START_FILE N_FILES [IN_CONDOR] [FROM_CRAB]
```

## 2024 (UAF)

```bash
source setup.sh 2024_el8
make rootDict   # first time only
make
./main.exe OUTDIR YEAR SAMPLE START_FILE N_FILES [IN_CONDOR] [FROM_CRAB]
```

## 2024 Condor

```bash
cd cpp
source setup.sh 2024_el8
make rootDict   # first time only
make
cd ..
export STARTDIR=$(pwd)
export SCOUTINGOUTPUTDIR=<your_output_subdir>
export X509_USER_PROXY=$(voms-proxy-info --path)
bash condor/create_package_2024.sh
condor_submit condor/runScoutingLooper_DQCD_2024_onCondor.sub
```

## Examples

```bash
# 2022 signal (crab/Xrootd)
./main.exe test 2022 Signal_HTo2ZdTo2mu2x_MZd-24p0_ctau-1mm_2022 0 100 0 1

# 2022 BToPhi signal
./main.exe test 2022 Signal_BToPhi_MPhi-2p0_ctau-100mm_2022postEE 0 100 0 1

# 2024 QCD background
./main.exe test 2024 QCD_Bin-PT-30to50_Fil-MuEnriched_2024 0 100
```
