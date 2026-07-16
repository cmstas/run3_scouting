#!/usr/bin/env python3
"""Working point analysis for the scouting BDT.

Trains the global BDT, finds the BDT score threshold at a configurable
background rejection target, then plots input variable distributions for
events passing the working point cut (signal vs background).

Usage:
    python BDT/workingpoint.py
"""

import argparse
import gc
import glob
import re
import uproot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import mplhep as hep
import numpy as np
import pandas as pd
import os
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score
from scipy.stats import norm
from xgboost import XGBClassifier

hep.style.use("CMS")
plt.rcParams.update({
    "font.size":             13,
    "axes.labelsize":        13,
    "axes.titlesize":        13,
    "xtick.labelsize":       11,
    "ytick.labelsize":       11,
    "legend.fontsize":       9,
    "legend.title_fontsize": 10,
    "axes.linewidth":        1.0,
    "xtick.major.size":      5,
    "ytick.major.size":      5,
    "xtick.minor.size":      3,
    "ytick.minor.size":      3,
    "xtick.major.width":     0.9,
    "ytick.major.width":     0.9,
})

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
_parser = argparse.ArgumentParser(description="Working point analysis for the scouting BDT.")
_parser.add_argument("--model-tag", default="A", help="Signal scenario tag for output naming.")
_parser.add_argument("--conditional", action=argparse.BooleanOptionalAction, default=False,
                     help="Train a parametric (conditional) BDT with the signal mass point "
                          "(param_ctau, param_mA, param_mpi) as extra inputs. Background is "
                          "replicated once per signal point, as in BDT_training.py.")
_parser.add_argument("--table", action=argparse.BooleanOptionalAction, default=True,
                     help="Build the Asimov significance table: for a set of target FPRs, "
                          "find the BDT threshold at which the xsec-weighted SV-selected QCD "
                          "has that FPR, then tabulate p0 = 1 - Phi(Z) (with Z) per signal w"
                          "point. Writes .tex per (mpi, mA). "
                          "Default: on; pass --no-table to skip.")
_parser.add_argument("--fpr-targets", type=float, nargs="+", default=[1e-1, 1e-2, 1e-3, 1e-4],
                     help="Target false-positive rates (rows of the --table output).")
_parser.add_argument("--mass-window-gev", type=float, default=1.0,
                     help="ABSOLUTE SV1 dimuon mass window half-width in GeV. Used only when "
                          "--mass-window-rel is 0. Signal and background yields are counted "
                          "within [mA - W, mA + W] around the nominal signal mass mA. "
                          "Set both this and --mass-window-rel to 0 to disable (full mass range).")
_parser.add_argument("--mass-window-rel", type=float, default=0.1,
                     help="RELATIVE (mass-dependent) SV1 dimuon mass window half-width, as a "
                          "fraction of mA: the window is [mA*(1-r), mA*(1+r)]. Takes precedence "
                          "over --mass-window-gev when > 0 (default r = 0.1 = +/-10%% of mA). "
                          "Set to 0 to fall back to the absolute --mass-window-gev window.")
_parser.add_argument("--bkg", choices=["minbias", "qcd", "both"], default="minbias",
                     help="Which background(s) to run. One shared BDT is trained on the "
                          "selected background(s). Output files are suffixed _minBias, _QCD, "
                          "or _both. In 'both' mode the significance-vs-ctau and shape plots "
                          "overlay MinBias and QCD as separate lines (ROC/discriminant remain "
                          "single-line, from the shared BDT).")
_parser.add_argument("--tuples-dir", default="tuples_parking_nochi2",
                     help="Name of the tuple directory under the repo root. Use "
                          "'tuples_L1_info' for the re-filled (unskimmed, collection-OR) tuples "
                          "that carry the 'passL1' branch; pair it with --require-l1.")
_parser.add_argument("--require-l1", action=argparse.BooleanOptionalAction, default=False,
                     help="Keep only events with passL1 != 0 (the L1-seed decision), applied to "
                          "BOTH signal and background right after loading -- i.e. fold the L1 "
                          "trigger efficiency into every yield/efficiency. Requires tuples with a "
                          "'passL1' branch (see --tuples-dir tuples_L1_info). Outputs go to a "
                          "separate 'significance_plots_L1req/' tree so they don't clobber the "
                          "no-L1 results.")
_args = _parser.parse_args()

use_conditional      = _args.conditional
model_tag            = _args.model_tag
MASS_WINDOW_GEV      = _args.mass_window_gev  # absolute SV1 mass window half-width [GeV] around mA
MASS_WINDOW_REL      = _args.mass_window_rel  # relative half-width (fraction of mA); takes precedence
MASS_WINDOW_ACTIVE   = bool((MASS_WINDOW_REL and MASS_WINDOW_REL > 0.0) or
                            (MASS_WINDOW_GEV and MASS_WINDOW_GEV > 0.0))
REQUIRE_L1           = _args.require_l1        # keep only passL1 != 0 events (sig + bkg)
TUPLES_SUBDIR        = _args.tuples_dir        # tuple directory name under the repo root
# The tuples_L1_info re-fill is UNSKIMMED (full filled tuple), whereas the parking_nochi2
# MinBias is the 1/6 skim; the MinBias BKG_FRACTION skim factor is dropped accordingly.
MINBIAS_UNSKIMMED    = ("tuples_L1_info" in TUPLES_SUBDIR)

def _mass_window_halfwidth(mA):
    """SV1 dimuon mass window half-width around mA [GeV].
    Relative (mass-dependent) window takes precedence; else absolute; else None."""
    if MASS_WINDOW_REL and MASS_WINDOW_REL > 0.0:
        return MASS_WINDOW_REL * mA
    if MASS_WINDOW_GEV and MASS_WINDOW_GEV > 0.0:
        return MASS_WINDOW_GEV
    return None

def _win_label_str():
    """LaTeX label describing the active mass window, or '' if disabled."""
    if MASS_WINDOW_REL and MASS_WINDOW_REL > 0.0:
        return rf'$|m_{{\mu\mu}}-m_A|<{MASS_WINDOW_REL:g}\,m_A$'
    if MASS_WINDOW_GEV and MASS_WINDOW_GEV > 0.0:
        return rf'$|m_{{\mu\mu}}-m_A|<{MASS_WINDOW_GEV:g}$ GeV'
    return ''

LUMI_FB = 109.95 # 2024 Luminosity [fb^-1]
SIG_XSEC_PB = 0.439


SIG_NGEN = {
    (10.0, 1.0,  0.1):   997140,
    (10.0, 1.0,  1.0):   999293,
    (10.0, 1.0,  10.0):  980749,
    (10.0, 1.0,  100.0): 954880,
    (4.0,  1.33, 0.1):   987256,
    (4.0,  1.33, 1.0):   932645,
    (4.0,  1.33, 10.0):  978670,
    (4.0,  1.33, 100.0): 951079,
    (4.0,  0.40, 0.1):   903440,
    (4.0,  0.40, 1.0):   998576,
    (4.0,  0.40, 10.0):  952631,
    (4.0,  0.40, 100.0): 997861,
    (1.0,  0.33, 0.1):   916220,
    (1.0,  0.33, 1.0):   955918,
    (1.0,  0.33, 10.0):  934864,
    (1.0,  0.33, 100.0): 998564,
}


BR_A_MUMU = {
    (1.0,  0.33): 0.464,   # 0.458/0.988
    (4.0,  0.40): 0.440,   # 0.436/0.992
    (2.0,  0.67): 0.193,   # not in current tuples
    (10.0, 1.00): 0.307,   # 0.293/0.95343
    (4.0,  1.33): 0.317,   # 0.305/0.9623
}

# Trigger label shown in the significance-plot header.
TRIGGER_LABEL = "Scouting Asymptotic Significance"

# Cut-and-count operating points are auto-loaded from BDT/cnc_tables/ further below
# (CNC_POINTS is built by _load_cnc_fullrange_points once the parser helpers exist).
# Nothing is hand-typed: run `python3 BDT/cutncount.py --bkg {qcd,minbias}` to (re)generate
# the tables, and both the full-range and per-lxy points are read straight from them.

MINBIAS_FILES = [
    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root",
]

QCD_FILES = [
    "tuples_QCD_Bin-PT-15to20_Fil-MuEnriched_2024_2024.root",
    #"tuples_QCD_Bin-PT-20to30_Fil-MuEnriched_2024_2024.root", #ZOMBIE FILE
    "tuples_QCD_Bin-PT-30to50_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-50to80_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-80to120_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-120to170_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-170to300_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-300to470_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-470to600_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-600to800_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-800to1000_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-1000_Fil-MuEnriched_2024_2024.root",
]

# Background cross sections [pb] (https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=%2FQCD_*MuEnriched*%2F*Summer24MiniAODv6*%2FMINIAODSIM)
BKG_XSEC = {
    "tuples_QCD_Bin-PT-15to20_Fil-MuEnriched_2024_2024.root":    3018000.0,
    #"tuples_QCD_Bin-PT-20to30_Fil-MuEnriched_2024_2024.root":    2701000.0, #ZOMBIE (for now)
    "tuples_QCD_Bin-PT-30to50_Fil-MuEnriched_2024_2024.root":    1461000.0,
    "tuples_QCD_Bin-PT-50to80_Fil-MuEnriched_2024_2024.root":    407600.0,
    "tuples_QCD_Bin-PT-80to120_Fil-MuEnriched_2024_2024.root":   96070.0,
    "tuples_QCD_Bin-PT-120to170_Fil-MuEnriched_2024_2024.root":  23140.0,
    "tuples_QCD_Bin-PT-170to300_Fil-MuEnriched_2024_2024.root":  7754.0,
    "tuples_QCD_Bin-PT-300to470_Fil-MuEnriched_2024_2024.root":  699.6,
    "tuples_QCD_Bin-PT-470to600_Fil-MuEnriched_2024_2024.root":  67.67,
    "tuples_QCD_Bin-PT-600to800_Fil-MuEnriched_2024_2024.root":  21.27,
    "tuples_QCD_Bin-PT-800to1000_Fil-MuEnriched_2024_2024.root": 3.89,
    "tuples_QCD_Bin-PT-1000_Fil-MuEnriched_2024_2024.root":      1.323,

    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root":            1.051e7 * (409318867 / 8.31e9),  # ~= 5.18e5 pb
}

# Number of generated events per background sample (from DAS nevents)
BKG_NGEN = {
    "tuples_QCD_Bin-PT-15to20_Fil-MuEnriched_2024_2024.root":    125036760,
    #"tuples_QCD_Bin-PT-20to30_Fil-MuEnriched_2024_2024.root":    93304586, #ZOMBIE (for now)
    "tuples_QCD_Bin-PT-30to50_Fil-MuEnriched_2024_2024.root":    95305920,
    "tuples_QCD_Bin-PT-50to80_Fil-MuEnriched_2024_2024.root":    107449521,
    "tuples_QCD_Bin-PT-80to120_Fil-MuEnriched_2024_2024.root":   94128199,
    "tuples_QCD_Bin-PT-120to170_Fil-MuEnriched_2024_2024.root":  99824346,
    "tuples_QCD_Bin-PT-170to300_Fil-MuEnriched_2024_2024.root":  94338762,
    "tuples_QCD_Bin-PT-300to470_Fil-MuEnriched_2024_2024.root":  79815908,
    "tuples_QCD_Bin-PT-470to600_Fil-MuEnriched_2024_2024.root":  71786916,
    "tuples_QCD_Bin-PT-600to800_Fil-MuEnriched_2024_2024.root":  85842835,
    "tuples_QCD_Bin-PT-800to1000_Fil-MuEnriched_2024_2024.root": 81930100,
    "tuples_QCD_Bin-PT-1000_Fil-MuEnriched_2024_2024.root":      87293168,
    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root":            409318867,
}


# Fraction of the generated MiniAOD sample actually represented by the on-disk tuple.
# Two independent factors:
#   (a) looper coverage: only 114,448,466 of 409,318,867 events were processed -- the looper
#       run was cancelled mid-way (66 of ~127 file-groups; 528/1013 input files, 2026-07-03).
#   (b) skim: skim_minbias.C kept the first 1/6 of the filled tuple (6,431,840 / 38,583,328).
#   (a) looper coverage: 114,448,466 / 409,318,867 events processed (run cancelled mid-way).
#   (b) skim: skim_minbias.C kept the first 1/6 (6,431,840 / 38,583,328) -- ONLY for the
#       parking_nochi2 tuple. The tuples_L1_info re-fill is unskimmed, so (b) drops out there.
_MINBIAS_LOOPER_COV  = 114448466 / 409318867          # ~= 0.2796
_MINBIAS_SKIM_FRAC   = 6431840 / 38583328             # ~= 0.1667 (skimmed tuple only)
BKG_FRACTION = {
    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root":
        _MINBIAS_LOOPER_COV * (1.0 if MINBIAS_UNSKIMMED else _MINBIAS_SKIM_FRAC),
}

def _bkg_fraction(fname):
    return BKG_FRACTION.get(fname, 1.0)

def _eff_ngen(fname):
    """Effective generated-event denominator for the loaded subsample: frac * N_gen.
    Using this everywhere N_gen enters the yield keeps subsampling unbiased."""
    return _bkg_fraction(fname) * BKG_NGEN[fname]

PB_TO_FB = 1.0e3   # 1 pb = 1000 fb (for the QCD background cross sections)

_HERE      = Path(__file__).resolve().parent
tuples_dir = _HERE.parent / TUPLES_SUBDIR

# Filename suffix tagging the background set used (appended to every plot/table).
OUT_TAG = "_minBias"

# ---------------------------------------------------------------------------
# Per-lxy-bin cut-and-count
# ---------------------------------------------------------------------------
CNC_LXY_DIRS = {
    (10.0, 1.00): "mpi10_mA1p00",
    (4.0,  1.33): "mpi4_mA1p33",
}

def _parse_cnc_lxy_table(path):
    """Parse one cutncount table into {lxy_label -> (sig_eff, bkg_rej)} for the
    per-lxy-bin rows (cutncount label style, e.g. '0p0-0p2'). Rows look like:
    '   0p0-0p2 |   6993/18961        0.369 | 973828/5061994      0.808'."""
    out = {}
    for line in Path(path).read_text().splitlines():
        if line.count("|") != 2:
            continue
        left, mid, right = line.split("|")
        # Per-lxy (and 'full range') rows carry 'pass/total' fractions; skip the
        # cutflow/header rows, which never do.
        if "/" not in mid or "/" not in right:
            continue
        try:
            eff = float(mid.split()[-1])
            rej = float(right.split()[-1])
        except (ValueError, IndexError):
            continue
        out[left.strip()] = (eff, rej)
    return out

# Cut-and-count tables (BDT/cnc_tables/mpi*_mA*/cnc_ctau-*mm_<bkg>*.txt) are parsed
# directly -- both the full-range operating points (CNC_POINTS) and the per-lxy-bin
# points come straight from these files, so nothing is hand-typed. The '<bkg>*' glob
# also matches the mass-window suffix cutncount adds (e.g. _qcd_mwinRel0p1.txt).
_CNC_DIR       = _HERE / "cnc_tables"
_CNC_SUBDIR_RE = re.compile(r"^mpi(\w+)_mA(\w+)$")

def _cnc_bkg_for_tag(tag):
    """Map a plot tag (OUT_TAG / SUB_BKGS) to the cutncount --bkg filename token."""
    return {"_minBias": "minbias", "_QCD": "qcd"}.get(tag)

def _iter_cnc_tables(bkg):
    """Yield (mpi, mA, ctau, path) for every cnc_tables/mpi*_mA*/cnc_ctau-*mm_<bkg>*.txt.
    Matches window-tagged names too (cnc_ctau-1p0mm_qcd_mwinRel0p1.txt); if both a
    windowed and a full-mass table exist for a point, the last in sorted order wins."""
    if not bkg:
        return
    for sub in sorted(_CNC_DIR.glob("mpi*_mA*")):
        m = _CNC_SUBDIR_RE.match(sub.name)
        if not m:
            continue
        mpi_v = float(m.group(1).replace("p", "."))
        mA_v  = float(m.group(2).replace("p", "."))
        for fp in sorted(sub.glob(f"cnc_ctau-*mm_{bkg}*.txt")):
            name   = fp.name
            ctau_v = float(name[len("cnc_ctau-"):name.index("mm_")].replace("p", "."))
            yield mpi_v, mA_v, ctau_v, fp

def _load_cnc_fullrange_points(bkg):
    """{(mpi, mA, ctau): (sig_eff, bkg_rej)} from the 'full range' row of each table."""
    pts = {}
    for mpi_v, mA_v, ctau_v, fp in _iter_cnc_tables(bkg):
        rows = _parse_cnc_lxy_table(fp)
        if "full range" in rows:
            pts[(mpi_v, mA_v, ctau_v)] = rows["full range"]
    return pts

def _load_cnc_lxy_points(bkg):
    """Build {(mpi, mA): {lxy_label(cutncount) -> {ctau -> (eff, rej)}}} for the
    CNC_LXY_DIRS mass points, from the per-lxy-bin rows of the <bkg> tables."""
    pts = {}
    for mpi_v, mA_v, ctau_v, fp in _iter_cnc_tables(bkg):
        if (mpi_v, mA_v) not in CNC_LXY_DIRS:
            continue
        for lbl, (eff, rej) in _parse_cnc_lxy_table(fp).items():
            if lbl == "full range":
                continue
            pts.setdefault((mpi_v, mA_v), {}).setdefault(lbl, {})[ctau_v] = (eff, rej)
    return pts

# Full-range C&C operating points, auto-loaded per background tag (was hardcoded).
CNC_POINTS = {
    "_minBias": _load_cnc_fullrange_points("minbias"),
    "_QCD":     _load_cnc_fullrange_points("qcd"),
}

FIGSIZE     = (8.5, 6.5)
MASS_COLORS = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#e377c2"]
BKG_FACE    = "#7fc7c4"
BKG_EDGE    = "#2f5f5d"

# Trailing (?:_\w+)? matches the event-range suffix the L1-info tuples carry
# (e.g. ..._2024_0To999999.root); the parking_nochi2 names end plainly at _2024.root.
_SIG_RE = re.compile(r"tuples_Signal_ScenarioA_Par_2024_mpi-(\w+)_mA-(\w+)_ctau-(\w+)mm_2024(?:_\w+)?\.root")

def _p2f(s):
    return float(s.replace("p", "."))

def _flabel(f):
    return f"{f:g}".replace(".", "p")

sig_file_params = []
for fpath in sorted(glob.glob(str(tuples_dir / "tuples_Signal_ScenarioA_Par_2024_*.root"))):
    m = _SIG_RE.search(os.path.basename(fpath))
    if m:
        mpi_s, mA_s, ctau_s = m.groups()
        sig_file_params.append((fpath, _p2f(mpi_s), _p2f(mA_s), _p2f(ctau_s)))

param_grid = [(p[3], p[2], p[1]) for p in sig_file_params]  # (ctau, mA, mpi)


# ---------------------------------------------------------------------------
# BDT variables — mirrors BDT_training.py
# ---------------------------------------------------------------------------
def _make_bdt_vars():
    sv_stems = [
        "chi2Ndof", "d3d_mumu_SV", "dphi_mumu_SV", "l3d", "lxy",
        "prob", "ptmm", "x", "xErr", "y", "yErr", "z", "zErr",
        "dr_mumu", "dphi_mumu", "deta_mumu", "deta_mumu_SV",
        "sindphi_lxy", "a3d_mumu",
    ]

    mu_stems = [
        "dxy", "dxysig", "dxy_lxy", "dz", "dzsig",
        "eta", "isGlobal", "isTracker", "isvtx", "maxdr",
        "mindr", "muCSCDT", "muChambs", "muHits", "nhitsbeforesv",
        "normChi2", "phi", "phiCorr", "pixHits", "pixLayers",
        "pt", "stripHits", "trkLayers", "PFIsoAll0p3", "PFRelIsoAll0p3",
    ]
    vars_ = []
    for sv in ("SV1", "SV2"):
        for s in sv_stems:
            vars_.append(f"{sv}_{s}")
        for mu in ("mu1", "mu2"):
            for s in mu_stems:
                vars_.append(f"{sv}_{mu}_{s}")
    return vars_

BDT_VARIABLES = _make_bdt_vars()
_LOAD_BRANCHES = list(dict.fromkeys(BDT_VARIABLES + ["SV1_lxy", "SV1_mass", "SV2_mass", "passL1"]))

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
def read_flat(path):
    with uproot.open(path) as f:
        t = f['tuples']
        available = set(t.keys())
        branches  = [b for b in _LOAD_BRANCHES if b in available]
        df = t.arrays(branches, library='pd')
    # All loaded branches are scalar doubles; store them as float32 to halve the
    # in-memory footprint (and every downstream copy: df_global, X_g, the
    # train/test split, the XGBoost matrix). Negligible precision loss for the BDT.
    return df.astype('float32')

def apply_l1(df, src):
    """If --require-l1, keep only events with passL1 != 0 (L1-seed decision), folding the
    L1 trigger efficiency into the sample. Errors out if the branch is missing (wrong dir)."""
    if not REQUIRE_L1:
        return df
    if 'passL1' not in df.columns:
        raise SystemExit(f"--require-l1 set but '{src}' has no passL1 branch "
                         f"(use --tuples-dir tuples_L1_info).")
    return df[df['passL1'] > 0.5].reset_index(drop=True)

def compute_sample_weights(df):
    y = df['label'].values
    w = np.ones(len(df), dtype=float)
    bkg_mask = (y == 0)
    w[bkg_mask] = df.loc[bkg_mask, 'xsec_weight'].values

    # Class balancing: scale signal so total signal weight == total background weight.
    n_sig   = int((y == 1).sum())
    sum_bkg = float(w[bkg_mask].sum())
    if n_sig > 0 and sum_bkg > 0:
        w[y == 1] = sum_bkg / n_sig
    return w


def add_dxy_lxy(df):
    for sv in ("SV1", "SV2"):
        denom = df[f"{sv}_lxy"] * df[f"{sv}_mass"] / df[f"{sv}_ptmm"]
        # float32 fill so np.where doesn't upcast denom (and the derived columns) to float64.
        denom = np.where(denom > 1e-9, denom, np.float32(1e-9))
        for mu in ("mu1", "mu2"):
            df[f"{sv}_{mu}_dxy_lxy"] = np.abs(df[f"{sv}_{mu}_dxy"]) / denom

sig_frames = []
for fpath, mpi_val, mA_val, ctau_val in sig_file_params:
    if not Path(fpath).exists():
        continue
    df = apply_l1(read_flat(fpath), Path(fpath).name)
    df['param_ctau'] = float(ctau_val)
    df['param_mA']   = float(mA_val)
    df['param_mpi']  = float(mpi_val)
    df['label']      = 1
    sig_frames.append(df)
df_sig = pd.concat(sig_frames, ignore_index=True)


if _args.bkg == "minbias":
    OUT_TAG      = "_minBias"
    ACTIVE_FILES = list(MINBIAS_FILES)
    SUB_BKGS     = [("_minBias", list(MINBIAS_FILES), "-",  "MinBias")]
elif _args.bkg == "qcd":
    OUT_TAG      = "_QCD"
    ACTIVE_FILES = list(QCD_FILES)
    SUB_BKGS     = [("_QCD", list(QCD_FILES), "-", "QCD")]
else:
    OUT_TAG      = "_both"
    ACTIVE_FILES = list(MINBIAS_FILES) + list(QCD_FILES)
    SUB_BKGS     = [("_minBias", list(MINBIAS_FILES), "-",  "MinBias"),
                    ("_QCD",     list(QCD_FILES),     "--", "QCD")]

for BKG_FILES, OUT_TAG in [(ACTIVE_FILES, OUT_TAG)]:
    bkg_frames = []
    for fname in BKG_FILES:
        fpath = tuples_dir / fname
        if not fpath.exists():
            continue
        if BKG_XSEC.get(fname) is None or BKG_NGEN.get(fname) is None:
            continue
        df = apply_l1(read_flat(fpath), fname)
        df['label'] = 0
        df['bkg_file'] = fname
        # Cross-section reweighting (no lumi): per-event weight = sigma / (frac * N_gen).
        # For a pre-skimmed file (frac < 1) this normalizes the skim to the full sample.
        df['xsec_weight'] = BKG_XSEC[fname] / _eff_ngen(fname)
        bkg_frames.append(df)

    df_bkg = pd.concat(bkg_frames, ignore_index=True)

    add_dxy_lxy(df_sig)
    add_dxy_lxy(df_bkg)

    # ---------------------------------------------------------------------------
    # Lxy binning (cm)
    # ---------------------------------------------------------------------------
    lxy_bins   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]  # Match Scouting analysis
    lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1", "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]
    # Human-readable range per label for plot titles/legends, e.g. "[0, 0.2]" (cm).
    lxy_pretty = {lbl: rf'[{lxy_bins[i]:g}, {lxy_bins[i+1]:g}]'
                  for i, lbl in enumerate(lxy_labels)}
    #lxy_bins   = [0.0, 1.0, 10.0, 100.0] # Match Parking analysis
    #lxy_labels = ["0to1", "1to10", "10to100"]

    df_sig['lxy_bin'] = pd.cut(df_sig['SV1_lxy'], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
    df_bkg['lxy_bin'] = pd.cut(df_bkg['SV1_lxy'], bins=lxy_bins, labels=lxy_labels, include_lowest=True)

    available  = set(df_sig.columns) & set(df_bkg.columns)
    input_vars = [v for v in BDT_VARIABLES if v in available]
    missing    = [v for v in BDT_VARIABLES if v not in available]



    cond_vars = ['param_ctau', 'param_mA', 'param_mpi'] if use_conditional else []
    out_dir   = _HERE / ('significance_plots_L1req' if REQUIRE_L1 else 'significance_plots')
    os.makedirs(out_dir, exist_ok=True)

    # ---------------------------------------------------------------------------
    # Train global BDT
    # ---------------------------------------------------------------------------
    if use_conditional:
        # Parametric BDT: replicate the full background once per signal point
        _combined = []
        for ctau_val, mA_val, mpi_val in param_grid:
            sig_pt = df_sig[
                (df_sig['param_ctau'] == ctau_val) &
                (df_sig['param_mA']   == mA_val)   &
                (df_sig['param_mpi']  == mpi_val)
            ].copy()
            bkg_cp = df_bkg.copy()
            bkg_cp['param_ctau'] = float(ctau_val)
            bkg_cp['param_mA']   = float(mA_val)
            bkg_cp['param_mpi']  = float(mpi_val)
            _combined.append(pd.concat([sig_pt, bkg_cp], ignore_index=True))
        df_global = pd.concat(_combined, ignore_index=True)
    else:
        df_global = pd.concat([df_sig, df_bkg], ignore_index=True)

    # df_sig/df_bkg are fully folded into df_global now; free them so their rows
    # aren't held alongside the copies below (df_global, X_g, the split).
    del df_sig, df_bkg
    gc.collect()

    X_g = df_global[input_vars + cond_vars]
    y_g = df_global['label']
    w_g = compute_sample_weights(df_global)
    df_global['weight'] = w_g

    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        X_g, y_g, w_g, test_size=0.3, random_state=42, stratify=y_g)
    # X_g is only needed to build the split; drop it (train/test hold their copies).
    del X_g
    gc.collect()

    bdt = XGBClassifier(
        n_estimators=100, max_depth=3, learning_rate=0.1,
        use_label_encoder=False, eval_metric='logloss',
        tree_method='hist', n_jobs=4,
    )
    bdt.fit(X_train, y_train, sample_weight=w_train)

    # ---------------------------------------------------------------------------
    # Find working point
    # ---------------------------------------------------------------------------
    y_score = bdt.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_score, sample_weight=w_test)
    auc = roc_auc_score(y_test, y_score, sample_weight=w_test)

    # Single output directory holding the FPR-scanned significance tables/plots.
    if True:
        out_dir = _HERE / ('significance_plots_L1req' if REQUIRE_L1 else 'significance_plots')
        os.makedirs(out_dir, exist_ok=True)

        def _mp_dir(mpi_val, mA_val, lxy_label=None):
            """Per-mass-point output directory out_dir/mpi<X>/mA_<Y>[/lxy_<label>]
            (created). When lxy_label is given, the per-lxy outputs go into an
            lxy_<label> subfolder of the mass point directory."""
            d = out_dir / f'mpi{_flabel(mpi_val)}' / f'mA_{_flabel(mA_val)}'
            if lxy_label is not None:
                d = d / f'lxy_{lxy_label}'
            os.makedirs(d, exist_ok=True)
            return d

        # ---------------------------------------------------------------------------
        # ROC curve
        # ---------------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
        ax.plot(fpr, tpr, color='#1f77b4', linewidth=2.0, label=f'Global BDT (AUC = {auc:.3f})')
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, linewidth=1.0)

        # Overlay the cut-and-count operating points (restricted to the CNC_LXY_DIRS
        # mass points to avoid clutter) at (1-bkg_rej, sig_eff). One distinct colour per
        # (mpi, mA, ctau) point; marker distinguishes the background. One legend entry
        # per point; all ctau of a point share x (bkg_rej is background-only).
        _cnc_marker = {"_minBias": "X", "_QCD": "P"}
        _cnc_points = sorted({(mpi, mA, c) for tag, _sf, _ls, _lbl in SUB_BKGS
                              for (mpi, mA, c) in CNC_POINTS.get(tag, {})
                              if (mpi, mA) in CNC_LXY_DIRS})
        _cnc_cmap  = plt.get_cmap('tab10')
        _cnc_color = {p: _cnc_cmap(i % 10) for i, p in enumerate(_cnc_points)}
        _cnc_seen = set()
        for tag, _sf, _ls, _lbl in SUB_BKGS:
            for (mpi_p, mA_p, ctau_p), (eff, rej) in sorted(CNC_POINTS.get(tag, {}).items()):
                if (mpi_p, mA_p) not in CNC_LXY_DIRS:
                    continue
                lab = None
                if (mpi_p, mA_p, ctau_p) not in _cnc_seen:
                    lab = rf'$m_\pi={mpi_p:g}$, $m_A={mA_p:g}$, $c\tau={ctau_p:g}$ mm'
                    _cnc_seen.add((mpi_p, mA_p, ctau_p))
                ax.scatter([1.0 - rej], [eff], marker=_cnc_marker.get(tag, "X"), s=45,
                           color=_cnc_color[(mpi_p, mA_p, ctau_p)], edgecolor='k', linewidth=0.4,
                           zorder=6, label=lab)

        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Global BDT ROC curve')
        ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
        ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes, fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
        ax.tick_params(direction="in", top=True, right=True, which="both")
        fig.savefig(out_dir / f'ROC_globalBDT{OUT_TAG}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

        # ---------------------------------------------------------------------------
        # Feature importance (XGBoost gain), top-N input variables
        # ---------------------------------------------------------------------------
        feat_names = list(input_vars + cond_vars)
        importances = np.asarray(bdt.feature_importances_, dtype=float)
        order       = np.argsort(importances)[::-1]
        top_n       = min(30, len(feat_names))
        top_idx     = order[:top_n][::-1]  # reversed so the largest is at the top of barh
        fig, ax = plt.subplots(figsize=(7.5, max(4.0, 0.28 * top_n)), constrained_layout=True)
        ax.barh(range(top_n), importances[top_idx], color='#1f77b4', edgecolor='#0f3b5f', linewidth=0.5)
        ax.set_yticks(range(top_n))
        ax.set_yticklabels([feat_names[i] for i in top_idx], fontsize=7)
        ax.set_xlabel('Feature importance (gain)')
        ax.set_title(f'Global BDT feature importance (top {top_n})')
        ax.text(0.98, 0.02, "Preliminary", transform=ax.transAxes, fontsize=11,
                fontstyle="italic", fontweight="bold", va="bottom", ha="right")
        ax.tick_params(direction="in", top=True, right=True, which="both")
        fig.savefig(out_dir / f'feature_importance_globalBDT{OUT_TAG}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

        # Also dump the full ranking to a text file for reference.
        _fi_lines = ["rank  importance  feature"]
        for r, i in enumerate(order):
            _fi_lines.append(f'{r:>4}  {importances[i]:>10.5f}  {feat_names[i]}')
        (out_dir / f'feature_importance_globalBDT{OUT_TAG}.txt').write_text('\n'.join(_fi_lines) + '\n')

        # ---------------------------------------------------------------------------
        # ROC curve split by SV1 lxy bin (same global BDT, test set partitioned):
        # one plot PER lxy bin, saved into that bin's per-mass-point directory, with
        # that mass point's cut-and-count operating points overlaid (one per ctau).
        # ---------------------------------------------------------------------------
        # lxy_bin for the test rows, aligned positionally to y_score/y_test.
        lxy_test  = df_global.loc[X_test.index, 'lxy_bin'].to_numpy()
        y_test_a  = np.asarray(y_test)
        w_test_a  = np.asarray(w_test)

        # Per-bin global ROC curve, computed once and reused for every mass point.
        _bin_roc = {}   # lxy_label -> (fpr, tpr, auc)
        for lxy_label in lxy_labels:
            m = (lxy_test == lxy_label)
            # Need both classes present to define a ROC.
            if m.sum() < 10 or len(np.unique(y_test_a[m])) < 2:
                continue
            fpr_b, tpr_b, _ = roc_curve(y_test_a[m], y_score[m], sample_weight=w_test_a[m])
            auc_b = roc_auc_score(y_test_a[m], y_score[m], sample_weight=w_test_a[m])
            _bin_roc[lxy_label] = (fpr_b, tpr_b, auc_b)

        # One plot per (C&C mass point, lxy bin): the bin's ROC curve + that mass
        # point's cut-and-count points, one distinct colour/legend entry per ctau.
        _cnc_lxy  = _load_cnc_lxy_points(_cnc_bkg_for_tag(OUT_TAG))
        _cnc_cmap = plt.get_cmap('tab10')
        for (mpi_p, mA_p), per_bin in sorted(_cnc_lxy.items()):
            for lxy_label in lxy_labels:
                roc = _bin_roc.get(lxy_label)
                if roc is None:
                    continue
                fpr_b, tpr_b, auc_b = roc
                fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
                ax.plot(fpr_b, tpr_b, color='#1f77b4', linewidth=2.0,
                        label=rf'BDT $l_{{xy}}$ {lxy_pretty[lxy_label]} cm (AUC = {auc_b:.3f})')
                ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, linewidth=1.0)
                # cutncount tables use '-' where workingpoint labels use 'to'.
                pts = per_bin.get(lxy_label.replace("to", "-"), {})
                for i, (ctau_v, (eff, rej)) in enumerate(sorted(pts.items())):
                    ax.scatter([1.0 - rej], [eff], marker='o', s=45,
                               color=_cnc_cmap(i % 10), edgecolor='k', linewidth=0.4,
                               zorder=6, label=rf'$c\tau={ctau_v:g}$ mm')
                ax.set_xlabel('False Positive Rate')
                ax.set_ylabel('True Positive Rate')
                ax.set_title(rf'ROC $m_\pi={mpi_p:g}$, $m_A={mA_p:g}$, $l_{{xy}}$ {lxy_pretty[lxy_label]} cm')
                ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
                ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes, fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
                ax.tick_params(direction="in", top=True, right=True, which="both")
                _fout = _mp_dir(mpi_p, mA_p, lxy_label) / f'ROC_bylxy_{lxy_label}{OUT_TAG}.png'
                fig.savefig(_fout, dpi=150, bbox_inches='tight')
                plt.close(fig)

        # ---------------------------------------------------------------------------
        # Score all events
        # ---------------------------------------------------------------------------
        X_all              = df_global[input_vars + cond_vars]
        df_global          = df_global.copy()
        df_global['score'] = bdt.predict_proba(X_all)[:, 1]

        # Group ctau values by (mpi, mA) for the per-signal-point plots below.
        mpi_mA_groups = {}
        for ctau_val, mA_val, mpi_val in param_grid:
            mpi_mA_groups.setdefault((mpi_val, mA_val), []).append(ctau_val)

        # ---------------------------------------------------------------------------
        # Discriminant (BDT score) distribution — one per (mpi, mA), lines = ctau
        # ---------------------------------------------------------------------------
        disc_bins   = np.linspace(0.0, 1.0, 51)
        disc_widths = np.diff(disc_bins)
        bkg_disc    = df_global.loc[df_global['label'] == 0, 'score'].values

        for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
            plot_dir_g = _mp_dir(mpi_val, mA_val)
            fig, ax = plt.subplots(figsize=(7.2, 5.6), constrained_layout=True)
            hb, _ = np.histogram(bkg_disc, bins=disc_bins)
            if hb.sum() > 0:
                hb = hb / hb.sum()
            ax.bar(disc_bins[:-1], hb, width=disc_widths, align='edge', color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6, label='Background', zorder=1)

            for i, ctau_val in enumerate(sorted(ctau_vals)):
                sig_mask = (
                    (df_global['label']      == 1) &
                    (df_global['param_ctau'] == float(ctau_val)) &
                    (df_global['param_mA']   == float(mA_val))   &
                    (df_global['param_mpi']  == float(mpi_val))
                )
                if int(sig_mask.sum()) < 5:
                    continue
                hs, _ = np.histogram(df_global.loc[sig_mask, 'score'].values, bins=disc_bins)
                if hs.sum() > 0:
                    hs = hs / hs.sum()
                ax.stairs(hs, disc_bins, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6, label=rf'$c\tau={ctau_val:g}$ mm', zorder=3 + i)

            ax.set_xlabel('BDT score')
            ax.set_ylabel('a.u.')
            ax.set_xlim(0.0, 1.0)
            ax.set_title(rf'Discriminant Global $m_\pi={mpi_val:g}$ GeV, $m_A={mA_val:g}$ GeV')
            ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes, fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
            ax.legend(loc='upper center', fontsize=9, framealpha=0.9)
            ax.tick_params(direction="in", top=True, right=True, which="both")
            _fout = plot_dir_g / f'Disc_global_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{OUT_TAG}.png'
            fig.savefig(_fout, dpi=150, bbox_inches='tight')
            plt.close(fig)

        def _bkg_param_mask(key):
            """In conditional mode, restrict background to the copy tagged with `key`'s
            params (the parametric BDT must be evaluated *at* that point). None otherwise."""
            if not use_conditional:
                return None
            return ((df_global['param_mpi']  == key[0]) &
                    (df_global['param_mA']   == key[1]) &
                    (df_global['param_ctau'] == key[2]))

        _MASS_WINDOW_CACHE  = {}

        def _signal_mass_window(key):
            #Mass-dependent window [mA - W(mA), mA + W(mA)]; W is relative or absolute
            if not MASS_WINDOW_ACTIVE: #if no window is selected, scan over all the mass range
                return None
            if key in _MASS_WINDOW_CACHE:
                return _MASS_WINDOW_CACHE[key]
            mA   = key[1]
            half = _mass_window_halfwidth(mA)
            win  = (mA - half, mA + half)
            _MASS_WINDOW_CACHE[key] = (win, mA, half)
            return _MASS_WINDOW_CACHE[key]

        def _mass_window_mask(key):
            #Select events inside SV1 mass window
            res = _signal_mass_window(key)
            if res is None:
                return None
            (lo, hi), _center, _half = res
            return (df_global['SV1_mass'] >= lo) & (df_global['SV1_mass'] <= hi)

        def _combine_masks(*masks):
            """AND together the non-None boolean masks; None if all are None."""
            out = None
            for m in masks:
                if m is None:
                    continue
                out = m if out is None else (out & m)
            return out

        # ---------------------------------------------------------------------------
        # Asimov significance table (one-sided p0 = 1 - Phi(Z), with Z)
        # ---------------------------------------------------------------------------
        # Rows  = target FPRs; for each, the BDT threshold is the one at which the
        #         xsec-weighted SV-selected QCD has that false-positive rate.
        # Cols  = signal points (ctau, for each (mpi, mA)).
        # Cells = p0 = 1 - Phi(Z) with the Gaussian/Asimov Z in parentheses, where
        #         S = L * sigma_ggH*B(H->psipsi) * BR_cascade * (n_pass/N_gen)
        #         B = FPR * L * sum_q sigma_q * eff_q^SV  (== xsec-weighted bkg above cut)
        def _counts_above_thr(scores, t):
            return int(np.count_nonzero(scores > t))

        def _bkg_b_at(t, extra_mask=None, files=None):
            #xsec-weighted background yield with score > t. `files` restricts the sum to one
            #sub-background (e.g. only MinBias or only QCD); None = all loaded backgrounds.
            base = (df_global['label'] == 0)
            if extra_mask is not None:
                base = base & extra_mask
            b = 0.0
            for fname in BKG_XSEC:
                if BKG_XSEC.get(fname) is None or BKG_NGEN.get(fname) is None:
                    continue
                if files is not None and fname not in files:
                    continue
                sc = df_global.loc[base & (df_global['bkg_file'] == fname), 'score'].values
                if len(sc) == 0:
                    continue
                # Denominator is frac*N_gen so a loaded subsample normalizes to the full sample.
                b += BKG_XSEC[fname] * PB_TO_FB * LUMI_FB * (_counts_above_thr(sc, t) / _eff_ngen(fname))
            return b

        def _sig_s_at(key, t, extra_mask=None):
            """Signal yield with score > t for `key`=(mpi, mA, ctau); None if no events."""
            sel = ((df_global['label'] == 1) &
                   (df_global['param_mpi']  == key[0]) &
                   (df_global['param_mA']   == key[1]) &
                   (df_global['param_ctau'] == key[2]))
            if extra_mask is not None:
                sel = sel & extra_mask
            sc = df_global.loc[sel, 'score'].values
            if len(sc) == 0:
                return None
            sig_eff = _counts_above_thr(sc, t) / SIG_NGEN[key]
            # eff_S already includes the cascade BR (folded in by the MC) -> NO external BR factor.
            return SIG_XSEC_PB * PB_TO_FB * LUMI_FB * sig_eff

        # Background samples actually loaded, and their cross-section sum (denominator of
        # the weighted-average count). Fixed across cut stages so the ratio = efficiency.
        _bkg_files_loaded = [f for f in BKG_XSEC if BKG_XSEC.get(f) is not None and bool((df_global['bkg_file'] == f).any())]
        _sigma_sum = sum(BKG_XSEC[f] for f in _bkg_files_loaded)

        def _qcd_weighted(extra_mask=None, files=None):
            #Cross-section-weighted average event count. `files` restricts to one sub-background.
            base = (df_global['label'] == 0)
            if extra_mask is not None:
                base = base & extra_mask
            _files = _bkg_files_loaded if files is None else [f for f in _bkg_files_loaded if f in files]
            _norm  = sum(BKG_XSEC[f] for f in _files)
            num = 0.0
            for f in _files:
                # Scale the loaded count to the full-sample equivalent (1/frac) so the
                # weighted-average count is comparable across subsampled/fully-loaded files.
                n_q = int((base & (df_global['bkg_file'] == f)).sum()) / _bkg_fraction(f)
                num += BKG_XSEC[f] * n_q
            return num / _norm if _norm > 0 else 0.0

        def _sig_count(key, extra_mask=None):
            #Raw signal event count
            sel = ((df_global['label'] == 1) &
                   (df_global['param_mpi']  == key[0]) &
                   (df_global['param_mA']   == key[1]) &
                   (df_global['param_ctau'] == key[2]))
            if extra_mask is not None:
                sel = sel & extra_mask
            return int(sel.sum())

        if _args.table:
            # FPR -> threshold from the xsec-weighted ROC (closest grid point).
            fpr_targets = sorted(_args.fpr_targets, reverse=True)
            fpr_rows = []
            for f_t in fpr_targets:
                j      = int(np.argmin(np.abs(fpr - f_t)))
                fpr_rows.append((f_t, float(fpr[j]), float(thresholds[j])))

            _win_str = (', ' + _win_label_str()) if MASS_WINDOW_ACTIVE else ''
            _hdr = (rf'Asimov significance $p_0$ ($Z$)  '
                    rf'(presel.+SV+BDT{_win_str}, $\sigma_{{ggH}}\mathcal{{B}}(H\to\psi\bar\psi)='
                    rf'{SIG_XSEC_PB:g}$ pb, $L={LUMI_FB:g}$ fb$^{{-1}}$)')

            # Significance vs ctau (one line per FPR target), from the table cells.
            _FPR_COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]
            _FPR_MARKERS = ["o", "s", "^", "D", "v"]

            def _significance_vs_ctau_plot(cells_by_sub, keys, ctaus, mpi_val, mA_val, lxy_label=None):
                # cells_by_sub[sub_tag] = cells for that sub-background (same shared-BDT
                # thresholds). In 'both' mode each FPR gets one line per sub-background
                # (distinguished by linestyle); single modes draw one solid line per FPR.
                if not ctaus:
                    return
                order = np.argsort(np.array(ctaus, dtype=float))
                x = np.array(ctaus, dtype=float)[order]
                fig, ax = plt.subplots(figsize=FIGSIZE)
                z_max = 0.0
                for i, (f_t, _f_ach, _thr) in enumerate(fpr_rows):
                    for (sub_tag, _sf, ls, _lbl) in SUB_BKGS:
                        cells = cells_by_sub[sub_tag]
                        z = np.array([cells[(f_t, keys[j])][1] for j in range(len(keys))], dtype=float)[order]
                        z = np.nan_to_num(z, nan=0.0)
                        z_max = max(z_max, float(z.max()))
                        ax.plot(x, z, color=_FPR_COLORS[i % len(_FPR_COLORS)], linestyle=ls,
                                marker=_FPR_MARKERS[i % len(_FPR_MARKERS)], markersize=7,
                                linewidth=1.8, zorder=3 + i)
                ax.set_xscale('log')
                ax.set_xlabel(r'$c\tau$ [mm]')
                ax.set_ylabel(r'Asymptotic significance $Z$')
                # Headroom so the header/annotations/legend don't collide with the curves.
                ax.set_ylim(0.0, z_max * 1.45 if z_max > 0 else 1.0)
                # Header: trigger (left) + lumi/energy (right), CMS-style.
                ax.text(0.0, 1.01, TRIGGER_LABEL, transform=ax.transAxes, ha='left', va='bottom',
                        fontweight='bold', fontsize=13)
                ax.text(1.0, 1.01, rf'{LUMI_FB:g} fb$^{{-1}}$ (13.6 TeV, 2024)', transform=ax.transAxes,
                        ha='right', va='bottom', fontsize=12)
                # Annotations (model, masses, BR, mass window).
                txt = [rf'Scenario {model_tag}', rf'$m_{{\pi_3}} = {mpi_val:g}$ GeV',
                       rf"$m_{{A'}} = {mA_val:g}$ GeV"]
                br = BR_A_MUMU.get((mpi_val, mA_val))
                if br is not None:
                    txt.append(rf"$B(A'\to\mu\mu) = {br:g}$")
                res = _signal_mass_window(keys[0])
                if res is not None:
                    (lo, hi), _c, _h = res
                    txt.append(rf'Mass window: $[{lo:.2f}, {hi:.2f}]$ GeV')
                if lxy_label is not None:
                    txt.append(rf'$l_{{xy}} \in {lxy_label.replace("to", "-")}$ cm')
                ax.text(0.04, 0.96, '\n'.join(txt), transform=ax.transAxes, va='top', ha='left', fontsize=11)
                # FPR colour legend always; a background-linestyle legend only when overlaying.
                fpr_handles = [Line2D([0], [0], color=_FPR_COLORS[i % len(_FPR_COLORS)],
                                      marker=_FPR_MARKERS[i % len(_FPR_MARKERS)], linestyle='-',
                                      label=rf'FPR$=10^{{{int(round(np.log10(f_t)))}}}$')
                               for i, (f_t, _a, _t) in enumerate(fpr_rows)]
                leg1 = ax.legend(handles=fpr_handles, loc='upper right', framealpha=0.9, fontsize=10)
                ax.add_artist(leg1)
                if len(SUB_BKGS) > 1:
                    bkg_handles = [Line2D([0], [0], color='k', linestyle=ls, label=lbl)
                                   for (_st, _sf, ls, lbl) in SUB_BKGS]
                    ax.legend(handles=bkg_handles, loc='center right', framealpha=0.9, fontsize=10)
                ax.tick_params(direction='in', top=True, right=True, which='both')
                fig.tight_layout()
                _fout = _mp_dir(mpi_val, mA_val, lxy_label) / f'significance_vs_ctau_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{OUT_TAG}.png'
                fig.savefig(_fout, dpi=130)
                plt.close(fig)

            def _build_cells(keys, extra_mask=None, files=None):
                """cells[(f_t, key)] = (p0, Z, s, b) at each FPR threshold, optionally
                restricted to an extra mask (e.g. an lxy bin) and to one sub-background's
                `files` (b only; s is background-independent). Mass window always applied."""
                cells = {}
                for f_t, _f_ach, thr in fpr_rows:
                    for k in keys:
                        mwin = _combine_masks(_mass_window_mask(k), extra_mask)
                        s = _sig_s_at(k, thr, mwin)
                        b = _bkg_b_at(thr, _combine_masks(_bkg_param_mask(k), mwin), files=files)
                        if s is None or s <= 0.0 or b <= 0.0:
                            cells[(f_t, k)] = (float('nan'), 0.0, s, b)
                            continue
                        Z  = float(np.sqrt(2.0 * ((s + b) * np.log1p(s / b) - s)))
                        p0 = float(norm.sf(Z))
                        cells[(f_t, k)] = (p0, Z, s, b)
                return cells

            def _write_asimov_tex(cells_by_sub, keys, ctaus, mpi_val, mA_val, lxy_label=None):
                """Write the booktabs Asimov p0(Z) table(s). One tabular per sub-background
                (labelled when overlaying) into a single OUT_TAG-suffixed file. When lxy_label
                is given, the lxy range is added to the header and the file name suffix."""
                hdr = _hdr
                if lxy_label is not None:
                    hdr = _hdr + rf'  [$l_{{xy}}\in {lxy_label.replace("to", "-")}$ cm]'
                tex = []
                for (sub_tag, _sf, _ls, sub_lbl) in SUB_BKGS:
                    cells = cells_by_sub[sub_tag]
                    hdr_b = hdr + (rf'  -- {sub_lbl}' if len(SUB_BKGS) > 1 else '')
                    tex.append(r'\begin{tabular}{l c ' + 'c ' * len(ctaus) + r'}')
                    tex.append(r'\toprule')
                    tex.append(r'\multicolumn{' + str(2 + len(ctaus)) + r'}{l}{' + hdr_b + r'} \\')
                    tex.append(r'\midrule')
                    tex.append(r' & & ' + ' & '.join(rf'$m_\pi={mpi_val:g}$, $m_A={mA_val:g}$' for _ in ctaus) + r' \\')
                    tex.append(r'FPR & BDT threshold & ' + ' & '.join(rf'$c\tau={c:g}$ mm' for c in ctaus) + r' \\')
                    tex.append(r'\midrule')
                    for f_t, _f_ach, thr in fpr_rows:
                        row_cells = []
                        for k in keys:
                            p0, Z, _s, _b = cells[(f_t, k)]
                            row_cells.append(rf'{p0:.2g} (${Z:.1f}\sigma$)')
                        tex.append(rf'$10^{{{int(round(np.log10(f_t)))}}}$ & {thr:.4f} & '
                                   + ' & '.join(row_cells) + r' \\')
                    tex.append(r'\bottomrule')
                    tex.append(r'\end{tabular}')
                    tex.append('')
                tex_path = _mp_dir(mpi_val, mA_val, lxy_label) / f'asimov_table_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{OUT_TAG}.tex'
                tex_path.write_text('\n'.join(tex) + '\n')

            def _sb_table_lines(cells_by_sub, keys, header):
                """Text block listing the actual S and B (xsec*lumi-weighted yields) that
                feed each significance, one sub-block per FPR threshold, per sub-background."""
                lines = [header]
                for (sub_tag, _sf, _ls, sub_lbl) in SUB_BKGS:
                    cells = cells_by_sub[sub_tag]
                    if len(SUB_BKGS) > 1:
                        lines.append(f'  [{sub_lbl}]')
                    for f_t, _f_ach, thr in fpr_rows:
                        lines.append(f'  FPR = {f_t:g}  (BDT score > {thr:.4f}):')
                        sub = f'{"ctau":>10}{"S":>14}{"B":>14}{"Z":>10}{"p0":>12}'
                        lines.append(sub)
                        lines.append('  ' + '-' * (len(sub) - 2))
                        for k in keys:
                            p0, Z, s, b = cells[(f_t, k)]
                            s_str = 'n/a' if s is None else f'{s:.4g}'
                            b_str = 'n/a' if b is None else f'{b:.4g}'
                            lines.append(f'{format(k[2],"g")+"mm":>10}{s_str:>14}{b_str:>14}{Z:>10.2f}{p0:>12.3g}')
                        lines.append('')
                return lines

            for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
                # Keep only signal points with a known N_gen (needed for the yield).
                keys = [(mpi_val, mA_val, c) for c in sorted(ctau_vals)
                        if (mpi_val, mA_val, c) in SIG_NGEN]
                if not keys:
                    continue

                ctaus = [k[2] for k in keys]
                # One cell set per sub-background (b restricted to its files, evaluated at the
                # shared-BDT thresholds). Single modes have one entry; 'both' has two.
                cells_by_sub = {st: _build_cells(keys, files=sf) for (st, sf, _ls, _lbl) in SUB_BKGS}

                # Inclusive LaTeX table + significance vs ctau plot.
                _write_asimov_tex(cells_by_sub, keys, ctaus, mpi_val, mA_val)
                _significance_vs_ctau_plot(cells_by_sub, keys, ctaus, mpi_val, mA_val)

                # Same table + plot per lxy bin; keep the per-bin cells for the cutflow below.
                cells_by_lxy = {}   # lxy_label -> {sub_tag -> cells}
                for lxy_label in lxy_labels:
                    lxy_mask = df_global['lxy_bin'] == lxy_label
                    cbs = {st: _build_cells(keys, lxy_mask, files=sf) for (st, sf, _ls, _lbl) in SUB_BKGS}
                    cells_by_lxy[lxy_label] = cbs
                    _write_asimov_tex(cbs, keys, ctaus, mpi_val, mA_val, lxy_label=lxy_label)
                    _significance_vs_ctau_plot(cbs, keys, ctaus, mpi_val, mA_val, lxy_label=lxy_label)

                #Cutflow: signal raw counts + per-background xsec-weighted count (no lumi)
                cf = []
                cf.append("Cutflow  (signal: raw event counts; "
                          "bkg: weighted = sum_q sigma_q N_q / sum_q sigma_q, no lumi)")
                cf.append(f'mpi = {mpi_val:g} GeV, mA = {mA_val:g} GeV')
                cw  = 16
                _wcols = [(sub_lbl, sf) for (_st, sf, _ls, sub_lbl) in SUB_BKGS]
                hdr = (f'{"stage":>16}'
                       + ''.join(f'{("ctau="+format(c,"g")+"mm"):>{cw}}' for c in ctaus)
                       + ''.join(f'{(wl+" (wgt)"):>{cw}}' for wl, _ in _wcols))
                cf.append(hdr)
                cf.append('-' * len(hdr))
                row = f'{"ntuple":>16}'
                for k in keys:
                    row += f'{_sig_count(k, None):>{cw}}'
                for _wl, _wf in _wcols:
                    row += f'{_qcd_weighted(None, files=_wf):>{cw}.1f}'
                cf.append(row)

                if MASS_WINDOW_ACTIVE:
                    cf.append('')
                    cf.append("SV1 mass window (per ctau; bkg weighted within that point's window):")
                    sub = (f'{"ctau":>10} {"sig(win)":>12} '
                           + ' '.join(f'{(wl+" wgt(win)"):>16}' for wl, _ in _wcols))
                    cf.append(sub)
                    cf.append('-' * len(sub))
                    for k in keys:
                        mwin = _mass_window_mask(k)
                        row = f'{format(k[2],"g")+"mm":>10} {_sig_count(k, mwin):>12} '
                        row += ' '.join(f'{_qcd_weighted(mwin, files=wf):>16.1f}' for _wl, wf in _wcols)
                        cf.append(row)

                # Actual S and B (xsec*lumi-weighted yields) feeding each significance,
                # at every FPR threshold -- inclusive, then one block per lxy bin. The
                # mass window (if active) is already folded into these yields.
                cf.append('')
                cf += _sb_table_lines(
                    cells_by_sub, keys,
                    "S and B entering each significance "
                    "(inclusive; yields = sigma[pb] * 1e3 * L[fb^-1] * eff):")
                for lxy_label in lxy_labels:
                    cf.append('')
                    cf += _sb_table_lines(
                        cells_by_lxy[lxy_label], keys,
                        f"S and B entering each significance "
                        f"(lxy in {lxy_label.replace('to', '-')} cm):")

                cutflow_txt = '\n'.join(cf)
                cf_path = _mp_dir(mpi_val, mA_val) / f'cutflow_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{OUT_TAG}.txt'
                cf_path.write_text(cutflow_txt + '\n')


# The significance-vs-ctau overlay (MinBias + QCD) is now produced inline by
# _significance_vs_ctau_plot in --bkg both mode, so no separate combined pass is needed.
