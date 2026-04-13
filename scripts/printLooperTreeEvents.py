import os
import ROOT

# Directorio con tus ROOT files
input_dir = "/ceph/cms/store/user/fernance/Run3ScoutingOutput/looperOutput_Sep-10-2025_2022_BToPhi/"

for fname in os.listdir(input_dir):
    if not fname.endswith(".root"):
        continue
    fpath = os.path.join(input_dir, fname)
    f = ROOT.TFile.Open(fpath)
    if not f or f.IsZombie():
        print(f"Not possible to open {fname}")
        continue

    tree = f.Get("tout")
    if not tree:
        print(f"No 'tout'in {fname}")
        f.Close()
        continue

    nentries = tree.GetEntries()
    print(f"{fname}: {nentries} events")

    f.Close()
