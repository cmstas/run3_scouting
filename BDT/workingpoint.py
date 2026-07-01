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
_parser.add_argument("--bkg-rej", type=float, nargs="+", default=[0.9, 0.99, 0.999, 0.9999],
                     help="Target background rejection(s); one set of WP plots is produced per "
                          "value (0.90 = 90%%). The BDT is trained once and reused for all of them.")
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
_args = _parser.parse_args()

WP_TARGETS           = list(_args.bkg_rej)
BKG_REJECTION_TARGET = WP_TARGETS[0]

use_conditional      = _args.conditional
model_tag            = _args.model_tag
MASS_WINDOW_GEV      = _args.mass_window_gev  # absolute SV1 mass window half-width [GeV] around mA
MASS_WINDOW_REL      = _args.mass_window_rel  # relative half-width (fraction of mA); takes precedence
MASS_WINDOW_ACTIVE   = bool((MASS_WINDOW_REL and MASS_WINDOW_REL > 0.0) or
                            (MASS_WINDOW_GEV and MASS_WINDOW_GEV > 0.0))

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

# NOTE: the cascade BR (psi psi -> ... -> A'A' -> mumu, with B(A'->mumu)=0.317,
# B(pi3->A'A')=1) is simulated in the signal gen fragment, so it is ALREADY folded into
# eff_S = n_pass / N_gen by the MC. It must therefore NOT be applied as an external yield
# factor (doing so double-counts the decay). The signal yield uses only
# sigma_ggH * B(H->psipsi) = SIG_XSEC_PB. This dict is kept only as the set of validated
# signal points; its values (old HepData per-point numbers) are no longer used in the yield.
SIG_BR = {
    (4.0,  1.33, 0.1):   0.012003,
    (4.0,  1.33, 1.0):   0.00083178,
    (4.0,  1.33, 10.0):  0.00069306,
    (4.0,  1.33, 100.0): 0.0052651,
    (4.0,  0.40, 0.1):   0.0039587,
    (4.0,  0.40, 1.0):   0.00078883,
    (4.0,  0.40, 10.0):  0.0044838,
    (4.0,  0.40, 100.0): 0.060461,
    # (10.0, 1.0, *): not in HepData
    (1.0,  0.33, 0.1):   0.02281,
    (1.0,  0.33, 1.0):   0.0029828,
    (1.0,  0.33, 10.0):  0.016743,
    (1.0,  0.33, 100.0): 0.14464,
}

# Number of generated events per signal point (mpi, mA, ctau) -> N_gen
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

# Per-point BR(A'->mu mu), read from the signal gen fragments (normalized addChannel
# branching ratios). REFERENCE / annotation ONLY -- it is already folded into
# eff_S = n_pass/N_gen by the generator, so it is NOT applied as an external yield
# factor (doing so would double-count; see the note above ~L111). Keyed by (mpi, mA).
BR_A_MUMU = {
    (1.0,  0.33): 0.464,   # 0.458/0.988
    (4.0,  0.40): 0.440,   # 0.436/0.992
    (2.0,  0.67): 0.193,   # not in current tuples
    (10.0, 1.00): 0.307,   # 0.293/0.95343
    (4.0,  1.33): 0.317,   # 0.305/0.9623
}

# Trigger label shown in the significance-plot header.
TRIGGER_LABEL = "Scouting Asymptotic Significance"

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
    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root":            1.036e7,  # GenXSecAnalyzer after-filter (DoubleMuOS43), weighted eff 1.852e-4; 2026-06-26
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
    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root":            409318867,  # DAS nevents (2026-06-18)
}

# Fraction of the full generated sample contained in the on-disk tuple. The MinBias
# file shipped to workers is a PRE-SKIM of the original ~30 GB tuple (the first 1/6 of
# its entries, ~5 GB; see skim_minbias.C), so it holds only ~0.1667 of the sample. The
# file is read in full; this fraction enters only the yield math (frac*N_gen denominator
# and the 1/frac count scaling) so the cross-section normalization stays unbiased.
# Files not listed default to 1.0. Re-skim -> update this to the printed fraction.
BKG_FRACTION = {
    "tuples_MinBias_Fil-DoubleMuOS43_2024_2024.root": 0.1667,
}

def _bkg_fraction(fname):
    return BKG_FRACTION.get(fname, 1.0)

def _eff_ngen(fname):
    """Effective generated-event denominator for the loaded subsample: frac * N_gen.
    Using this everywhere N_gen enters the yield keeps subsampling unbiased."""
    return _bkg_fraction(fname) * BKG_NGEN[fname]

PB_TO_FB = 1.0e3   # 1 pb = 1000 fb (for the QCD background cross sections)

_HERE      = Path(__file__).resolve().parent
tuples_dir = _HERE.parent / "tuples_parking_nochi2"

# Filename suffix tagging the background set used (appended to every plot/table).
OUT_TAG = "_minBias"

FIGSIZE     = (8.5, 6.5)
N_BINS      = 50
MASS_COLORS = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#e377c2"]
BKG_FACE    = "#7fc7c4"
BKG_EDGE    = "#2f5f5d"
WP_COLOR    = "#9467bd"

_SIG_RE = re.compile(r"tuples_Signal_ScenarioA_Par_2024_mpi-(\w+)_mA-(\w+)_ctau-(\w+)mm_2024\.root")

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
        "ecalIso", "ecalRelIso", "eta", "hcalIso", "hcalRelIso",
        "isGlobal", "isTracker", "isvtx", "maxdr", "mindr",
        "muCSCDT", "muChambs", "muHits", "nhitsbeforesv", "normChi2",
        "phiCorr", "pixHits", "pixLayers", "pt", "stripHits",
        "trackIso", "trackRelIso", "trkLayers", "PFIsoAll0p3", "PFRelIsoAll0p3",
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
_LOAD_BRANCHES = list(dict.fromkeys(BDT_VARIABLES + ["SV1_lxy", "SV1_mass", "SV2_mass"]))

# ---------------------------------------------------------------------------
# Axis labels (only the variables plotted by _global_shape_plot)
# ---------------------------------------------------------------------------
AXIS_LABELS = {
    "SV1_lxy":  r"SV1 $l_{xy}$ (from PV) [cm]",
    "SV1_mass": r"SV1 $m_{\mu\mu}$ [GeV]",
}

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
def read_flat(path):
    with uproot.open(path) as f:
        t = f['tuples']
        available = set(t.keys())
        branches  = [b for b in _LOAD_BRANCHES if b in available]
        return t.arrays(branches, library='pd')

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
        denom = np.where(denom > 1e-9, denom, 1e-9)
        for mu in ("mu1", "mu2"):
            df[f"{sv}_{mu}_dxy_lxy"] = np.abs(df[f"{sv}_{mu}_dxy"]) / denom

sig_frames = []
for fpath, mpi_val, mA_val, ctau_val in sig_file_params:
    if not Path(fpath).exists():
        continue
    df = read_flat(fpath)
    df['param_ctau'] = float(ctau_val)
    df['param_mA']   = float(mA_val)
    df['param_mpi']  = float(mpi_val)
    df['label']      = 1
    sig_frames.append(df)
df_sig = pd.concat(sig_frames, ignore_index=True)

COMBINED_CELLS = {}
for BKG_FILES, OUT_TAG in [(MINBIAS_FILES, "_minBias"), (QCD_FILES, "_QCD")]:
    bkg_frames = []
    for fname in BKG_FILES:
        fpath = tuples_dir / fname
        if not fpath.exists():
            continue
        if BKG_XSEC.get(fname) is None or BKG_NGEN.get(fname) is None:
            continue
        df = read_flat(fpath)
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
    #lxy_bins   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]  # Match Scouting analysis
    #lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1", "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]
    lxy_bins   = [0.0, 1.0, 10.0, 100.0] # Match Parking analysis
    lxy_labels = ["0to1", "1to10", "10to100"]

    df_sig['lxy_bin'] = pd.cut(df_sig['SV1_lxy'], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
    df_bkg['lxy_bin'] = pd.cut(df_bkg['SV1_lxy'], bins=lxy_bins, labels=lxy_labels, include_lowest=True)

    available  = set(df_sig.columns) & set(df_bkg.columns)
    input_vars = [v for v in BDT_VARIABLES if v in available]
    missing    = [v for v in BDT_VARIABLES if v not in available]



    cond_vars = ['param_ctau', 'param_mA', 'param_mpi'] if use_conditional else []
    out_dir   = _HERE / f'working_point_{BKG_REJECTION_TARGET}'
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

    X_g = df_global[input_vars + cond_vars]
    y_g = df_global['label']
    w_g = compute_sample_weights(df_global)
    df_global['weight'] = w_g

    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        X_g, y_g, w_g, test_size=0.3, random_state=42, stratify=y_g)

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

    bkg_rej_curve = 1.0 - fpr

    # One set of WP outputs per target; BDT trained once above is reused.
    for BKG_REJECTION_TARGET in WP_TARGETS:
        out_dir = _HERE / ("working_point_" + str(BKG_REJECTION_TARGET))
        os.makedirs(out_dir, exist_ok=True)

        def _mp_dir(mpi_val, mA_val):
            """Per-mass-point output directory out_dir/mpi<X>/mA_<Y> (created)."""
            d = out_dir / f'mpi{_flabel(mpi_val)}' / f'mA_{_flabel(mA_val)}'
            os.makedirs(d, exist_ok=True)
            return d

        idx = int(np.argmin(np.abs(bkg_rej_curve - BKG_REJECTION_TARGET)))
        wp_threshold = thresholds[idx]
        wp_sig_eff = tpr[idx]
        wp_bkg_rej = bkg_rej_curve[idx]


        # ---------------------------------------------------------------------------
        # ROC curve (with WP)
        # ---------------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
        ax.plot(fpr, tpr, color='#1f77b4', linewidth=2.0, label=f'Global BDT (AUC = {auc:.3f})')
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, linewidth=1.0)
        ax.scatter([1.0 - wp_bkg_rej], [wp_sig_eff], color=WP_COLOR, s=80, zorder=5,
                   label=rf'WP: {wp_bkg_rej:.0%} bkg rej., {wp_sig_eff:.1%} sig eff.')
        ax.axvline(1.0 - wp_bkg_rej, color=WP_COLOR, linestyle='--', linewidth=1.0, alpha=0.6)
        ax.axhline(wp_sig_eff,        color=WP_COLOR, linestyle='--', linewidth=1.0, alpha=0.6)
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Global BDT ROC curve')
        ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
        ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes, fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
        ax.tick_params(direction="in", top=True, right=True, which="both")
        fig.savefig(out_dir / f'ROC_globalBDT_WP{OUT_TAG}.png', dpi=150, bbox_inches='tight')
        plt.close(fig)

        # ---------------------------------------------------------------------------
        # Score all events and apply WP cut
        # ---------------------------------------------------------------------------
        X_all              = df_global[input_vars + cond_vars]
        df_global          = df_global.copy()
        df_global['score'] = bdt.predict_proba(X_all)[:, 1]

        df_bkg_pass = df_global[(df_global['label'] == 0) & (df_global['score'] > wp_threshold)]
        df_bkg_all  = df_global[df_global['label'] == 0]
        w_all  = df_bkg_all['weight'].sum()
        w_pass = df_bkg_pass['weight'].sum()

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

            ax.axvline(wp_threshold, color=WP_COLOR, linestyle='--', linewidth=1.2, label=f'WP (score = {wp_threshold:.3f})', zorder=2)
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

        def _bkg_b_at(t, extra_mask=None):
            #xsec-weighted background yield with score > t
            base = (df_global['label'] == 0)
            if extra_mask is not None:
                base = base & extra_mask
            b = 0.0
            for fname in BKG_XSEC:
                if BKG_XSEC.get(fname) is None or BKG_NGEN.get(fname) is None:
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

        def _qcd_weighted(extra_mask=None):
            #Cross-section-weighted average event count
            base = (df_global['label'] == 0)
            if extra_mask is not None:
                base = base & extra_mask
            num = 0.0
            for f in _bkg_files_loaded:
                # Scale the loaded count to the full-sample equivalent (1/frac) so the
                # weighted-average count is comparable across subsampled/fully-loaded files.
                n_q = int((base & (df_global['bkg_file'] == f)).sum()) / _bkg_fraction(f)
                num += BKG_XSEC[f] * n_q
            return num / _sigma_sum if _sigma_sum > 0 else 0.0

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

            def _significance_vs_ctau_plot(cells, keys, ctaus, mpi_val, mA_val, lxy_label=None):
                if not ctaus:
                    return
                order = np.argsort(np.array(ctaus, dtype=float))
                x = np.array(ctaus, dtype=float)[order]
                fig, ax = plt.subplots(figsize=FIGSIZE)
                z_max = 0.0
                for i, (f_t, _f_ach, _thr) in enumerate(fpr_rows):
                    z = np.array([cells[(f_t, keys[j])][1] for j in range(len(keys))], dtype=float)[order]
                    z = np.nan_to_num(z, nan=0.0)
                    z_max = max(z_max, float(z.max()))
                    ax.plot(x, z, color=_FPR_COLORS[i % len(_FPR_COLORS)],
                            marker=_FPR_MARKERS[i % len(_FPR_MARKERS)], markersize=7, linewidth=1.8,
                            label=rf'FPR$=10^{{{int(round(np.log10(f_t)))}}}$', zorder=3 + i)
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
                ax.legend(loc='upper right', framealpha=0.9, fontsize=10, title_fontsize=11)
                ax.tick_params(direction='in', top=True, right=True, which='both')
                fig.tight_layout()
                _lxy_sfx = f'_lxy_{lxy_label}' if lxy_label is not None else ''
                _fout = _mp_dir(mpi_val, mA_val) / f'significance_vs_ctau_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{_lxy_sfx}{OUT_TAG}.png'
                fig.savefig(_fout, dpi=130)
                plt.close(fig)

            def _build_cells(keys, extra_mask=None):
                """cells[(f_t, key)] = (p0, Z, s, b) at each FPR threshold, optionally
                restricted to an extra mask (e.g. an lxy bin). Mass window always applied."""
                cells = {}
                for f_t, _f_ach, thr in fpr_rows:
                    for k in keys:
                        mwin = _combine_masks(_mass_window_mask(k), extra_mask)
                        s = _sig_s_at(k, thr, mwin)
                        b = _bkg_b_at(thr, _combine_masks(_bkg_param_mask(k), mwin))
                        if s is None or s <= 0.0 or b <= 0.0:
                            cells[(f_t, k)] = (float('nan'), 0.0, s, b)
                            continue
                        Z  = float(np.sqrt(2.0 * ((s + b) * np.log1p(s / b) - s)))
                        p0 = float(norm.sf(Z))
                        cells[(f_t, k)] = (p0, Z, s, b)
                return cells

            def _write_asimov_tex(cells, keys, ctaus, mpi_val, mA_val, lxy_label=None):
                """Write the booktabs Asimov p0(Z) table for these cells. When lxy_label
                is given, the lxy range is added to the header and the file name suffix."""
                hdr = _hdr
                if lxy_label is not None:
                    hdr = _hdr + rf'  [$l_{{xy}}\in {lxy_label.replace("to", "-")}$ cm]'
                tex = []
                tex.append(r'\begin{tabular}{l c ' + 'c ' * len(ctaus) + r'}')
                tex.append(r'\toprule')
                tex.append(r'\multicolumn{' + str(2 + len(ctaus)) + r'}{l}{' + hdr + r'} \\')
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
                _lxy_sfx = f'_lxy_{lxy_label}' if lxy_label is not None else ''
                tex_path = _mp_dir(mpi_val, mA_val) / f'asimov_table_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{_lxy_sfx}{OUT_TAG}.tex'
                tex_path.write_text('\n'.join(tex) + '\n')

            def _sb_table_lines(cells, keys, header):
                """Text block listing the actual S and B (xsec*lumi-weighted yields) that
                feed each significance, one sub-block per FPR threshold."""
                lines = [header]
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
                # Gate only on SIG_NGEN (needed for the yield); SIG_BR's values are no longer
                # used in the yield, so don't require membership in it -- otherwise points
                # absent from SIG_BR (e.g. mpi=10, mA=1.0) would be silently dropped.
                keys = [(mpi_val, mA_val, c) for c in sorted(ctau_vals)
                        if (mpi_val, mA_val, c) in SIG_NGEN]
                if not keys:
                    continue

                cells = _build_cells(keys)
                ctaus = [k[2] for k in keys]

                # Inclusive LaTeX table + significance vs ctau plot.
                _write_asimov_tex(cells, keys, ctaus, mpi_val, mA_val)
                _significance_vs_ctau_plot(cells, keys, ctaus, mpi_val, mA_val)

                # Same table + plot per lxy bin; keep the per-bin cells for the cutflow below.
                cells_by_lxy = {}
                for lxy_label in lxy_labels:
                    cells_lxy = _build_cells(keys, df_global['lxy_bin'] == lxy_label)
                    cells_by_lxy[lxy_label] = cells_lxy
                    _write_asimov_tex(cells_lxy, keys, ctaus, mpi_val, mA_val, lxy_label=lxy_label)
                    _significance_vs_ctau_plot(cells_lxy, keys, ctaus, mpi_val, mA_val, lxy_label=lxy_label)

                COMBINED_CELLS.setdefault((mpi_val, mA_val), {})[OUT_TAG] = (
                    list(keys), list(ctaus), dict(cells),
                    {lx: dict(cv) for lx, cv in cells_by_lxy.items()})
                #Cutflow: signal raw counts + QCD weighted-average count (no lumi)
                cf = []
                cf.append("Cutflow  (signal: raw event counts; "
                          "QCD: weighted = sum_q sigma_q N_q / sum_q sigma_q, no lumi)")
                cf.append(f'mpi = {mpi_val:g} GeV, mA = {mA_val:g} GeV   '
                          f'(BDT WP: score > {wp_threshold:.4f})')
                cw  = 16
                hdr = f'{"stage":>16}' + ''.join(f'{("ctau="+format(c,"g")+"mm"):>{cw}}' for c in ctaus) + f'{"QCD (wgt)":>{cw}}'
                cf.append(hdr)
                cf.append('-' * len(hdr))
                wp_mask = (df_global['score'] > wp_threshold)
                for stage_label, stage_mask in [("ntuple", None), ("BDT WP", wp_mask)]:
                    row = f'{stage_label:>16}'
                    for k in keys:
                        row += f'{_sig_count(k, stage_mask):>{cw}}'
                    row += f'{_qcd_weighted(stage_mask):>{cw}.1f}'
                    cf.append(row)

                if MASS_WINDOW_ACTIVE:
                    cf.append('')
                    cf.append("SV1 mass window (per ctau; QCD weighted within that point's window):")
                    sub = (f'{"ctau":>10} {"sig(win)":>12} {"sig(win+BDT)":>14} '
                           f'{"QCD wgt(win)":>16} {"QCD wgt(win+BDT)":>18}')
                    cf.append(sub)
                    cf.append('-' * len(sub))
                    for k in keys:
                        mwin   = _mass_window_mask(k)
                        win_wp = _combine_masks(mwin, wp_mask)
                        cf.append(f'{format(k[2],"g")+"mm":>10} '
                                  f'{_sig_count(k, mwin):>12} {_sig_count(k, win_wp):>14} '
                                  f'{_qcd_weighted(mwin):>16.1f} {_qcd_weighted(win_wp):>18.1f}')

                # Actual S and B (xsec*lumi-weighted yields) feeding each significance,
                # at every FPR threshold -- inclusive, then one block per lxy bin. The
                # mass window (if active) is already folded into these yields.
                cf.append('')
                cf += _sb_table_lines(
                    cells, keys,
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

        # ---------------------------------------------------------------------------
        # Normalized signal vs background shape after WP, per (mpi, mA) mass point,
        # restricted to that point's SV1 dimuon mass window. Saved in the mass-point dir.
        # ---------------------------------------------------------------------------
        def _masspoint_shape_plot(var, title, mpi_val, mA_val, ctau_vals, plot_dir, mwin_mask):
            # Background: passing WP and inside this mass point's SV1 mass window.
            b_base = (df_global['label'] == 0) & (df_global['score'] > wp_threshold)
            if mwin_mask is not None:
                b_base = b_base & mwin_mask
            b_arr = df_global.loc[b_base, var].values.astype(float)
            b_arr = b_arr[np.isfinite(b_arr)]

            sig_lines = []   # list of (label, array)
            for ctau_val in sorted(ctau_vals):
                mask = (
                    (df_global['label']      == 1) &
                    (df_global['param_ctau'] == ctau_val) &
                    (df_global['param_mA']   == mA_val) &
                    (df_global['param_mpi']  == mpi_val) &
                    (df_global['score']      > wp_threshold)
                )
                if mwin_mask is not None:
                    mask = mask & mwin_mask
                arr = df_global[mask][var].values.astype(float)
                arr = arr[np.isfinite(arr)]
                if len(arr) > 0:
                    sig_lines.append((rf'$c\tau={ctau_val:g}$ mm', arr))

            if not sig_lines or b_arr.size == 0:
                return
            all_vals = np.concatenate([b_arr] + [a for _, a in sig_lines])
            lo = np.percentile(all_vals, 1)
            hi = np.percentile(all_vals, 99)
            if lo == hi:
                return

            hb, edges = np.histogram(b_arr, bins=N_BINS, range=(lo, hi))
            hb_norm   = hb / hb.sum() if hb.sum() > 0 else hb.astype(float)
            widths    = np.diff(edges)

            fig, ax = plt.subplots(figsize=FIGSIZE)
            ax.bar(edges[:-1], hb_norm, width=widths, align='edge',
                   color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6,
                   label=f'Background (score > {wp_threshold:.3f})', zorder=1)

            for i, (lbl, arr) in enumerate(sig_lines):
                hs, _ = np.histogram(arr, bins=N_BINS, range=(lo, hi))
                if hs.sum() > 0:
                    hs = hs / hs.sum()
                ax.stairs(hs, edges, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.2, label=lbl, zorder=3 + i)

            pos = hb_norm[hb_norm > 0]
            if pos.size > 0:
                ax.set_yscale('log')
                ax.set_ylim(bottom=max(pos.min() * 0.3, 1e-6))

            ax.set_xlabel(AXIS_LABELS.get(var, var))
            ax.set_ylabel('a.u.')
            ax.set_title(title)
            ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes, fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
            ax.legend(loc='best', framealpha=0.9, fontsize=8)
            ax.tick_params(direction="in", top=True, right=True, which="both")
            fig.tight_layout()
            _fout = plot_dir / f'{var}_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}{OUT_TAG}.png'
            fig.savefig(_fout, dpi=130)
            plt.close(fig)

        for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
            plot_dir_g = _mp_dir(mpi_val, mA_val)
            # Mass window depends only on mA, so any ctau key for this point works.
            mwin_mask = _mass_window_mask((mpi_val, mA_val, sorted(ctau_vals)[0]))
            _win_txt = (' (' + _win_label_str() + ')') if MASS_WINDOW_ACTIVE else ''
            _masspoint_shape_plot(
                'SV1_lxy',
                rf'$m_A={mA_val:g}$ GeV{_win_txt}, {BKG_REJECTION_TARGET:.0%} bkg rej. WP',
                mpi_val, mA_val, ctau_vals, plot_dir_g, mwin_mask)
            _masspoint_shape_plot(
                'SV1_mass',
                rf'$m_A={mA_val:g}$ GeV{_win_txt}, {BKG_REJECTION_TARGET:.0%} bkg rej. WP',
                mpi_val, mA_val, ctau_vals, plot_dir_g, mwin_mask)


# ---------------------------------------------------------------------------
# Combined significance: MinBias (solid) + QCD (dashed) overlaid, 8 lines
# (4 FPR targets x 2 backgrounds). No _minBias/_QCD suffix on these.
# ---------------------------------------------------------------------------
from matplotlib.lines import Line2D

_FPR_COLORS_C  = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]
_FPR_MARKERS_C = ["o", "s", "^", "D", "v"]
_BKG_STYLE_C   = [("_minBias", "-", "MinBias"), ("_QCD", "--", "QCD")]

def _combined_significance_plot(mpi_val, mA_val, out_path, lxy_label=None):
    data = COMBINED_CELLS.get((mpi_val, mA_val), {})
    if "_minBias" not in data or "_QCD" not in data:
        return
    keys_ref, ctaus_ref, _c, _l = data["_minBias"]
    if not ctaus_ref:
        return
    order = np.argsort(np.array(ctaus_ref, dtype=float))
    x = np.array(ctaus_ref, dtype=float)[order]
    fpr_targets = sorted(_args.fpr_targets, reverse=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    z_max = 0.0
    for i, f_t in enumerate(fpr_targets):
        for tag, ls, _lbl in _BKG_STYLE_C:
            keys_t, _ct, cells_incl, cells_lxy = data[tag]
            cell_src = cells_incl if lxy_label is None else cells_lxy.get(lxy_label, {})
            try:
                z = np.array([cell_src[(f_t, keys_ref[j])][1]
                              for j in range(len(keys_ref))], dtype=float)[order]
            except KeyError:
                continue
            z = np.nan_to_num(z, nan=0.0)
            if z.size:
                z_max = max(z_max, float(z.max()))
            ax.plot(x, z, color=_FPR_COLORS_C[i % len(_FPR_COLORS_C)], linestyle=ls,
                    marker=_FPR_MARKERS_C[i % len(_FPR_MARKERS_C)], markersize=6,
                    linewidth=1.7, zorder=3 + i)
    ax.set_xscale('log')
    ax.set_xlabel(r'$c\tau$ [mm]')
    ax.set_ylabel(r'Asymptotic significance $Z$')
    ax.set_ylim(0.0, z_max * 1.45 if z_max > 0 else 1.0)
    ax.text(0.0, 1.01, TRIGGER_LABEL, transform=ax.transAxes, ha='left', va='bottom',
            fontweight='bold', fontsize=13)
    ax.text(1.0, 1.01, rf'{LUMI_FB:g} fb$^{{-1}}$ (13.6 TeV, 2024)', transform=ax.transAxes,
            ha='right', va='bottom', fontsize=12)
    txt = [rf'Scenario {model_tag}', rf'$m_{{\pi_3}} = {mpi_val:g}$ GeV',
           rf"$m_{{A'}} = {mA_val:g}$ GeV"]
    br = BR_A_MUMU.get((mpi_val, mA_val))
    if br is not None:
        txt.append(rf"$B(A'\to\mu\mu) = {br:g}$")
    if MASS_WINDOW_ACTIVE:
        half = _mass_window_halfwidth(mA_val)
        txt.append(rf'Mass window: $[{mA_val-half:.2f}, {mA_val+half:.2f}]$ GeV')
    if lxy_label is not None:
        txt.append(rf'$l_{{xy}} \in {lxy_label.replace("to", "-")}$ cm')
    ax.text(0.04, 0.96, '\n'.join(txt), transform=ax.transAxes, va='top', ha='left', fontsize=11)

    fpr_handles = [Line2D([0], [0], color=_FPR_COLORS_C[i % len(_FPR_COLORS_C)],
                          marker=_FPR_MARKERS_C[i % len(_FPR_MARKERS_C)], linestyle='-',
                          label=rf'FPR$=10^{{{int(round(np.log10(f_t)))}}}$')
                   for i, f_t in enumerate(fpr_targets)]
    bkg_handles = [Line2D([0], [0], color='k', linestyle=ls, label=lbl)
                   for _t, ls, lbl in _BKG_STYLE_C]
    leg1 = ax.legend(handles=fpr_handles, loc='upper right', framealpha=0.9, fontsize=10)
    ax.add_artist(leg1)
    ax.legend(handles=bkg_handles, loc='center right', framealpha=0.9, fontsize=10)
    ax.tick_params(direction='in', top=True, right=True, which='both')
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)

for _wp_target in WP_TARGETS:
    _base = _HERE / ("working_point_" + str(_wp_target))
    for (_mpi_val, _mA_val) in sorted(COMBINED_CELLS.keys()):
        _d = _base / f'mpi{_flabel(_mpi_val)}' / f'mA_{_flabel(_mA_val)}'
        os.makedirs(_d, exist_ok=True)
        _stem = f'significance_vs_ctau_mpi{_flabel(_mpi_val)}_mA{_flabel(_mA_val)}'
        _combined_significance_plot(_mpi_val, _mA_val, _d / f'{_stem}_combined.png')
        for _lxy_label in lxy_labels:
            _combined_significance_plot(_mpi_val, _mA_val,
                                        _d / f'{_stem}_lxy_{_lxy_label}_combined.png',
                                        lxy_label=_lxy_label)
