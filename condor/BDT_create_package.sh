#!/bin/bash


#ScoutingRun3/BDT/workingpoint.py   (uses _HERE.parent / "tuples_parking_nochi2")

set -e

rm -rf tmp_create_package_BDT
mkdir -p tmp_create_package_BDT/ScoutingRun3/BDT

# Ship the BDT python sources only
cp BDT/*.py tmp_create_package_BDT/ScoutingRun3/BDT/.

cd tmp_create_package_BDT
tar -chzf package_BDT.tar.gz ScoutingRun3
mv package_BDT.tar.gz ../.
cd ..
rm -rf tmp_create_package_BDT

echo "Created package_BDT.tar.gz ($(du -h package_BDT.tar.gz | cut -f1))"
