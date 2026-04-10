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
export TYPE=$4

echo "Creating dirs..."
mkdir -p condor/limits/limits_logs
mkdir -p /ceph/cms/store/user/$USER/Run3ScoutingOutput/$SCOUTINGSNTOUTPUTDIRLIM

echo "Preparing to create package..."
sh condor/limits/create_package.sh $SCOUTINGSNTINPUTDIRLIM
mv package.tar.gz package_${LABEL}.tar.gz

## Submission files to try extract limits on different subsets of signal samples
if [ ${TYPE} == "HTo2ZdTo2mu2x_mass_asymptotic" ]
then
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_Asymptotic_onCondor.sub
elif [ ${TYPE} == "HTo2ZdTo2mu2x_mass_toys" ]
then
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_ToysObs_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_ToysExp_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_ToysEm1_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_ToysEp1_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_ToysEm2_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsMass_ToysEp2_onCondor.sub
elif [ ${TYPE} == "HTo2ZdTo2mu2x_ctau_asymptotic" ]
then
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_Asymptotic_onCondor.sub
elif [ ${TYPE} == "HTo2ZdTo2mu2x_ctau_toys" ]
then
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysObs_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysExp_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEm1_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEp1_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEm2_onCondor.sub
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEp2_onCondor.sub
elif [ ${TYPE} == "HTo2ZdTo2mu2x_ctau_toys_test" ]
then
    condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_grid_onCondor_Test.sub
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysObs_onCondor_Test.sub
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysExp_onCondor_Test.sub
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEm1_onCondor_Test.sub
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEp1_onCondor_Test.sub
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEm2_onCondor_Test.sub
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_vsCTau_ToysEp2_onCondor_Test.sub
elif [ ${TYPE} == "BToPhi_mass_asymptotic" ]
then
    #condor_submit condor/limits/runLimits_BToPhi_vsMass_1mm_Asymptotic_onCondor.sub
    condor_submit condor/limits/runLimits_BToPhi_vsMass_10mm_Asymptotic_onCondor.sub
    #condor_submit condor/limits/runLimits_BToPhi_vsMass_100mm_Asymptotic_onCondor.sub
else
    echo "The type of limit was not specified -> Aborting submission..."
fi
#condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_onCondor.sub   # Mass grid for HTo2ZdTo2mu2x
#condor_submit condor/limits/runLimits_BToPhi_onCondor.sub          # Mass grid for BToPhi
#condor_submit condor/limits/runLimits_BToPhi_SignalMC_onCondor.sub
#condor_submit condor/limits/runLimits_ScenarioA_SignalMC_onCondor.sub
#condor_submit condor/limits/runLimits_ScenarioB1_SignalMC_onCondor.sub
#condor_submit condor/limits/runLimits_reweighting_limited_onCondor.sub
#condor_submit condor/limits/runLimits_reweightingValidation_onCondor.sub
#condor_submit condor/limits/runLimits_limited_onCondor.sub
