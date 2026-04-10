#!/bin/bash

export X509_USER_PROXY=$(voms-proxy-info -path)

usage()
{
    echo "Usage:"
    echo ""
    echo "  sh condor/limits/runLimits_onCondor.sh [datacards] [output] [era/year] [type]"
    echo ""
    echo "The output_dir will be created in /ceph/cms/store/user/$USER/Run3ScoutingOutput/"
    echo "Control the jobs to be run by editing the corresponding runLimits_onCondor.sub"
    echo "Options:"
    echo "-> [datacards]  e.g.  datacards_HTo2ZdTo2mu2x_Norm0.01_standard_Apr-15-2025_allEras"
    echo "-> [output]     e.g.  limits_Apr-15-2025_HTo2ZdTo2mu2x_Norm0p01_vsMass_allEras"
    echo "-> [era/year]   e.g.  allEras"
    echo "-> [type]       e.g.  HTo2ZdTo2mu2x_mass_asymptotic"
    echo ""
    exit
}

if [ -z $1 ]; then usage; fi

export SCOUTINGSNTINPUTDIRLIM=$1
export SCOUTINGSNTOUTPUTDIRLIM=$2
export PERIOD=$3
export HOMEDIR=$PWD
export LABEL=$(basename $SCOUTINGSNTOUTPUTDIRLIM)
#export TYPE=$4

#MODEL="BToPhi"
#allmasses=("2.000_M0.670" "4.000_M1.330")
#allmasses=("1.000_M0.330" "2.000_M0.670" "4.000_M1.330" "5.000_M1.670" "7.500_M2.500" "6.000_M2.000" "12.000_M1.200")
#allctaus=(0.10 0.25 0.60 1.00 2.50 6.00 10.00 25.00 60.00 100.00)

MODEL="BToPhi"
allctaus=(1.00 10.00 100.00)
#allmasses=(0.304 0.308 0.314 0.322 0.328 0.338 0.346 0.352 0.358 0.362 0.366 0.370 0.375 0.655 0.670 1.190 1.260 1.280 1.300 1.320 1.340 1.360 1.390 1.410 1.450 1.490 1.530 1.550 1.570 1.590 1.620 1.640 1.660 1.680 1.700 1.730 1.760 1.790 1.820 1.840 1.860 1.880 1.900 1.950 1.980 2.020 2.160 2.220 2.360 2.400 2.460 2.520 2.580)
allmasses=(4.300 4.360 4.440 4.520 4.600)


mkdir tmp_merged

for mass in ${allmasses[@]}
do
    for ctau in ${allctaus[@]}
    do
        eval "hadd tmp_merged/merged_${MODEL}_M${mass}_ctau${ctau}.root /ceph/cms/store/user/$USER/Run3ScoutingOutput/${SCOUTINGSNTOUTPUTDIRLIM}/higgsCombine_grid_${MODEL}_M${mass}_ctau${ctau}.POINT*.HybridNew.mH125.root"
    done
done

echo "Creating dirs..."
mkdir -p condor/limits/limits_logs

echo "Preparing to create package..."
sh condor/limits/create_package.sh $SCOUTINGSNTINPUTDIRLIM tmp_merged
mv package.tar.gz package_${LABEL}_wp.tar.gz

## Submission files to try extract limits on different subsets of signal samples


#### Masses for Scenario B1
#for mass in ${allmasses[@]}
#do
#    export MASS="${mass}"
#    #condor_submit condor/limits/runWrapper_ScenarioB1_CTauGrid_onCondor.sub
#    condor_submit condor/limits/runWrapper_ScenarioA_CTauGrid_onCondor.sub
#done

condor_submit condor/limits/runWrapper_BToPhi_MassGrid_1mm_onCondor.sub
condor_submit condor/limits/runWrapper_BToPhi_MassGrid_10mm_onCondor.sub
condor_submit condor/limits/runWrapper_BToPhi_MassGrid_100mm_onCondor.sub
