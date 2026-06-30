#!/bin/bash

# Packages the BDT python code (code only, ~tiny) into package_BDT.tar.gz.
# The 5.6 GB input tuples (tuples_parking_nochi2/) are NOT tarred here -- they are
# transferred directly by HTCondor (see BDT_onCondor.sub) to avoid
# re-tarring several GB of already-compressed ROOT files on every submit.
#
# Layout inside the tarball matches what workingpoint.py expects:
#   ScoutingRun3/BDT/workingpoint.py   (uses _HERE.parent / "tuples_parking_nochi2")

set -e

rm -rf tmp_create_package_BDT
mkdir -p tmp_create_package_BDT/ScoutingRun3/BDT

# Ship the BDT python sources only (exclude bulky/transient output dirs).
cp BDT/*.py tmp_create_package_BDT/ScoutingRun3/BDT/.

cd tmp_create_package_BDT
tar -chzf package_BDT.tar.gz ScoutingRun3
mv package_BDT.tar.gz ../.
cd ..
rm -rf tmp_create_package_BDT

echo "Created package_BDT.tar.gz ($(du -h package_BDT.tar.gz | cut -f1))"
