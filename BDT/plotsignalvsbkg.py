#!/usr/bin/env python3
"""Signal vs background shape comparison for all BDT input variables.

One set of plots per ctau value (all mpi/mA combined for that ctau).
Ranges are auto-computed from combined sig+bkg data (1st-99th percentile).
Output: BDT/signal_vs_bkg_ctau{label}/{var}.png
"""
import os
import re
import glob
import numpy as np
import uproot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

_HERE      = Path(__file__).resolve().parent
TUPLES_DIR = str(_HERE.parent / "tuples")
TREE_NAME  = "tuples"

N_BINS = 50

# ---------------------------------------------------------------------------
# Discover signal files grouped by ctau
# ---------------------------------------------------------------------------
_SIG_RE = re.compile(
    r"tuples_Signal_ScenarioA_Par_2024_mpi-\w+_mA-\w+_ctau-(\w+)mm_2024\.root"
)

def _p2f(s):
    return float(s.replace("p", "."))

def _ctau_label(c):
    s = f"{c:g}"
    return s.replace(".", "p")

ctau_to_files = {}
for fpath in sorted(glob.glob(os.path.join(TUPLES_DIR, "tuples_Signal_ScenarioA_Par_2024_*.root"))):
    m = _SIG_RE.search(os.path.basename(fpath))
    if m:
        ctau = _p2f(m.group(1))
        ctau_to_files.setdefault(ctau, []).append(fpath)

ctau_values = sorted(ctau_to_files)
print(f"ctau values found: {ctau_values}")

BKG_FILES = sorted(glob.glob(os.path.join(TUPLES_DIR, "tuples_QCD_*.root")))

# ---------------------------------------------------------------------------
# Axis label definitions (matplotlib LaTeX)
# ---------------------------------------------------------------------------

_SV_STEM_LABELS = {
    "ptmm":                    r"$p_{T}^{\mu\mu}$ [GeV]",
    #"chi2":                    r"SV $\chi^{2}$",
    "prob":                    r"SV $\chi^{2}$ probability",
    "x":                       r"SV $x$ [cm]",
    "y":                       r"SV $y$ [cm]",
    "z":                       r"SV $z$ [cm]",
    "lxy":                     r"$l_{xy}$ (from PV) [cm]",
    "xErr":                    r"SV $x$ error [cm]",
    "yErr":                    r"SV $y$ error [cm]",
    "zErr":                    r"SV $z$ error [cm]",
    "dphi_mumu_SV":            r"$|\Delta\phi(\vec{\mu\mu},\,\vec{SV})|$ [rad]",
    "d3d_mumu_SV":             r"3D angle$(\vec{\mu\mu},\,\vec{SV})$ [rad]",
    "a3d_mumu":                r"3D angle$(\mu,\,\mu)$ [rad]",
    "mass":                    r"$m_{\mu\mu}$ [GeV]",
    #"ndof":                    r"SV ndof",
    "chi2Ndof":                r"SV $\chi^{2}$/ndof",
    "l3d":                     r"$l_{3D}$ (from PV) [cm]",
    #"mindx":                   r"min $D_{x}(SV_{i},SV_{j})$ [cm]",
    #"mindy":                   r"min $D_{y}(SV_{i},SV_{j})$ [cm]",
    #"mindz":                   r"min $D_{z}(SV_{i},SV_{j})$ [cm]",
    #"mindxy":                  r"min $D_{xy}(SV_{i},SV_{j})$ [cm]",
    #"mind3d":                  r"min $D_{3D}(SV_{i},SV_{j})$ [cm]",
    #"maxdx":                   r"max $D_{x}(SV_{i},SV_{j})$ [cm]",
    #"maxdy":                   r"max $D_{y}(SV_{i},SV_{j})$ [cm]",
    #"maxdz":                   r"max $D_{z}(SV_{i},SV_{j})$ [cm]",
    #"maxdxy":                  r"max $D_{xy}(SV_{i},SV_{j})$ [cm]",
    #"maxd3d":                  r"max $D_{3D}(SV_{i},SV_{j})$ [cm]",
    #"onModule":                r"SV on module",
    #"onModuleWithinUnc":       r"SV on module (within unc.)",
    #"minDistanceFromDet":      r"Min. distance to module [cm]",
    #"minDistanceFromDet_x":    r"Min. distance to module, $x$ [cm]",
    #"minDistanceFromDet_y":    r"Min. distance to module, $y$ [cm]",
    #"minDistanceFromDet_z":    r"Min. distance to module, $z$ [cm]",
    #"closestDet_x":            r"Closest module $x$ [cm]",
    #"closestDet_y":            r"Closest module $y$ [cm]",
    #"closestDet_z":            r"Closest module $z$ [cm]",
}

_MU_STEM_LABELS = {
    "pt":                        r"Muon $p_{T}$ [GeV]",
    "eta":                       r"Muon $\eta$",
    #"phi":                       r"Muon $\phi$ [rad]",
    "phiCorr":                   r"Muon $\phi$ corrected [rad]",
    "isvtx":                     r"Muon is from vertex",
    "normChi2":                  r"Muon $\chi^{2}$/ndof",
    "dxy":                       r"Muon $|d_{xy}|$ [cm]",
    #"dxyErr":                    r"Muon $d_{xy}$ error [cm]",
    "dxysig":                    r"Muon $|d_{xy}|/\sigma_{xy}$",
    "dz":                        r"Muon $|d_{z}|$ [cm]",
    #"dze":                       r"Muon $d_{z}$ error [cm]",
    "dzsig":                     r"Muon $|d_{z}|/\sigma_{z}$",
    "nhitsbeforesv":             r"Hits before SV",
    "isGlobal":                  r"Muon isGlobal",
    "isTracker":                 r"Muon isTracker",
    #"isStandAlone":              r"Muon isStandAlone",
    "pixHits":                   r"Pixel hits",
    "stripHits":                 r"Strip hits",
    "pixLayers":                 r"Pixel layers",
    "trkLayers":                 r"Tracker layers",
    #"saHits":                    r"SA muon hits",
    #"saMatchedStats":            r"SA matched stations",
    "muHits":                    r"Muon hits",
    "muChambs":                  r"Muon chambers",
    "muCSCDT":                   r"CSC/DT chambers",
    #"muMatch":                   r"Muon matches",
    #"muMatchedStats":            r"Matched stations",
    #"muExpMatchedStats":         r"Expected matched stations",
    #"muMatchedRPC":              r"Matched RPC layers",
    "ecalIso":                   r"ECAL isolation [GeV]",
    "hcalIso":                   r"HCAL isolation [GeV]",
    "trackIso":                  r"Track isolation [GeV]",
    "ecalRelIso":                r"ECAL isolation / $p_{T}$",
    "hcalRelIso":                r"HCAL isolation / $p_{T}$",
    "trackRelIso":               r"Track isolation / $p_{T}$",
    #"PFIsoChg0p3":               r"PF-chg iso. ($\Delta R<0.3$) [GeV]",
    "PFIsoAll0p3":               r"PF-all iso. ($\Delta R<0.3$) [GeV]",
    #"PFRelIsoChg0p3":            r"PF-chg rel. iso. ($\Delta R<0.3$)",
    "PFRelIsoAll0p3":            r"PF-all rel. iso. ($\Delta R<0.3$)",
    #"mindrPF0p3":                r"min $\Delta R(\mu,\mathrm{PF\ cand.})\ [\Delta R<0.3]$",
    #"PFIsoChg0p4":               r"PF-chg iso. ($\Delta R<0.4$) [GeV]",
    #"PFIsoAll0p4":               r"PF-all iso. ($\Delta R<0.4$) [GeV]",
    #"PFRelIsoChg0p4":            r"PF-chg rel. iso. ($\Delta R<0.4$)",
    #"PFRelIsoAll0p4":            r"PF-all rel. iso. ($\Delta R<0.4$)",
    #"mindrPF0p4":                r"min $\Delta R(\mu,\mathrm{PF\ cand.})\ [\Delta R<0.4]$",
    "mindr":                     r"min $\Delta R(\mu_{i},\mu_{j})$",
    "maxdr":                     r"max $\Delta R(\mu_{i},\mu_{j})$",
    #"mindrJet":                  r"min $\Delta R(\mu,\mathrm{PF\ jet})$",
    #"mindphiJet":                r"$\Delta\phi(\mu,\mathrm{nearest\ PF\ jet})$ [rad]",
    #"mindetaJet":                r"$\Delta\eta(\mu,\mathrm{nearest\ PF\ jet})$",
    #"ncompatible":               r"$n_\mathrm{compatible}$",
    #"ncompatibletotal":          r"$n_\mathrm{compatible\ total}$",
    #"nexpectedhits":             r"$n_\mathrm{expected\ hits}$",
    #"nexpectedhitsmultiple":     r"$n_\mathrm{expected\ hits\ (multiple)}$",
    #"nexpectedhitsmultipletotal":r"$n_\mathrm{expected\ hits\ (multiple,\ total)}$",
    #"nexpectedhitstotal":        r"$n_\mathrm{expected\ hits\ total}$",
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

def load_all(files):
    arrays = {}
    for path in files:
        with uproot.open(path) as f:
            t = f[TREE_NAME]
            for branch in t.keys():
                arr = t[branch].array(library="np")
                arrays.setdefault(branch, []).append(arr)
    return {k: np.concatenate(v) for k, v in arrays.items()}


print("Loading background...")
bkg = load_all(BKG_FILES)

for ctau in ctau_values:
    lbl    = _ctau_label(ctau)
    outdir = str(_HERE / f"signal_vs_bkg_ctau{lbl}")
    os.makedirs(outdir, exist_ok=True)

    print(f"Loading signal ctau={ctau}mm ({len(ctau_to_files[ctau])} files)...")
    sig = load_all(ctau_to_files[ctau])

    variables = [v for v in AXIS_LABELS if v in sig and v in bkg]
    print(f"  Plotting {len(variables)} variables...")

    for var in variables:
        s = sig[var].astype(float)
        b = bkg[var].astype(float)

        combined = np.concatenate([s, b])
        combined = combined[np.isfinite(combined)]
        if len(combined) == 0:
            continue

        lo = np.percentile(combined, 1)
        hi = np.percentile(combined, 99)
        if lo == hi:
            lo, hi = combined.min(), combined.max()
        if lo == hi:
            continue

        hs, edges = np.histogram(s, bins=N_BINS, range=(lo, hi))
        hb, _     = np.histogram(b, bins=N_BINS, range=(lo, hi))

        hs = hs / hs.sum() if hs.sum() > 0 else hs
        hb = hb / hb.sum() if hb.sum() > 0 else hb

        xlabel = AXIS_LABELS.get(var, var)

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.step(edges[:-1], hb, where='post', color='red',  linewidth=1.5, label="QCD")
        ax.step(edges[:-1], hs, where='post', color='blue', linewidth=1.5,
                label=rf"Signal ($c\tau$={ctau}mm, all masses)")
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel("a.u.", fontsize=11)
        ax.set_title(var, fontsize=10)
        ax.legend(fontsize=9)
        fig.tight_layout()
        fig.savefig(os.path.join(outdir, f"{var}.png"), dpi=100)
        plt.close(fig)

    print(f"  Done. Saved to {outdir}/")

print("All done.")
