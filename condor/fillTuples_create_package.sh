#!/bin/bash

set -e

rm -rf tmp_create_package_fillTuples
mkdir -p tmp_create_package_fillTuples/ScoutingRun3

cp fillTuplesScouting.py tmp_create_package_fillTuples/ScoutingRun3/.
cp -r utils tmp_create_package_fillTuples/ScoutingRun3/.
cp -r data  tmp_create_package_fillTuples/ScoutingRun3/.

cd tmp_create_package_fillTuples
tar -chzf package_fillTuples.tar.gz ScoutingRun3
mv package_fillTuples.tar.gz ../.
cd ..
rm -rf tmp_create_package_fillTuples

echo "Created package_fillTuples.tar.gz ($(du -h package_fillTuples.tar.gz | cut -f1))"
