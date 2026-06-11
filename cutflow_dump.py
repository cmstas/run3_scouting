#!/usr/bin/env python3

import argparse
import glob
import os
import re
from pathlib import Path

import uproot

_HERE = Path(__file__).resolve().parent

# cutflow bin index (0-based for uproot .values()) -> label, in logical order
CUTFLOW_STAGES = [
    (0, "generated"),
    (2, "goodRun"),
    (3, "noDuplicate"),
    (4, "fraction"),
    (5, "L1"),
    (6, "HLT"),
    (7, "preMu"),
    (1, "saved"),
]


def _looper_core(fname):
    """output_<core>_<range>.root -> <core> (the sample identifier)."""
    base = os.path.basename(fname)
    base = re.sub(r"^output_", "", base)
    base = re.sub(r"_\d+To\d+\.root$", "", base)
    return base


def _sum_hist(looper_files, name):
    """Sum bin contents of histogram `name` across a list of files."""
    total = None
    for f in looper_files:
        with uproot.open(f) as fh:
            if name not in fh:
                continue
            vals = fh[name].values()
            total = vals.copy() if total is None else total + vals
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", choices=["signal", "qcd"], default="signal",
                    help="Which samples to summarize.")
    ap.add_argument("--looper-dir", nargs="+",
                    default=["/ceph/cms/store/group/Run3Scouting/looperOutput_Jun8_2026_noL1"],
                    help="Directories holding looper output_*.root files.")
    ap.add_argument("--tuples-dir", default="tuples_parking_nochi2",
                    help="Directory holding the flat tuples_*.root files.")
    args = ap.parse_args()

    tag = "Signal" if args.kind == "signal" else "QCD"
    tuples_dir = (_HERE / args.tuples_dir) if not os.path.isabs(args.tuples_dir) else Path(args.tuples_dir)

    # Index every looper output by its sample core
    looper_by_core = {}
    for d in args.looper_dir:
        d = (_HERE / d) if not os.path.isabs(d) else Path(d)
        for f in glob.glob(str(d / f"output_*{tag}*_*To*.root")):
            looper_by_core.setdefault(_looper_core(f), []).append(f)

    tuple_files = sorted(glob.glob(str(tuples_dir / f"tuples_*{tag}*.root")))
    if not tuple_files:
        print(f"No tuples matching '*{tag}*' in {tuples_dir}")
        return

    hdr = (f'{"sample":<52} {"generated":>12} {"HLT":>11} '
           f'{">=1 SV (tuple)":>15} {"eff[%]":>8}')
    print(hdr)
    print("-" * len(hdr))

    for tup in tuple_files:
        core = re.sub(r"^tuples_", "", os.path.basename(tup))
        core = re.sub(r"\.root$", "", core)
        looper_files = looper_by_core.get(core, [])

        n_tuple = uproot.open(tup)["tuples"].num_entries

        cutflow = _sum_hist(looper_files, "cutflow") if looper_files else None
        if cutflow is None:
            short = core.replace("Signal_ScenarioA_Par_2024_", "").replace("_Fil-MuEnriched", "")
            why = "(no cutflow histo)" if looper_files else "(no looper file)"
            print(f"{short:<52} {why:>12} "
                  f"{'-':>11} {n_tuple:>15d} {'-':>8}")
            continue

        n_gen = cutflow[0]
        n_hlt = cutflow[6]
        eff = 100.0 * n_tuple / n_gen if n_gen > 0 else float("nan")

        short = core.replace("Signal_ScenarioA_Par_2024_", "").replace("_Fil-MuEnriched", "")
        print(f"{short:<52} {n_gen:>12.0f} {n_hlt:>11.0f} "
              f"{n_tuple:>15d} {eff:>8.3f}")


if __name__ == "__main__":
    main()
