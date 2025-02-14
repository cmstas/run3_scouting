#!/bin/bash

#INDIR="datacards_all_Feb-21-2024"
INDIR=$1

# Start from ScoutingRun3/.
echo "Removing previous package..."
rm tmp_create_package/ -rf
mkdir -p tmp_create_package
cd tmp_create_package
mkdir -p ScoutingRun3
cd ..

echo "Copying HiggsAnalysis inside tmp_create_package..."
cp HiggsAnalysis/ tmp_create_package/ScoutingRun3/. -r # Copy relevant folders
#cd tmp_create_package/ScoutingRun3/
#git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
#pushd HiggsAnalysis/CombinedLimit
#git fetch origin
#git checkout v10.0.2
#cd ../../

#cp CMSSW_13_3_0 tmp_create_package/ScoutingRun3/. -r # Copy relevant folders
#cp combineScripts tmp_create_package/ScoutingRun3/. -r 
echo "Checking what is inside the package:"
ls tmp_create_package/ScoutingRun3/
for INDIR in "$@"; do
    echo "Adding ${INDIR} to package.tar.gz..."
    tar -cf - ${INDIR} | tar -xf - -C tmp_create_package/ScoutingRun3/. # Copy cpp folder without the plot folders
    ls tmp_create_package/ScoutingRun3/
done
echo "Adding final combine scripts..."
cd tmp_create_package
tar -cf - ../combineScripts | tar -xf - -C ScoutingRun3/. # Copy cpp folder without the plot folders
ls ScoutingRun3/

tar -chJf package.tar.gz ScoutingRun3

mv package.tar.gz ../.
rm -rf tmp_create_package
