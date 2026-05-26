#!/usr/bin/env python3
"""Working point analysis for the scouting BDT.

Trains the global BDT, finds the BDT score threshold at a configurable
background rejection target, then plots input variable distributions for
events passing the working point cut (signal vs background).

Usage:
    python BDT/workingpoint.py
"""

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
BKG_REJECTION_TARGET = 0.90   # 0.90 = 90% background rejection
use_conditional      = False
model_tag            = 'A'

_HERE      = Path(__file__).resolve().parent
tuples_dir = _HERE.parent / "tuples"

FIGSIZE     = (8.5, 6.5)
N_BINS      = 50
MASS_COLORS = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#e377c2"]
BKG_FACE    = "#7fc7c4"
BKG_EDGE    = "#2f5f5d"
WP_COLOR    = "#9467bd"

# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------
_SIG_RE = re.compile(
    r"tuples_Signal_ScenarioA_Par_2024_mpi-(\w+)_mA-(\w+)_ctau-(\w+)mm_2024\.root"
)

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

BKG_FILES = [
    "tuples_QCD_Bin-PT-15to20_Fil-MuEnriched_2024_2024.root",
    "tuples_QCD_Bin-PT-20to30_Fil-MuEnriched_2024_2024.root",
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

def compute_class_weights(y):
    n_sig = (y == 1).sum()
    n_bkg = (y == 0).sum()
    return np.where(y == 1, n_bkg / n_sig, 1.0)

def add_dxy_lxy(df):
    for sv in ("SV1", "SV2"):
        denom = df[f"{sv}_lxy"] * df[f"{sv}_mass"] / df[f"{sv}_ptmm"]
        denom = np.where(denom > 1e-9, denom, 1e-9)
        for mu in ("mu1", "mu2"):
            df[f"{sv}_{mu}_dxy_lxy"] = np.abs(df[f"{sv}_{mu}_dxy"]) / denom

# ---------------------------------------------------------------------------
# Load signal
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Load background
# ---------------------------------------------------------------------------
print('Loading background...')
bkg_frames = []
for fname in BKG_FILES:
    fpath = tuples_dir / fname
    if not fpath.exists():
        continue
    df = read_flat(fpath)
    df['label'] = 0
    bkg_frames.append(df)
    print(f'  bkg {fname}: {len(df)} events')

df_bkg = pd.concat(bkg_frames, ignore_index=True)

add_dxy_lxy(df_sig)
add_dxy_lxy(df_bkg)

# ---------------------------------------------------------------------------
# Lxy binning
# ---------------------------------------------------------------------------
lxy_bins   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]
lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1",
              "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]

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
out_dir   = _HERE / f'workingpoint_OR_{model_tag}_{cond_tag}'
os.makedirs(out_dir, exist_ok=True)

# ---------------------------------------------------------------------------
# Train global BDT
# ---------------------------------------------------------------------------
print('\nTraining global BDT...')
df_global = pd.concat([df_sig, df_bkg], ignore_index=True)

X_g = df_global[input_vars + cond_vars]
y_g = df_global['label']
w_g = compute_class_weights(y_g.values)

X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
    X_g, y_g, w_g, test_size=0.3, random_state=42, stratify=y_g)

bdt = XGBClassifier(
    n_estimators=100, max_depth=3, learning_rate=0.1,
    use_label_encoder=False, eval_metric='logloss',
    tree_method='hist', n_jobs=4,
)
bdt.fit(X_train, y_train, sample_weight=w_train)
print('  Done.')

# ---------------------------------------------------------------------------
# Find working point
# ---------------------------------------------------------------------------
y_score = bdt.predict_proba(X_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_score)
auc = roc_auc_score(y_test, y_score)

bkg_rej_curve = 1.0 - fpr
idx           = np.argmin(np.abs(bkg_rej_curve - BKG_REJECTION_TARGET))
wp_threshold  = thresholds[idx]
wp_sig_eff    = tpr[idx]
wp_bkg_rej    = bkg_rej_curve[idx]

print(f'\nWorking point (target bkg rejection = {BKG_REJECTION_TARGET:.0%}):')
print(f'  BDT score threshold : {wp_threshold:.4f}')
print(f'  Signal efficiency   : {wp_sig_eff:.3f}')
print(f'  Background rejection: {wp_bkg_rej:.3f}')

# ---------------------------------------------------------------------------
# ROC curve with WP marked
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

# ---------------------------------------------------------------------------
# Variable distributions after WP cut — one set of plots per (mpi, mA)
# ---------------------------------------------------------------------------
mpi_mA_groups = {}
for ctau_val, mA_val, mpi_val in param_grid:
    mpi_mA_groups.setdefault((mpi_val, mA_val), []).append(ctau_val)

for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
    plot_dir = out_dir / f'mpi{_flabel(mpi_val)}' / f'mA_{_flabel(mA_val)}'
    os.makedirs(plot_dir, exist_ok=True)

    # Gather passed-signal per ctau
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
        sig_pass[ctau_val] = df_global[mask]

    plot_vars = [v for v in input_vars if v in AXIS_LABELS]

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
print(f'\n{"lxy bin":>14} | {"sig_eff":>8} | {"bkg_rej":>8}')
print('-' * 38)

eff_data = []
for lxy_label in lxy_labels:
    sig_bin = df_global[(df_global['label'] == 1) & (df_global['lxy_bin'] == lxy_label)]
    bkg_bin = df_global[(df_global['label'] == 0) & (df_global['lxy_bin'] == lxy_label)]

    sig_eff = (sig_bin['score'] > wp_threshold).sum() / len(sig_bin) if len(sig_bin) > 0 else float('nan')
    bkg_rej_bin = 1.0 - (bkg_bin['score'] > wp_threshold).sum() / len(bkg_bin) if len(bkg_bin) > 0 else float('nan')
    print(f'{lxy_label:>14} | {sig_eff:>8.3f} | {bkg_rej_bin:>8.3f}')
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
print('\nDone.')
