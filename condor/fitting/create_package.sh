#!/bin/bash

#INDIR="datacards_all_Feb-21-2024"

# Start from ScoutingRun3/.
rm tmp_create_package/ -rf
mkdir -p tmp_create_package
cd tmp_create_package
mkdir -p ScoutingRun3
cd ..

cp HiggsAnalysis/ tmp_create_package/ScoutingRun3/. -r # Copy relevant folders
#cp CMSSW_13_3_0 tmp_create_package/ScoutingRun3/. -r # Copy relevant folders
#cp combineScripts tmp_create_package/ScoutingRun3/. -r 
echo "Checking what is inside the package:"
ls tmp_create_package/ScoutingRun3/
echo "Adding final fitting scripts..."
cd tmp_create_package
tar -cf - ../cpp | tar -xf - -C ScoutingRun3/. # Copy cpp folder without the plot folders
ls ScoutingRun3/

tar -chJf package.tar.gz ScoutingRun3

mv package.tar.gz ../.
rm -rf tmp_create_package
