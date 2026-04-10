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

echo "Creating dirs..."
mkdir -p condor/limits/limits_logs
mkdir -p /ceph/cms/store/user/$USER/Run3ScoutingOutput/$SCOUTINGSNTOUTPUTDIRLIM

echo "Preparing to create package..."
sh condor/limits/create_package.sh $SCOUTINGSNTINPUTDIRLIM
mv package.tar.gz package_${LABEL}.tar.gz

## Submission files to try extract limits on different subsets of signal samples

#allmasses=(50.000)
#allCTaus=(0.10 0.16 0.25 0.40 0.63 1.00 1.60 2.50 4.00 6.30 10.00 16.00 25.00 40.00 63.00 100.00 160.00 250.00 400.00 630.00 1000.00)
#allCTaus=(0.10 0.16 0.25 0.40 0.63 1.00)
#allCTaus=(0.10 0.16)

### Preview: For general grid initial testing
#allmasses=(50.000)
#allCTaus=(0.10 0.16 0.25 0.40 0.63 1.00 1.60 2.50 4.00 6.30 10.00 16.00 25.00 40.00 63.00 100.00 160.00 250.00 400.00 630.00 1000.00)
#for m in ${allmasses[@]}
#do
#    for t in ${allCTaus[@]}
#    do
#        export MASS="${m}"
#        export CTAU="${t}"
#        condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_generalGrid_onCondor.sub
#    done
#done

#### CTau Grid
#allmasses=(1.500 5.000 20.000 30.000 40.000 50.000)
allmasses=(1.250 1.500 2.000)
#allmasses=(2.000)
for m in ${allmasses[@]}
do
    export MASS="${m}"
    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_CTauGrid_onCondor.sub
    condor_submit condor/limits/runLimits_BToPhi_CTauGrid_onCondor.sub
done

#### Mass grid (1 mm)
#allrs=(0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100)
#for r in ${allrs[@]}
#do
#    export IMIN="${r}"
#    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_MassGrid_1mm_onCondor.sub
#    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_MassGrid_10mm_onCondor.sub
#    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_MassGrid_100mm_onCondor.sub
#    #condor_submit condor/limits/runLimits_HTo2ZdTo2mu2x_MassGrid_1000mm_onCondor.sub
#    #condor_submit condor/limits/runLimits_ScenarioA_MassGrid_CTauGrid_onCondor.sub
#    #condor_submit condor/limits/runLimits_BToPhi_vsMass_1mm_Grid_onCondor.sub
#    #condor_submit condor/limits/runLimits_ScenarioB1_CTauGrid_onCondor.sub
#    condor_submit condor/limits/runLimits_ScenarioA_CTauGrid_onCondor.sub
#    #condor_submit condor/limits/runLimits_BToPhi_vsMass_10mm_Grid_onCondor.sub
#    #condor_submit condor/limits/runLimits_BToPhi_vsMass_100mm_Grid_onCondor.sub
#    #
#    #allCTaus=("1.00" "10.00" "100.00")
#    #for ctau_value in ${allCTaus[@]}
#    #do
#    #    export CTAU="${ctau_value}"
#    #    condor_submit condor/limits/runLimits_BToPhi_vsMass_Grid_onCondor.sub
#    #done
#done
