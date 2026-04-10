#!/bin/bash
cd /ruta/a/tu/CMSSW_X_Y_Z/src
eval `scramv1 runtime -sh`
source venv_root/bin/activate
exec python3 "$@
