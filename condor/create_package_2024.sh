#!/bin/bash

# Must be run after: source cpp/setup.sh 2024
# Compiles the looper under el9_amd64_gcc12/CMSSW_15_0_2 and creates package.tar.gz

cd cpp
make
cd ..

rm -rf tmp_create_package
mkdir -p tmp_create_package
cd tmp_create_package

mkdir -p ScoutingRun3
cp ../*.py ../data ../utils ScoutingRun3/. -r
tar -cf - --exclude=temp_data* ../cpp | tar -xf - -C ScoutingRun3/.
tar -chJf package.tar.gz ScoutingRun3
mv package.tar.gz ../.
