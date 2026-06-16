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
_parser.add_argument("--bkg-rej", type=float, default=0.90,
                     help="Target background rejection for the working point (0.90 = 90%%).")
_parser.add_argument("--wp-score", type=float, default=None,
                     help="Set the BDT score threshold directly, overriding --bkg-rej.")
_parser.add_argument("--model-tag", default="A", help="Signal scenario tag for output naming.")
_parser.add_argument("--weigh-bkg", action=argparse.BooleanOptionalAction, default=True,
                     help="Apply cross-section (sigma/N_gen) weights to background events in "
                          "training, the WP/ROC determination and the per-lxy breakdown. "
                          "Use --no-weigh-bkg to treat all background events with unit weight.")
_args = _parser.parse_args()

BKG_REJECTION_TARGET = _args.bkg_rej   # 0.90 = 90% background rejection
WP_SCORE_OVERRIDE    = _args.wp_score  # if set, used directly as the BDT threshold
use_conditional      = False
model_tag            = _args.model_tag
WEIGH_BKG            = _args.weigh_bkg  # cross-section weight the background?

LUMI_FB = 110.0 # 2024 Luminosity

# PLACEHOLDER signal production cross section [pb] -- NOT physical. Used only to
# scale the Asimov signal yield for sensitivity tests (SIG_BR holds dimensionless
# branching fractions). Replace with the real production xsec (e.g. SM ggH) before
# quoting any significance.
SIG_XSEC_PB = 1.0

# Signal BRANCHING FRACTION from HepData (https://www.hepdata.net/record/ins3083980?version=1)
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

BKG_FILES = [
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
}
PB_TO_FB = 1.0e3   # 1 pb = 1000 fb (for the QCD background cross sections)

_HERE      = Path(__file__).resolve().parent
tuples_dir = _HERE.parent / "tuples_parking_nochi2"

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
print(f"Found {len(sig_file_params)} signal files")


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
# Axis labels — mirrors plotsignalvsbkg.py
# ---------------------------------------------------------------------------
_SV_STEM_LABELS = {
    "ptmm":         r"$p_{T}^{\mu\mu}$ [GeV]",
    "prob":         r"SV $\chi^{2}$ probability",
    "x":            r"SV $x$ [cm]",
    "y":            r"SV $y$ [cm]",
    "z":            r"SV $z$ [cm]",
    "lxy":          r"$l_{xy}$ (from PV) [cm]",
    "xErr":         r"SV $x$ error [cm]",
    "yErr":         r"SV $y$ error [cm]",
    "zErr":         r"SV $z$ error [cm]",
    "dphi_mumu_SV": r"$|\Delta\phi(\vec{\mu\mu},\,\vec{SV})|$ [rad]",
    "d3d_mumu_SV":  r"3D angle$(\vec{\mu\mu},\,\vec{SV})$ [rad]",
    "a3d_mumu":     r"3D angle$(\mu,\,\mu)$ [rad]",
    "mass":         r"$m_{\mu\mu}$ [GeV]",
    "chi2Ndof":     r"SV $\chi^{2}$/ndof",
    "l3d":          r"$l_{3D}$ (from PV) [cm]",
    "dr_mumu":      r"$\Delta R(\mu,\mu)$",
    "dphi_mumu":    r"$\Delta\phi(\mu,\mu)$ [rad]",
    "deta_mumu":    r"$\Delta\eta(\mu,\mu)$",
    "deta_mumu_SV": r"$\Delta\eta(\mu\mu,\mathrm{SV})$",
    "sindphi_lxy":  r"$\sin(\Delta\phi) \cdot l_{xy}$",
}

_MU_STEM_LABELS = {
    "pt":           r"Muon $p_{T}$ [GeV]",
    "eta":          r"Muon $\eta$",
    "phiCorr":      r"Muon $\phi$ corrected [rad]",
    "isvtx":        r"Muon is from vertex",
    "normChi2":     r"Muon $\chi^{2}$/ndof",
    "dxy":          r"Muon $|d_{xy}|$ [cm]",
    "dxysig":       r"Muon $|d_{xy}|/\sigma_{xy}$",
    "dxy_lxy":      r"Muon $|d_{xy}|/l_{xy}$ (scaled)",
    "dz":           r"Muon $|d_{z}|$ [cm]",
    "dzsig":        r"Muon $|d_{z}|/\sigma_{z}$",
    "nhitsbeforesv":r"Hits before SV",
    "isGlobal":     r"Muon isGlobal",
    "isTracker":    r"Muon isTracker",
    "pixHits":      r"Pixel hits",
    "stripHits":    r"Strip hits",
    "pixLayers":    r"Pixel layers",
    "trkLayers":    r"Tracker layers",
    "muHits":       r"Muon hits",
    "muChambs":     r"Muon chambers",
    "muCSCDT":      r"CSC/DT chambers",
    "ecalIso":      r"ECAL isolation [GeV]",
    "hcalIso":      r"HCAL isolation [GeV]",
    "trackIso":     r"Track isolation [GeV]",
    "ecalRelIso":   r"ECAL isolation / $p_{T}$",
    "hcalRelIso":   r"HCAL isolation / $p_{T}$",
    "trackRelIso":  r"Track isolation / $p_{T}$",
    "PFIsoAll0p3":  r"PF-all iso. ($\Delta R<0.3$) [GeV]",
    "PFRelIsoAll0p3": r"PF-all rel. iso. ($\Delta R<0.3$)",
    "mindr":        r"min $\Delta R(\mu_{i},\mu_{j})$",
    "maxdr":        r"max $\Delta R(\mu_{i},\mu_{j})$",
}

def _build_axis_labels():
    labels = {}
    for sv in ("SV1", "SV2"):
        for stem, label in _SV_STEM_LABELS.items():
            labels[f"{sv}_{stem}"] = f"{sv} {label}"
        for mu in ("mu1", "mu2"):
            for stem, label in _MU_STEM_LABELS.items():
                labels[f"{sv}_{mu}_{stem}"] = f"{sv} {mu} {label}"
    return labels

AXIS_LABELS = _build_axis_labels()

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
    if WEIGH_BKG:
        # Cross-section reweighting for background: each event weighted by sigma / N_gen
        # (no luminosity -- only the relative normalization across the QCD pT bins matters).
        # The 'xsec_weight' column is set at load time.
        w[bkg_mask] = df.loc[bkg_mask, 'xsec_weight'].values
    # else: background stays at unit weight.

    # Class balancing: scale signal so total signal weight == total background weight.
    n_sig   = int((y == 1).sum())
    sum_bkg = float(w[bkg_mask].sum())
    if n_sig > 0 and sum_bkg > 0:
        w[y == 1] = sum_bkg / n_sig
    return w

def asimov_z(sig_eff, br_sig, bkg_effs):
    """Asimov median discovery significance: Z = sqrt(2((s+b)ln(1+s/b) - s)).

    Yields are built here from cross sections, luminosity and WP acceptances:
        s = SIG_XSEC_PB * PB_TO_FB * BR * LUMI_FB * sig_eff
        b = sum_bins  sigma_bin[pb] * PB_TO_FB * LUMI_FB * bkg_acceptance

    sig_eff  : signal acceptance at the WP (n_pass / N_gen)
    br_sig   : signal branching fraction (dimensionless)
    bkg_effs : dict {bkg filename: WP acceptance (n_pass / N_gen) for that bkg}
    """
    s = SIG_XSEC_PB * PB_TO_FB * br_sig * LUMI_FB * sig_eff
    b = sum(BKG_XSEC[f] * PB_TO_FB * LUMI_FB * bkg_acceptance for f, bkg_acceptance in bkg_effs.items())
    if b <= 0.0 or s <= 0.0:
        return 0.0
    return float(np.sqrt(2.0 * ((s + b) * np.log1p(s / b) - s)))

def add_dxy_lxy(df):
    for sv in ("SV1", "SV2"):
        denom = df[f"{sv}_lxy"] * df[f"{sv}_mass"] / df[f"{sv}_ptmm"]
        denom = np.where(denom > 1e-9, denom, 1e-9)
        for mu in ("mu1", "mu2"):
            df[f"{sv}_{mu}_dxy_lxy"] = np.abs(df[f"{sv}_{mu}_dxy"]) / denom

print('Loading signal...')
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
    print(f'  sig mpi={mpi_val} mA={mA_val} ctau={ctau_val}: {len(df)} events')
df_sig = pd.concat(sig_frames, ignore_index=True)

print('Loading background...')
bkg_frames = []
for fname in BKG_FILES:
    fpath = tuples_dir / fname
    if not fpath.exists():
        continue
    df = read_flat(fpath)
    df['label'] = 0
    df['bkg_file'] = fname
    # Cross-section reweighting (no lumi): per-event weight = sigma / N_gen.
    df['xsec_weight'] = BKG_XSEC[fname] / BKG_NGEN[fname]
    bkg_frames.append(df)
    if WEIGH_BKG:
        print(f'  bkg {fname}: {len(df)} events ({df["xsec_weight"].sum():.4g} xsec-weighted)')
    else:
        print(f'  bkg {fname}: {len(df)} events')

df_bkg = pd.concat(bkg_frames, ignore_index=True)

add_dxy_lxy(df_sig)
add_dxy_lxy(df_bkg)

# ---------------------------------------------------------------------------
# Lxy binning (cm)
# ---------------------------------------------------------------------------
# lxy_bins   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]  # Match Scouting analysis
# lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1", "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]
lxy_bins   = [0.0, 1.0, 10.0, 100.0] # Match Parking analysis
lxy_labels = ["0to1", "1to10", "10to100"]

df_sig['lxy_bin'] = pd.cut(df_sig['SV1_lxy'], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_bkg['lxy_bin'] = pd.cut(df_bkg['SV1_lxy'], bins=lxy_bins, labels=lxy_labels, include_lowest=True)

available  = set(df_sig.columns) & set(df_bkg.columns)
input_vars = [v for v in BDT_VARIABLES if v in available]
missing    = [v for v in BDT_VARIABLES if v not in available]

if missing:
    print(f'\nWARNING: {len(missing)} BDT variables missing from tuples')
print(f'Using {len(input_vars)} BDT input variables')


cond_vars = ['param_ctau', 'param_mA', 'param_mpi'] if use_conditional else []
cond_tag  = 'conditional' if use_conditional else 'non_cond'
out_dir   = _HERE / f'working_point_{BKG_REJECTION_TARGET}'
os.makedirs(out_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Train global BDT
# ---------------------------------------------------------------------------
print(f'\nTraining global BDT... (background weighting: '
      f'{"sigma/N_gen (xsec)" if WEIGH_BKG else "OFF -- unit weight"})')
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
if WP_SCORE_OVERRIDE is not None:
    wp_threshold = WP_SCORE_OVERRIDE
    idx          = int(np.argmin(np.abs(thresholds - wp_threshold)))
    print(f'\nWorking point (BDT score fixed at {wp_threshold:.4f}):')
else:
    idx          = int(np.argmin(np.abs(bkg_rej_curve - BKG_REJECTION_TARGET)))
    wp_threshold = thresholds[idx]
    print(f'\nWorking point (target bkg rejection = {BKG_REJECTION_TARGET:.0%}):')
wp_sig_eff = tpr[idx]
wp_bkg_rej = bkg_rej_curve[idx]

print(f'  BDT score threshold : {wp_threshold:.4f}')
print(f'  Signal efficiency   : {wp_sig_eff:.3f}')
print(f'  Background rejection: {wp_bkg_rej:.3f}')

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
ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes,
        fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
ax.tick_params(direction="in", top=True, right=True, which="both")
fig.savefig(out_dir / 'ROC_globalBDT_WP.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print(f'\nSaved: {out_dir}/ROC_globalBDT_WP.png')

# ---------------------------------------------------------------------------
# Score all events and apply WP cut
# ---------------------------------------------------------------------------
print('\nScoring all events...')
X_all              = df_global[input_vars + cond_vars]
df_global          = df_global.copy()
df_global['score'] = bdt.predict_proba(X_all)[:, 1]

df_bkg_pass = df_global[(df_global['label'] == 0) & (df_global['score'] > wp_threshold)]
df_bkg_all  = df_global[df_global['label'] == 0]
print(f'Background: {len(df_bkg_all)} total, {len(df_bkg_pass)} pass WP '
      f'({len(df_bkg_pass)/len(df_bkg_all):.1%})')
if WEIGH_BKG:
    w_all  = df_bkg_all['weight'].sum()
    w_pass = df_bkg_pass['weight'].sum()
    print(f'            weighted (xsec): {w_all:.4g} total, {w_pass:.4g} pass WP '
          f'({w_pass/w_all:.1%})')

# ---------------------------------------------------------------------------
# Asimov significance at the working point  -- DISABLED for now (revisit later)
# ---------------------------------------------------------------------------
# def _bkg_effs(extra_mask=None):
#     """WP acceptance per background pT bin (n_pass / N_gen), optionally within an extra mask."""
#     effs = {}
#     for fname in BKG_XSEC:
#         sel = (df_global['label'] == 0) & (df_global['bkg_file'] == fname)
#         if extra_mask is not None:
#             sel = sel & extra_mask
#         n_pass = int((sel & (df_global['score'] > wp_threshold)).sum())
#         if n_pass == 0:
#             continue
#         effs[fname] = n_pass / BKG_NGEN[fname]
#     return effs
#
# bkg_effs_incl = _bkg_effs()
# bkg_effs_lxy  = {lbl: _bkg_effs(df_global['lxy_bin'] == lbl) for lbl in lxy_labels}
#
# print(f'\nAsimov significance at WP (lumi = {LUMI_FB:.0f}/fb, '
#       f'PLACEHOLDER sig xsec = {SIG_XSEC_PB:g} pb, BR from HepData limits):')
# print(f'{"mpi":>5} {"mA":>6} {"ctau":>7} | {"Z(incl)":>9} | {"Z(lxy 0to1)":>12}| {"Z(lxy 1to10)":>15}| {"Z(lxy 10to100)":>18}')
# print('-' * 50)
# for (mpi_val, mA_val, ctau_val), br in sorted(SIG_BR.items()):
#     sig_sel = ((df_global['label'] == 1) &
#                (df_global['param_mpi']  == mpi_val) &
#                (df_global['param_mA']   == mA_val) &
#                (df_global['param_ctau'] == ctau_val))
#     n_sig = int(sig_sel.sum())
#     if n_sig == 0:
#         continue
#     n_gen_sig = SIG_NGEN[(mpi_val, mA_val, ctau_val)]
#     sig_eff = int((sig_sel & (df_global['score'] > wp_threshold)).sum()) / n_gen_sig
#     z_incl  = asimov_z(sig_eff, br, bkg_effs_incl)
#     z0to1 = 0
#     z1to10 = 0
#     z10to100 = 0
#     for lxy_label in lxy_labels:
#         lxy_mask = df_global['lxy_bin'] == lxy_label
#         n_sig_b  = int((sig_sel & lxy_mask).sum())
#         if n_sig_b == 0:
#             continue
#         sig_eff_b = int((sig_sel & lxy_mask & (df_global['score'] > wp_threshold)).sum()) / n_gen_sig
#         if lxy_label=="0to1":
#             z0to1 = asimov_z(sig_eff_b, br, bkg_effs_lxy[lxy_label])
#         elif lxy_label=="1to10":
#             z1to10 = asimov_z(sig_eff_b, br, bkg_effs_lxy[lxy_label])
#         elif lxy_label=="10to100":
#             z10to100 = asimov_z(sig_eff_b, br, bkg_effs_lxy[lxy_label])
#     print(f'{mpi_val:>5g} {mA_val:>6g} {ctau_val:>7g} | {z_incl:>9.3f} | {z0to1:>1.3f} | {z1to10:>13.3f} | {z10to100:>15.3f}')

# ---------------------------------------------------------------------------
# Variable distributions after WP cut — one set of plots per (mpi, mA)
# ---------------------------------------------------------------------------
mpi_mA_groups = {}
for ctau_val, mA_val, mpi_val in param_grid:
    mpi_mA_groups.setdefault((mpi_val, mA_val), []).append(ctau_val)

for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
    plot_dir = out_dir / f'mpi{_flabel(mpi_val)}' / f'mA_{_flabel(mA_val)}'
    os.makedirs(plot_dir, exist_ok=True)

    sig_pass = {}
    for ctau_val in sorted(ctau_vals):
        mask = (
            (df_global['label']      == 1) &
            (df_global['param_ctau'] == ctau_val) &
            (df_global['param_mA']   == mA_val) &
            (df_global['param_mpi']  == mpi_val) &
            (df_global['score']      > wp_threshold)
        )
        n_total = int(((df_global['label'] == 1) &
                       (df_global['param_ctau'] == ctau_val) &
                       (df_global['param_mA']   == mA_val) &
                       (df_global['param_mpi']  == mpi_val)).sum())
        n_pass  = int(mask.sum())
        print(f'  mpi={mpi_val} mA={mA_val} ctau={ctau_val}: {n_pass}/{n_total} pass WP '
              f'({n_pass/n_total:.1%} sig eff.)' if n_total > 0 else '  no events')
        # Per-lxy-bin breakdown for this signal point
        for lxy_label in lxy_labels:
            bin_sel = (
                (df_global['label']      == 1) &
                (df_global['param_ctau'] == ctau_val) &
                (df_global['param_mA']   == mA_val) &
                (df_global['param_mpi']  == mpi_val) &
                (df_global['lxy_bin']    == lxy_label)
            )
            n_bin_total = int(bin_sel.sum())
            n_bin_pass  = int((bin_sel & (df_global['score'] > wp_threshold)).sum())
            if n_bin_total > 0:
                print(f'      lxy={lxy_label}: {n_bin_pass}/{n_bin_total} pass WP '
                      f'({n_bin_pass/n_bin_total:.1%} sig eff.)')
            else:
                print(f'      lxy={lxy_label}: no events')
        sig_pass[ctau_val] = df_global[mask]

    #plot_vars = [v for v in input_vars if v in AXIS_LABELS]
    plot_vars = []

    for var in plot_vars:
        b_arr = df_bkg_pass[var].values.astype(float) if var in df_bkg_pass.columns else np.array([])
        if b_arr.size == 0:
            continue

        sig_arrs = {ctau: df[var].values.astype(float)
                    for ctau, df in sig_pass.items()
                    if var in df.columns and len(df) > 0}
        if not sig_arrs:
            continue

        all_vals = np.concatenate([a[np.isfinite(a)] for a in [b_arr] + list(sig_arrs.values())])
        if len(all_vals) == 0:
            continue
        lo, hi = np.percentile(all_vals, 1), np.percentile(all_vals, 99)
        if lo == hi:
            lo, hi = all_vals.min(), all_vals.max()
        if lo == hi:
            continue

        b_fin  = b_arr[np.isfinite(b_arr)]
        hb, edges = np.histogram(b_fin, bins=N_BINS, range=(lo, hi))
        hb_norm   = hb / hb.sum() if hb.sum() > 0 else hb.astype(float)
        widths    = np.diff(edges)

        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.bar(edges[:-1], hb_norm, width=widths, align='edge',
               color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6,
               label=f'Background (score > {wp_threshold:.3f})', zorder=1)

        for i, (ctau_val, s_arr) in enumerate(sorted(sig_arrs.items())):
            s_fin = s_arr[np.isfinite(s_arr)]
            hs, _ = np.histogram(s_fin, bins=N_BINS, range=(lo, hi))
            if hs.sum() > 0:
                hs = hs / hs.sum()
            ax.stairs(hs, edges, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6,
                      label=rf'$c\tau = {ctau_val:g}$ mm', zorder=3 + i)

        pos = hb_norm[hb_norm > 0]
        if pos.size > 0:
            ax.set_yscale('log')
            ax.set_ylim(bottom=max(pos.min() * 0.3, 1e-6))

        ax.set_xlabel(AXIS_LABELS.get(var, var))
        ax.set_ylabel('a.u.')
        ax.set_title(var, fontsize=11)
        ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes,
                fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
        ax.legend(loc='best', framealpha=0.9,
                  title=(rf'$m_\pi={mpi_val:g}$ GeV, $m_A={mA_val:g}$ GeV'
                         f'\n{BKG_REJECTION_TARGET:.0%} bkg rej. WP'),
                  title_fontsize=9)
        ax.tick_params(direction="in", top=True, right=True, which="both")
        fig.tight_layout()
        fig.savefig(plot_dir / f'{var}.png', dpi=130)
        plt.close(fig)

    print(f'  Saved variable plots -> {plot_dir}/')

# ---------------------------------------------------------------------------
# Global SV1_lxy distribution after WP cut — all (mpi, mA, ctau) on one plot
# ---------------------------------------------------------------------------
_lxy_var    = 'SV1_lxy'
_lxy_xlabel = AXIS_LABELS.get(_lxy_var, _lxy_var)

b_lxy  = df_bkg_pass[_lxy_var].values.astype(float)
b_lxy  = b_lxy[np.isfinite(b_lxy)]

# Collect all signal arrays across every (mpi, mA, ctau)
_sig_lxy_lines = []   # list of (label, array)
for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
    for ctau_val in sorted(ctau_vals):
        mask = (
            (df_global['label']      == 1) &
            (df_global['param_ctau'] == ctau_val) &
            (df_global['param_mA']   == mA_val) &
            (df_global['param_mpi']  == mpi_val) &
            (df_global['score']      > wp_threshold)
        )
        arr = df_global[mask][_lxy_var].values.astype(float)
        arr = arr[np.isfinite(arr)]
        if len(arr) > 0:
            _sig_lxy_lines.append((
                rf'$m_\pi={mpi_val:g}$, $m_A={mA_val:g}$, $c\tau={ctau_val:g}$ mm',
                arr
            ))

if _sig_lxy_lines:
    all_lxy = np.concatenate([b_lxy] + [a for _, a in _sig_lxy_lines])
    lo = np.percentile(all_lxy, 1)
    hi = np.percentile(all_lxy, 99)

    hb, edges = np.histogram(b_lxy, bins=N_BINS, range=(lo, hi))
    hb_norm   = hb / hb.sum() if hb.sum() > 0 else hb.astype(float)
    widths    = np.diff(edges)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.bar(edges[:-1], hb_norm, width=widths, align='edge',
           color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6,
           label=f'Background (score > {wp_threshold:.3f})', zorder=1)

    for i, (lbl, arr) in enumerate(_sig_lxy_lines):
        hs, _ = np.histogram(arr, bins=N_BINS, range=(lo, hi))
        if hs.sum() > 0:
            hs = hs / hs.sum()
        ax.stairs(hs, edges, color=MASS_COLORS[i % len(MASS_COLORS)],
                  linewidth=1.2, label=lbl, zorder=3 + i)

    pos = hb_norm[hb_norm > 0]
    if pos.size > 0:
        ax.set_yscale('log')
        ax.set_ylim(bottom=max(pos.min() * 0.3, 1e-6))

    ax.set_xlabel(_lxy_xlabel)
    ax.set_ylabel('a.u.')
    ax.set_title(rf'$l_{{xy}}$ — all signal points, {BKG_REJECTION_TARGET:.0%} bkg rej. WP')
    ax.text(0.02, 0.97, "Preliminary", transform=ax.transAxes,
            fontsize=11, fontstyle="italic", fontweight="bold", va="top", ha="left")
    ax.legend(loc='best', framealpha=0.9, fontsize=7)
    ax.tick_params(direction="in", top=True, right=True, which="both")
    fig.tight_layout()
    fig.savefig(out_dir / 'SV1_lxy_global.png', dpi=130)
    plt.close(fig)
    print(f'Saved: {out_dir}/SV1_lxy_global.png')

# ---------------------------------------------------------------------------
# Signal efficiency & background rejection per lxy bin at the WP
# ---------------------------------------------------------------------------
_wgt_hdr = "bkg pass (xs-wgt)" if WEIGH_BKG else "bkg pass (unit-wgt)"
print(f'\n{"lxy bin":>14} | {"sig_eff":>8} | {"bkg_rej":>8} | '
      f'{"bkg pass (raw)":>16} | {_wgt_hdr:>20}')
print('-' * 80)

eff_data = []
for lxy_label in lxy_labels:
    sig_bin = df_global[(df_global['label'] == 1) & (df_global['lxy_bin'] == lxy_label)]
    bkg_bin = df_global[(df_global['label'] == 0) & (df_global['lxy_bin'] == lxy_label)]

    sig_eff = (sig_bin['score'] > wp_threshold).sum() / len(sig_bin) if len(sig_bin) > 0 else float('nan')
    n_bkg_total = len(bkg_bin)
    pass_mask   = bkg_bin['score'] > wp_threshold
    n_bkg_pass  = int(pass_mask.sum())
    if n_bkg_total > 0:
        # 'weight' already reflects WEIGH_BKG (xsec weights if on, unit weights if off).
        w_tot       = bkg_bin['weight'].sum()
        w_pass      = bkg_bin.loc[pass_mask, 'weight'].sum()
        bkg_rej_bin = 1.0 - w_pass / w_tot
    else:
        w_tot = w_pass = 0.0
        bkg_rej_bin = float('nan')
    print(f'{lxy_label:>14} | {sig_eff:>8.3f} | {bkg_rej_bin:>8.3f} | '
          f'{n_bkg_pass:>7}/{n_bkg_total:<8} | {w_pass:>9.4g}/{w_tot:<9.4g}')
    eff_data.append((lxy_label, sig_eff, bkg_rej_bin))

# Bar chart: sig eff and bkg rej per lxy bin
x        = np.arange(len(lxy_labels))
sig_effs = [d[1] for d in eff_data]
bkg_rejs = [d[2] for d in eff_data]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), constrained_layout=True, sharex=True)

ax1.bar(x, sig_effs, color='#1f77b4', edgecolor='#0a4b8a', linewidth=0.8)
ax1.axhline(wp_sig_eff, color='k', linestyle='--', linewidth=1.0, alpha=0.5,
            label=f'Global avg. ({wp_sig_eff:.1%})')
ax1.set_ylabel('Signal Efficiency')
ax1.set_ylim(0, 1.1)
ax1.legend(fontsize=9)
ax1.set_title(f'Working Point: {BKG_REJECTION_TARGET:.0%} background rejection  '
              f'(BDT score > {wp_threshold:.4f})')
ax1.tick_params(direction="in", top=True, right=True, which="both")

ax2.bar(x, bkg_rejs, color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.8)
ax2.axhline(BKG_REJECTION_TARGET, color='k', linestyle='--', linewidth=1.0, alpha=0.5,
            label=f'Target ({BKG_REJECTION_TARGET:.0%})')
ax2.set_ylabel('Background Rejection')
ax2.set_ylim(0, 1.05)
ax2.set_xticks(x)
ax2.set_xticklabels(lxy_labels, rotation=30, ha='right', fontsize=10)
ax2.legend(fontsize=9)
ax2.tick_params(direction="in", top=True, right=True, which="both")

fig.savefig(out_dir / 'WP_lxy_breakdown.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print(f'\nSaved: {out_dir}/WP_lxy_breakdown.png')