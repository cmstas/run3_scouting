import glob
import re
import uproot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, roc_curve

# ---------------------------------------------------------------------------
# Paths — flat tuples produced by fillTuplesScouting.py
# ---------------------------------------------------------------------------
tuples_dir = Path("/home/users/garciaja/fullRun3/CMSSW_15_0_2/src/run3_scouting/tuples")

use_conditional = False
model = 'A'

# ---------------------------------------------------------------------------
# Discover all signal files and parse (mpi, mA, ctau) from filenames
# ---------------------------------------------------------------------------
_SIG_RE = re.compile(
    r"tuples_Signal_ScenarioA_Par_2024_mpi-(\w+)_mA-(\w+)_ctau-(\w+)mm_2024\.root"
)

def _p2f(s):
    return float(s.replace("p", "."))

def _flabel(f):
    s = f"{f:g}"
    return s.replace(".", "p")

MASS_COLORS = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#e377c2"]
BKG_FACE    = "#7fc7c4"
BKG_EDGE    = "#2f5f5d"

sig_file_params = []
for fpath in sorted(glob.glob(str(tuples_dir / "tuples_Signal_ScenarioA_Par_2024_*.root"))):
    m = _SIG_RE.search(os.path.basename(fpath))
    if m:
        mpi_s, mA_s, ctau_s = m.groups()
        sig_file_params.append((fpath, _p2f(mpi_s), _p2f(mA_s), _p2f(ctau_s)))

ctau_values = sorted(set(p[3] for p in sig_file_params))
param_grid  = [(p[3], p[2], p[1]) for p in sig_file_params]  # (ctau, mA, mpi)
print(f"Found {len(sig_file_params)} signal files, ctau values: {ctau_values}")

# ---------------------------------------------------------------------------
# BDT input variables — comment out variables to exclude from training
# Mirrors the selection in plotsignalvsbkg.py
# ---------------------------------------------------------------------------
def _make_bdt_vars():
    sv_stems = [
        # "chi2",
        "chi2Ndof",
        "d3d_mumu_SV",
        "dphi_mumu_SV",
        "l3d",
        "lxy",
        # "maxd3d",
        # "maxdx",
        # "maxdxy",
        # "maxdy",
        # "maxdz",
        # "minDistanceFromDet",
        # "minDistanceFromDet_x",
        # "minDistanceFromDet_y",
        # "minDistanceFromDet_z",
        # "mind3d",
        # "mindx",
        # "mindxy",
        # "mindy",
        # "mindz",
        # "ndof",
        # "onModule",
        # "onModuleWithinUnc",
        "prob",
        "ptmm",
        "x",
        "xErr",
        "y",
        "yErr",
        "z",
        "zErr",
        "dr_mumu",
        "dphi_mumu",
        "deta_mumu",
        "deta_mumu_SV",
        "sindphi_lxy",
        # "closestDet_x",
        # "closestDet_y",
        # "closestDet_z",
        "a3d_mumu"
    ]
    mu_stems = [
        "dxy",
        # "dxyErr",
        "dxysig",
        "dxy_lxy",
        "dz",
        # "dze",
        "dzsig",
        "ecalIso",
        "ecalRelIso",
        "eta",
        "hcalIso",
        "hcalRelIso",
        "isGlobal",
        # "isStandAlone",
        "isTracker",
        "isvtx",
        "maxdr",
        # "mindetaJet",
        # "mindphiJet",
        "mindr",
        # "mindrJet",
        # "mindrPF0p3",
        # "mindrPF0p4",
        "muCSCDT",
        "muChambs",
        # "muExpMatchedStats",
        "muHits",
        # "muMatch",
        # "muMatchedRPC",
        # "muMatchedStats",
        # "ncompatible",
        # "ncompatibletotal",
        # "nexpectedhits",
        # "nexpectedhitsmultiple",
        # "nexpectedhitsmultipletotal",
        # "nexpectedhitstotal",
        "nhitsbeforesv",
        "normChi2",
        # "phi",
        "phiCorr",
        "pixHits",
        "pixLayers",
        "pt",
        # "saHits",
        # "saMatchedStats",
        "stripHits",
        "trackIso",
        "trackRelIso",
        "trkLayers",
        # "PFIsoChg0p3",
        "PFIsoAll0p3",
        # "PFIsoChg0p4",
        # "PFIsoAll0p4",
        # "PFRelIsoChg0p3",
        "PFRelIsoAll0p3",
        # "PFRelIsoChg0p4",
        # "PFRelIsoAll0p4",
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
_LOAD_BRANCHES = list(dict.fromkeys(
    BDT_VARIABLES + ["SV1_lxy", "SV1_mass", "SV2_mass"]
))

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


# ---------------------------------------------------------------------------
# Load signal — all mass/mpi/ctau points
# ---------------------------------------------------------------------------
print('Making signal dataframes...')
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
print('Making background dataframes...')
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


def add_dxy_lxy(df):
    for sv in ("SV1", "SV2"):
        denom = df[f"{sv}_lxy"] * df[f"{sv}_mass"] / df[f"{sv}_ptmm"]
        denom = np.where(denom > 1e-9, denom, 1e-9)
        for mu in ("mu1", "mu2"):
            df[f"{sv}_{mu}_dxy_lxy"] = np.abs(df[f"{sv}_{mu}_dxy"]) / denom


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
    print(f'\nWARNING: {len(missing)} BDT variables not in tuples (regenerate with fillTuplesScouting.py?):')
    for v in missing:
        print(f'  {v}')
print(f'\nBDT input variables ({len(input_vars)}):')
for v in input_vars:
    print(f'  {v}')

cond_vars = ['param_ctau', 'param_mA', 'param_mpi'] if use_conditional else []

cond_tag = 'conditional' if use_conditional else 'non_cond'
out_dir = f'BDT/curves_OR_{model}_{cond_tag}'
os.makedirs(f'{out_dir}/binned_lxy', exist_ok=True)
os.makedirs(f'{out_dir}/global',     exist_ok=True)

# ---------------------------------------------------------------------------
# Training loop — one BDT per lxy bin
# ---------------------------------------------------------------------------
print('Training...')
for bin_label in lxy_labels:
    sig_bin = df_sig[df_sig['lxy_bin'] == bin_label].copy()
    bkg_bin = df_bkg[df_bkg['lxy_bin'] == bin_label].copy()

    if len(bkg_bin) < 100 or len(sig_bin) < 10:
        continue

    if use_conditional:
        # Replicate background once per param point so conditional vars are set
        all_combined = []
        for ctau_val, mA_val, mpi_val in param_grid:
            sig_pt = sig_bin[
                (sig_bin['param_ctau'] == ctau_val) &
                (sig_bin['param_mA']   == mA_val)   &
                (sig_bin['param_mpi']  == mpi_val)
            ].copy()
            bkg_cp = bkg_bin.copy()
            bkg_cp['param_ctau'] = float(ctau_val)
            bkg_cp['param_mA']   = float(mA_val)
            bkg_cp['param_mpi']  = float(mpi_val)
            all_combined.append(pd.concat([sig_pt, bkg_cp], ignore_index=True))
        df_combined = pd.concat(all_combined, ignore_index=True)
    else:
        # Non-conditional: all signal + background combined once
        print(f'  Combining datasets for lxy={bin_label}...')
        df_combined = pd.concat([sig_bin, bkg_bin], ignore_index=True)

    X = df_combined[input_vars + cond_vars]
    y = df_combined['label']
    w = compute_class_weights(y.values)

    print(f'  Training lxy={bin_label} ({len(sig_bin)} sig, {len(bkg_bin)} bkg)...')
    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        X, y, w, test_size=0.3, random_state=42, stratify=y)

    bdt = XGBClassifier(
        n_estimators=100, max_depth=3, learning_rate=0.1,
        use_label_encoder=False, eval_metric='logloss',
        tree_method='hist', n_jobs=4,
    )
    bdt.fit(X_train, y_train, sample_weight=w_train)

    # Feature importance
    print('  Feature importance...')
    importances = bdt.feature_importances_
    mask        = importances >= 0.001
    imp_filt    = importances[mask]
    col_filt    = np.array(X.columns)[mask]
    sorted_idx  = np.argsort(imp_filt)
    fig, ax = plt.subplots(figsize=(8, max(4, len(col_filt) * 0.3)), constrained_layout=True)
    ax.barh(col_filt[sorted_idx], imp_filt[sorted_idx])
    ax.set_title(f'Feature Importance (Lxy={bin_label})')
    ax.tick_params(axis='y', labelsize=8)
    fig.savefig(f'{out_dir}/binned_lxy/FeatImp_lxy_{bin_label}.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # ROC curves — one per (mpi, mA), lines = ctau values
    df_test_meta = df_combined.loc[X_test.index]
    bkg_mask_roc = df_test_meta['label'] == 0

    mpi_mA_groups = {}
    for ctau_val, mA_val, mpi_val in param_grid:
        mpi_mA_groups.setdefault((mpi_val, mA_val), []).append(ctau_val)

    for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
        plot_dir = f'{out_dir}/binned_lxy/mpi{_flabel(mpi_val)}/mA_{_flabel(mA_val)}'
        os.makedirs(plot_dir, exist_ok=True)
        fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, linewidth=1.0)

        for i, ctau_val in enumerate(sorted(ctau_vals)):
            sig_mask = (
                (df_test_meta['param_ctau'] == float(ctau_val)) &
                (df_test_meta['param_mA']   == float(mA_val))   &
                (df_test_meta['param_mpi']  == float(mpi_val))
            )
            eval_mask = sig_mask | bkg_mask_roc if not use_conditional else sig_mask
            X_eval = X_test[eval_mask]
            y_eval = y_test[eval_mask]
            if len(y_eval) < 10 or y_eval.nunique() < 2:
                continue
            y_pred = bdt.predict_proba(X_eval)[:, 1]
            fpr, tpr, _ = roc_curve(y_eval, y_pred)
            auc = roc_auc_score(y_eval, y_pred)
            ax.plot(fpr, tpr, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6,
                    label=rf'$c\tau={ctau_val:g}$ mm (AUC={auc:.3f})')

        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(f'ROC mpi={mpi_val} mA={mA_val} lxy={bin_label}')
        ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
        fig.savefig(
            f'{plot_dir}/ROC_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}_lxy_{bin_label}.png',
            dpi=150, bbox_inches='tight',
        )
        plt.close(fig)

    # Grouped discriminant plots — one per (mpi, mA), lines = ctau values
    bkg_disc_scores = bdt.predict_proba(X_test[bkg_mask_roc])[:, 1]

    disc_bins = np.linspace(0, 1, 51)
    widths = np.diff(disc_bins)
    for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups.items()):
        plot_dir = f'{out_dir}/binned_lxy/mpi{_flabel(mpi_val)}/mA_{_flabel(mA_val)}'
        os.makedirs(plot_dir, exist_ok=True)
        fig, ax = plt.subplots(figsize=(7.2, 5.6), constrained_layout=True)

        hb, _ = np.histogram(bkg_disc_scores, bins=disc_bins)
        if hb.sum() > 0: hb = hb / hb.sum()
        ax.bar(disc_bins[:-1], hb, width=widths, align='edge',
               color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6,
               label='Background', zorder=1)

        for i, ctau_val in enumerate(sorted(ctau_vals)):
            sig_mask = (
                (df_test_meta['param_ctau'] == float(ctau_val)) &
                (df_test_meta['param_mA']   == float(mA_val))   &
                (df_test_meta['param_mpi']  == float(mpi_val))
            )
            if sig_mask.sum() < 5:
                continue
            hs, _ = np.histogram(bdt.predict_proba(X_test[sig_mask])[:, 1], bins=disc_bins)
            if hs.sum() > 0: hs = hs / hs.sum()
            ax.stairs(hs, disc_bins, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6,
                      label=rf'$c\tau={ctau_val:g}$ mm', zorder=3 + i)

        ax.set_xlabel('BDT score')
        ax.set_ylabel('a.u.')
        ax.set_title(rf'Discriminant $m_\pi={mpi_val:g}$ GeV, $m_A={mA_val:g}$ GeV, lxy={bin_label}')
        ax.legend(loc='upper center', fontsize=9, framealpha=0.9)
        fig.savefig(
            f'{plot_dir}/Disc_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}_lxy_{bin_label}.png',
            dpi=150, bbox_inches='tight',
        )
        plt.close(fig)

# ---------------------------------------------------------------------------
# Global BDT — trained on all lxy bins combined
# ---------------------------------------------------------------------------
print('Training global BDT...')
if use_conditional:
    all_combined_global = []
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
        all_combined_global.append(pd.concat([sig_pt, bkg_cp], ignore_index=True))
    df_global = pd.concat(all_combined_global, ignore_index=True)
else:
    df_global = pd.concat([df_sig, df_bkg], ignore_index=True)

X_g = df_global[input_vars + cond_vars]
y_g = df_global['label']
w_g = compute_class_weights(y_g.values)

X_train_g, X_test_g, y_train_g, y_test_g, w_train_g, w_test_g = train_test_split(
    X_g, y_g, w_g, test_size=0.3, random_state=42, stratify=y_g)

bdt_global = XGBClassifier(
    n_estimators=100, max_depth=3, learning_rate=0.1,
    use_label_encoder=False, eval_metric='logloss',
    tree_method='hist', n_jobs=4,
)
bdt_global.fit(X_train_g, y_train_g, sample_weight=w_train_g)

# Feature importance
importances_g = bdt_global.feature_importances_
mask_g        = importances_g >= 0.001
imp_filt_g    = importances_g[mask_g]
col_filt_g    = np.array(X_g.columns)[mask_g]
sorted_idx_g  = np.argsort(imp_filt_g)
fig, ax = plt.subplots(figsize=(8, max(4, len(col_filt_g) * 0.3)), constrained_layout=True)
ax.barh(col_filt_g[sorted_idx_g], imp_filt_g[sorted_idx_g])
ax.set_title('Feature Importance (Global, all lxy)')
ax.tick_params(axis='y', labelsize=8)
fig.savefig(f'{out_dir}/global/FeatImp_global.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ROC curves — global BDT, one per (mpi, mA), lines = ctau values
df_test_meta_g = df_global.loc[X_test_g.index]
bkg_mask_roc_g = df_test_meta_g['label'] == 0

mpi_mA_groups_g = {}
for ctau_val, mA_val, mpi_val in param_grid:
    mpi_mA_groups_g.setdefault((mpi_val, mA_val), []).append(ctau_val)

for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups_g.items()):
    plot_dir_g = f'{out_dir}/global/mpi{_flabel(mpi_val)}/mA_{_flabel(mA_val)}'
    os.makedirs(plot_dir_g, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.4, linewidth=1.0)

    for i, ctau_val in enumerate(sorted(ctau_vals)):
        sig_mask = (
            (df_test_meta_g['param_ctau'] == float(ctau_val)) &
            (df_test_meta_g['param_mA']   == float(mA_val))   &
            (df_test_meta_g['param_mpi']  == float(mpi_val))
        )
        eval_mask = sig_mask | bkg_mask_roc_g if not use_conditional else sig_mask
        X_eval_g = X_test_g[eval_mask]
        y_eval_g = y_test_g[eval_mask]
        if len(y_eval_g) < 10 or y_eval_g.nunique() < 2:
            continue
        y_pred_g = bdt_global.predict_proba(X_eval_g)[:, 1]
        fpr_g, tpr_g, _ = roc_curve(y_eval_g, y_pred_g)
        auc_g = roc_auc_score(y_eval_g, y_pred_g)
        ax.plot(fpr_g, tpr_g, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6,
                label=rf'$c\tau={ctau_val:g}$ mm (AUC={auc_g:.3f})')

    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title(f'ROC Global mpi={mpi_val} mA={mA_val}')
    ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
    fig.savefig(
        f'{plot_dir_g}/ROC_global_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}.png',
        dpi=150, bbox_inches='tight',
    )
    plt.close(fig)

# Grouped discriminant plots — global BDT, one per (mpi, mA), lines = ctau values
bkg_disc_scores_g = bdt_global.predict_proba(X_test_g[bkg_mask_roc_g])[:, 1]

disc_bins = np.linspace(0, 1, 51)
widths = np.diff(disc_bins)
for (mpi_val, mA_val), ctau_vals in sorted(mpi_mA_groups_g.items()):
    plot_dir_g = f'{out_dir}/global/mpi{_flabel(mpi_val)}/mA_{_flabel(mA_val)}'
    os.makedirs(plot_dir_g, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 5.6), constrained_layout=True)

    hb_g, _ = np.histogram(bkg_disc_scores_g, bins=disc_bins)
    if hb_g.sum() > 0: hb_g = hb_g / hb_g.sum()
    ax.bar(disc_bins[:-1], hb_g, width=widths, align='edge',
           color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6,
           label='Background', zorder=1)

    for i, ctau_val in enumerate(sorted(ctau_vals)):
        sig_mask = (
            (df_test_meta_g['param_ctau'] == float(ctau_val)) &
            (df_test_meta_g['param_mA']   == float(mA_val))   &
            (df_test_meta_g['param_mpi']  == float(mpi_val))
        )
        if sig_mask.sum() < 5:
            continue
        hs_g, _ = np.histogram(bdt_global.predict_proba(X_test_g[sig_mask])[:, 1], bins=disc_bins)
        if hs_g.sum() > 0: hs_g = hs_g / hs_g.sum()
        ax.stairs(hs_g, disc_bins, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6,
                  label=rf'$c\tau={ctau_val:g}$ mm', zorder=3 + i)

    ax.set_xlabel('BDT score')
    ax.set_ylabel('a.u.')
    ax.set_title(rf'Discriminant Global $m_\pi={mpi_val:g}$ GeV, $m_A={mA_val:g}$ GeV')
    ax.legend(loc='upper center', fontsize=9, framealpha=0.9)
    fig.savefig(
        f'{plot_dir_g}/Disc_global_mpi{_flabel(mpi_val)}_mA{_flabel(mA_val)}.png',
        dpi=150, bbox_inches='tight',
    )
    plt.close(fig)
