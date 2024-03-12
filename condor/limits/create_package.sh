#!/bin/bash

#INDIR="datacards_all_Feb-21-2024"
INDIR=$1

# Start from ScoutingRun3/.
rm tmp_create_package/ -rf
mkdir -p tmp_create_package
cd tmp_create_package
mkdir -p ScoutingRun3

cp ../HiggsAnalysis/ ScoutingRun3/. -r # Copy relevant folders
#cp CMSSW_12_6_0 tmp_create_package/ScoutingRun3/. -r # Copy relevant folders
#cp combineScripts tmp_create_package/ScoutingRun3/. -r 
tar -cf - ../combineScripts ../${INDIR} ../fitResults | tar -xf - -C ScoutingRun3/. # Copy cpp folder without the plot folders

tar -chJf package.tar.gz ScoutingRun3

mv package.tar.gz ../.
rm -rf tmp_create_package
