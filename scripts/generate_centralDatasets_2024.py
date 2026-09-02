#!/usr/bin/env python3
"""
Generate centralDatasets.txt entries for 2024 signal and background samples.
Reads directory listings from UCSD xrootd and appends entries to cpp/input/centralDatasets.txt.
Run once after crab jobs complete.
"""
import subprocess
import re
import sys

REDIRECTOR  = "redirector.t2.ucsd.edu:1095"
SIG_BASE    = "/store/group/Run3Scouting/RAWScouting_DQCD_sig2024_v_dqcd_2024"
BKG_BASE    = "/store/group/Run3Scouting/RAWScouting_DQCD_bkg2024_v_dqcd_2024"
OUTPUT_FILE = "../cpp/input/centralDatasets.txt"

def xrdfs_ls(path):
    result = subprocess.run(
        ["xrdfs", REDIRECTOR, "ls", path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR listing {path}: {result.stderr.strip()}", file=sys.stderr)
        return []
    return [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]

entries = []

# --- Signal ---
for path in xrdfs_ls(SIG_BASE):
    dirname = path.split('/')[-1]
    # GluGluHToDarkShowers-{Scenario}-ctau-{ctau}-mA-{mA}-mpi-{mpi}_TuneCP5_...
    m = re.match(r'GluGluHToDarkShowers-(\w+_Par)-ctau-(\w+)-mA-(\w+)-mpi-(\d+)_TuneCP5_', dirname)
    if not m:
        print(f"Skipping unrecognised signal dir: {dirname}", file=sys.stderr)
        continue
    scenario, ctau, mA, mpi = m.group(1), m.group(2), m.group(3), m.group(4)
    sample_name = f"Signal_{scenario}_2024_mpi-{mpi}_mA-{mA}_ctau-{ctau}mm"
    entries.append((sample_name, path))

# --- Background ---
for path in xrdfs_ls(BKG_BASE):
    dirname = path.split('/')[-1]
    # QCD_Bin-PT-{range}_Fil-MuEnriched_TuneCP5_...
    m = re.match(r'(QCD_Bin-PT-[\w]+_Fil-MuEnriched)_TuneCP5_', dirname)
    if not m:
        print(f"Skipping unrecognised background dir: {dirname}", file=sys.stderr)
        continue
    sample_name = f"{m.group(1)}_2024"
    entries.append((sample_name, path))

if not entries:
    print("No entries generated — check xrootd connectivity and proxy.", file=sys.stderr)
    sys.exit(1)

# Check for duplicates against existing file
existing = set()
try:
    with open(OUTPUT_FILE, 'r') as f:
        for line in f:
            name = line.split(',')[0].strip()
            if name:
                existing.add(name)
except FileNotFoundError:
    pass

new_entries = [(n, p) for n, p in entries if n not in existing]
skipped     = len(entries) - len(new_entries)

with open(OUTPUT_FILE, 'a') as f:
    for name, path in sorted(new_entries):
        f.write(f"{name},{path}\n")

print(f"Added {len(new_entries)} entries to {OUTPUT_FILE} ({skipped} already present, skipped).")
