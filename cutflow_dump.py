#!/usr/bin/env python3

import argparse
import glob
import os
import re
from pathlib import Path

import numpy as np
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


def _tuple_chi2_keep(tup, thresholds):
    """Count tuple events whose best used SV passes chi2/ndof < thr.

    Operates on the flat tuple, which already encodes the full preselection
    (incl. the current SV chi2/ndof < 10 cut). An event is kept if its SV1, or a
    filled SV2 (SV2_x != -1), has chi2/ndof below the threshold. So at thr=10 the
    count equals the tuple entry count, and at a tighter thr it is the nested
    survivor count. Returns {thr: n_kept}.
    """
    arrs = uproot.open(tup)["tuples"].arrays(
        ["SV1_chi2Ndof", "SV2_chi2Ndof", "SV2_x"], library="np")
    c1 = arrs["SV1_chi2Ndof"]
    c2 = arrs["SV2_chi2Ndof"]
    sv2_filled = arrs["SV2_x"] != -1.0
    counts = {}
    for thr in thresholds:
        keep = (c1 < thr) | (sv2_filled & (c2 < thr))
        counts[thr] = int(keep.sum())
    return counts


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
    ap.add_argument("--chi2-loose", type=float, default=10.0,
                    help="Current SV chi2/ndof cut (events with >=1 SV below this).")
    ap.add_argument("--chi2-tight", type=float, default=3.0,
                    help="Tightened SV chi2/ndof cut to compare against.")
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

    c_lo, c_hi = args.chi2_loose, args.chi2_tight
    lo_lbl = f"chi2<{c_lo:g}"
    hi_lbl = f"chi2<{c_hi:g}"
    hdr = (f'{"sample":<52} {"generated":>12} {"HLT":>11} '
           f'{">=1 SV (tuple)":>15} {"eff[%]":>8} '
           f'{lo_lbl:>10} {hi_lbl:>10} {"lost":>7} {"loss[%]":>8}')
    print(hdr)
    print("-" * len(hdr))

    tot_lo = tot_hi = 0
    for tup in tuple_files:
        core = re.sub(r"^tuples_", "", os.path.basename(tup))
        core = re.sub(r"\.root$", "", core)
        looper_files = looper_by_core.get(core, [])

        n_tuple = uproot.open(tup)["tuples"].num_entries

        # Nested chi2 comparison, computed from the tuple's own SV branches.
        keep = _tuple_chi2_keep(tup, [c_lo, c_hi])
        n_lo, n_hi = keep[c_lo], keep[c_hi]
        tot_lo += n_lo
        tot_hi += n_hi
        lost = n_lo - n_hi
        loss = 100.0 * lost / n_lo if n_lo > 0 else float("nan")
        short = core.replace("Signal_ScenarioA_Par_2024_", "").replace("_Fil-MuEnriched", "")

        cutflow = _sum_hist(looper_files, "cutflow") if looper_files else None
        if cutflow is None:
            why = "(no cutflow histo)" if looper_files else "(no looper file)"
            print(f"{short:<52} {why:>12} "
                  f"{'-':>11} {n_tuple:>15d} {'-':>8} "
                  f"{n_lo:>10d} {n_hi:>10d} {lost:>7d} {loss:>8.2f}")
            continue

        n_gen = cutflow[0]
        n_hlt = cutflow[6]
        eff = 100.0 * n_tuple / n_gen if n_gen > 0 else float("nan")

        print(f"{short:<52} {n_gen:>12.0f} {n_hlt:>11.0f} "
              f"{n_tuple:>15d} {eff:>8.3f} "
              f"{n_lo:>10d} {n_hi:>10d} {lost:>7d} {loss:>8.2f}")

    if tot_lo > 0:
        tot_lost = tot_lo - tot_hi
        tot_loss = 100.0 * tot_lost / tot_lo
        print("-" * len(hdr))
        print(f"{'TOTAL':<52} {'':>12} {'':>11} {'':>15} {'':>8} "
              f"{tot_lo:>10d} {tot_hi:>10d} {tot_lost:>7d} {tot_loss:>8.2f}")


if __name__ == "__main__":
    main()
