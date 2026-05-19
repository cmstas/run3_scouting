#!/usr/bin/env python3
"""Cut-and-count: signal efficiency vs background rejection in lxy bins.

Ported from the old Vtx-collection ntuples to the new flat tuples format.
Key changes vs old version:
  - Tree is 'tuples' (was 'tout')
  - Branches are flat scalars, no jagged max_or_default needed
  - Muon vars live on the SV object: SV1_mu1_pt, SV1_mu1_dxysig, etc.
  - dphi: SV1_dphi_mumu_SV  (was SV1_dphi_Vtx)
  - chi2/ndof: SV1_chi2Ndof already computed (was SV1_chi2/SV1_ndof)
  - dxysig: SV1_mu1_dxysig already computed
  - SV1_3Dangle has no equivalent in new ntuples — cut dropped
"""
import glob
import numpy as np
import uproot
from pathlib import Path

TUPLES_DIR = Path(__file__).resolve().parent.parent / "tuples"
TREE_NAME  = "tuples"

# One benchmark signal — edit as needed
SIG_PATTERN = str(TUPLES_DIR / "tuples_Signal_ScenarioA_Par_2024_mpi-2_mA-0p50_ctau-1p0mm_2024.root")
BKG_PATTERN = str(TUPLES_DIR / "tuples_QCD_*.root")

SIG_FILES = sorted(glob.glob(SIG_PATTERN))
BKG_FILES = sorted(glob.glob(BKG_PATTERN))

BRANCHES = [
    "SV1_lxy",   "SV1_chi2Ndof",  "SV1_prob",  "SV1_mass",  "SV1_ptmm",
    "SV1_xErr",  "SV1_yErr",      "SV1_zErr",
    "SV1_dphi_mumu_SV",
    "SV1_mu1_dxysig", "SV1_mu1_dxy", "SV1_mu1_normChi2", "SV1_mu1_phi", "SV1_mu1_eta",
    "SV1_mu1_nhitsbeforesv",
    "SV1_mu2_dxysig", "SV1_mu2_dxy", "SV1_mu2_normChi2", "SV1_mu2_phi", "SV1_mu2_eta",
    "SV1_mu2_nhitsbeforesv",
    "SV1_minDistanceFromDet_x", "SV1_minDistanceFromDet_y", "SV1_minDistanceFromDet_z",

    "SV2_lxy",   "SV2_chi2Ndof",  "SV2_prob",  "SV2_mass",  "SV2_ptmm",
    "SV2_xErr",  "SV2_yErr",      "SV2_zErr",
    "SV2_dphi_mumu_SV",
    "SV2_mu1_dxysig", "SV2_mu1_dxy", "SV2_mu1_normChi2", "SV2_mu1_phi", "SV2_mu1_eta",
    "SV2_mu1_nhitsbeforesv",
    "SV2_mu2_dxysig", "SV2_mu2_dxy", "SV2_mu2_normChi2", "SV2_mu2_phi", "SV2_mu2_eta",
    "SV2_mu2_nhitsbeforesv",
    "SV2_minDistanceFromDet_x", "SV2_minDistanceFromDet_y", "SV2_minDistanceFromDet_z",
]

LXY_BINS   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]
LXY_LABELS = ["0p0-0p2", "0p2-1p0", "1p0-2p4", "2p4-3p1",
               "3p1-7p0", "7p0-11p0", "11p0-16p0", "16p0-70p0"]


def load_arrays(files, label):
    arrays = {b: [] for b in BRANCHES}
    for path in files:
        with uproot.open(path) as f:
            t = f[TREE_NAME]
            for b in BRANCHES:
                arrays[b].append(t[b].array(library="np"))
    arr = {b: np.concatenate(arrays[b]) for b in BRANCHES}
    arr["label"] = np.full(len(arr[BRANCHES[0]]), label, dtype=np.int8)
    return arr


def sv_mask(arr, sv):
    dphi     = arr[f"SV{sv}_dphi_mumu_SV"]
    xErr     = arr[f"SV{sv}_xErr"]
    yErr     = arr[f"SV{sv}_yErr"]
    zErr     = arr[f"SV{sv}_zErr"]
    lxy      = arr[f"SV{sv}_lxy"]
    chi2ndof = arr[f"SV{sv}_chi2Ndof"]
    return (
        (xErr     < 0.05) &
        (yErr     < 0.05) &
        (zErr     < 0.10) &
        (dphi     > 0   ) &
        (lxy      > 0   ) &
        (lxy      < 70  ) &
        (chi2ndof < 3   )
    )


def dimuon_mask(arr, sv):
    dxysig1   = arr[f"SV{sv}_mu1_dxysig"]
    dxysig2   = arr[f"SV{sv}_mu2_dxysig"]
    dxy1      = arr[f"SV{sv}_mu1_dxy"]
    dxy2      = arr[f"SV{sv}_mu2_dxy"]
    chi2ndof1 = arr[f"SV{sv}_mu1_normChi2"]
    chi2ndof2 = arr[f"SV{sv}_mu2_normChi2"]
    phi1      = arr[f"SV{sv}_mu1_phi"]
    phi2      = arr[f"SV{sv}_mu2_phi"]
    eta1      = arr[f"SV{sv}_mu1_eta"]
    eta2      = arr[f"SV{sv}_mu2_eta"]
    lxy       = arr[f"SV{sv}_lxy"]
    mass      = arr[f"SV{sv}_mass"]
    ptmm      = arr[f"SV{sv}_ptmm"]

    dphi = (phi1 - phi2 + np.pi) % (2 * np.pi) - np.pi
    dphi = np.where(np.abs(dphi) > 1e-6, dphi, 1e-6)
    deta = eta1 - eta2
    log_ratio = np.log10(np.abs(deta) / np.abs(dphi))

    denom     = lxy * mass / ptmm
    dxy_lxy1  = np.abs(dxy1) / np.where(denom > 1e-9, denom, 1e-9)
    dxy_lxy2  = np.abs(dxy2) / np.where(denom > 1e-9, denom, 1e-9)

    return (
        (dxysig1   > 2   ) &
        (dxysig2   > 2   ) &
        (chi2ndof1 < 3   ) &
        (chi2ndof2 < 3   ) &
        (dphi      < 2.8 ) &
        (log_ratio < 1.25) &
        (dxy_lxy1  > 0.1 ) &
        (dxy_lxy2  > 0.1 )
    )


def material_veto_mask(arr, sv):
    dx = arr[f"SV{sv}_minDistanceFromDet_x"]
    dy = arr[f"SV{sv}_minDistanceFromDet_y"]
    dz = arr[f"SV{sv}_minDistanceFromDet_z"]
    return (dx >= 0.81) & (dy >= 3.24) & (dz >= 0.0145)


def excess_hits_mask(arr, sv):
    lxy     = arr[f"SV{sv}_lxy"]
    n_excess = arr[f"SV{sv}_mu1_nhitsbeforesv"] + arr[f"SV{sv}_mu2_nhitsbeforesv"]
    max_hits = np.where(lxy < 11, 0, np.where(lxy < 16, 1, 2))
    return n_excess <= max_hits


def apply_cuts(arr):
    pass1 = sv_mask(arr, 1) & dimuon_mask(arr, 1) & excess_hits_mask(arr, 1) & material_veto_mask(arr, 1)
    pass2 = sv_mask(arr, 2) & dimuon_mask(arr, 2) & excess_hits_mask(arr, 2) & material_veto_mask(arr, 2)
    mask  = pass1 | pass2
    return {k: v[mask] for k, v in arr.items()}


print("Loading signal...")
sig = load_arrays(SIG_FILES, label=1)
print("Loading background...")
bkg = load_arrays(BKG_FILES, label=0)

all_events = {k: np.concatenate([sig[k], bkg[k]]) for k in sig}

lxy    = all_events["SV1_lxy"]
labels = all_events["label"]

print()
print(f"{'lxy bin':>14} | {'sig pass/total':>16}  {'sig eff':>8} | {'bkg pass/total':>16}  {'bkg rej':>8}")
print("-" * 75)

for lo, hi, lbl in zip(LXY_BINS[:-1], LXY_BINS[1:], LXY_LABELS):
    bin_mask = (lxy >= lo) & (lxy < hi)
    arr_bin  = {k: v[bin_mask] for k, v in all_events.items()}
    arr_pass = apply_cuts(arr_bin)

    sig_total = int(np.sum(arr_bin["label"]  == 1))
    bkg_total = int(np.sum(arr_bin["label"]  == 0))
    sig_pass  = int(np.sum(arr_pass["label"] == 1))
    bkg_pass  = int(np.sum(arr_pass["label"] == 0))

    sig_eff = sig_pass / sig_total if sig_total > 0 else float("nan")
    bkg_rej = 1 - bkg_pass / bkg_total if bkg_total > 0 else float("nan")

    print(
        f"{lbl:>14} | "
        f"{sig_pass:>6}/{sig_total:<8}  {sig_eff:>8.3f} | "
        f"{bkg_pass:>6}/{bkg_total:<8}  {bkg_rej:>8.3f}"
    )
