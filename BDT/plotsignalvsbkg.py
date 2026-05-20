#!/usr/bin/env python3
"""Signal vs background shape comparison for all BDT input variables.

One set of plots per ctau lifetime. Each plot overlays:
  - the combined QCD background (filled, with sqrt(N) uncertainty band)
  - one step-line per (mpi, mA) mass point available at that ctau

Ranges are auto-computed from combined sig+bkg data (1st-99th percentile).
Output: BDT/signal_vs_bkg_ctau{X}mm/{var}.png
"""
import os
import re
import glob
import numpy as np
import uproot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use("CMS")

# --- Aesthetic overrides on top of the CMS style ---------------------------
# The CMS mplhep style is sized for publication-scale plots; for these many
# small figures we want lighter text and a more compact look.
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

FIGSIZE = (8.5, 6.5)

from pathlib import Path

_HERE      = Path(__file__).resolve().parent
TUPLES_DIR = str(_HERE.parent / "tuples")
TREE_NAME  = "tuples"

N_BINS = 50

# Colors for mass-point overlays (ordered light -> heavy).
MASS_COLORS = ["#d62728", "#ff7f0e", "#2ca02c", "#1f77b4", "#e377c2"]

# Background colours
BKG_FACE = "#7fc7c4"
BKG_EDGE = "#2f5f5d"

# ---------------------------------------------------------------------------
# Discover signal files grouped by (mpi, mA) then ctau
# ---------------------------------------------------------------------------
_SIG_RE = re.compile(
    r"tuples_Signal_ScenarioA_Par_2024_mpi-(\w+?)_mA-(\w+?)_ctau-(\w+?)mm_2024\.root"
)

def _p2f(s):
    return float(s.replace("p", "."))

def _f2lbl(x):
    return f"{x:g}".replace(".", "p")

# mpi_mA_files[(mpi, mA)][ctau] = [files]
mpi_mA_files = {}
for fpath in sorted(glob.glob(os.path.join(TUPLES_DIR, "tuples_Signal_ScenarioA_Par_2024_*.root"))):
    m = _SIG_RE.search(os.path.basename(fpath))
    if not m:
        continue
    mpi  = _p2f(m.group(1))
    mA   = _p2f(m.group(2))
    ctau = _p2f(m.group(3))
    mpi_mA_files.setdefault((mpi, mA), {}).setdefault(ctau, []).append(fpath)

mpi_values = sorted(set(k[0] for k in mpi_mA_files))
print(f"(mpi, mA) points found ({len(mpi_mA_files)}):")
for (mpi, mA), ctau_dict in sorted(mpi_mA_files.items()):
    print(f"  mpi={mpi}, mA={mA}: ctau={sorted(ctau_dict)}")

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

for mpi in mpi_values:
    mA_vals = sorted(set(k[1] for k in mpi_mA_files if k[0] == mpi))
    for mA in mA_vals:
        ctau_dict = mpi_mA_files[(mpi, mA)]
        ctau_vals = sorted(ctau_dict)
        outdir = str(_HERE / f"signal_vs_bkg_mpi{mpi:g}" / f"mA_{mA:g}")
        os.makedirs(outdir, exist_ok=True)

        sig_per_ctau = {}
        for ctau in ctau_vals:
            print(f"  Loading mpi={mpi}, mA={mA}, ctau={ctau} ({len(ctau_dict[ctau])} files)...")
            sig_per_ctau[ctau] = load_all(ctau_dict[ctau])

        common = set(bkg.keys())
        for s in sig_per_ctau.values():
            common &= set(s.keys())
        variables = [v for v in AXIS_LABELS if v in common]
        print(f"  ({len(variables)} vars) -> {outdir}/")

        for var in variables:
            all_vals = [bkg[var].astype(float)]
            for s in sig_per_ctau.values():
                all_vals.append(s[var].astype(float))
            combined = np.concatenate(all_vals)
            combined = combined[np.isfinite(combined)]
            if len(combined) == 0:
                continue

            lo = np.percentile(combined, 1)
            hi = np.percentile(combined, 99)
            if lo == hi:
                lo, hi = combined.min(), combined.max()
            if lo == hi:
                continue

            b  = bkg[var].astype(float)
            hb, edges = np.histogram(b, bins=N_BINS, range=(lo, hi))
            bsum = hb.sum()
            hb_norm = hb / bsum if bsum > 0 else hb.astype(float)

            widths = np.diff(edges)
            xlabel = AXIS_LABELS.get(var, var)

            fig, ax = plt.subplots(figsize=FIGSIZE)

            ax.bar(edges[:-1], hb_norm, width=widths, align='edge',
                   color=BKG_FACE, edgecolor=BKG_EDGE, linewidth=0.6,
                   label="Background", zorder=1)

            for i, ctau in enumerate(ctau_vals):
                s = sig_per_ctau[ctau][var].astype(float)
                hs, _ = np.histogram(s, bins=N_BINS, range=(lo, hi))
                if hs.sum() > 0:
                    hs = hs / hs.sum()
                ax.stairs(hs, edges, color=MASS_COLORS[i % len(MASS_COLORS)], linewidth=1.6,
                          label=rf"$c\tau = {ctau:g}$ mm", zorder=3 + i)

            pos_vals = hb_norm[hb_norm > 0]
            if pos_vals.size > 0:
                ax.set_yscale('log')
                ymin = max(pos_vals.min() * 0.3, 1e-6)
                ax.set_ylim(bottom=ymin)

            ax.set_title(var, fontsize=11)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("a.u.")

            ax.text(0.02, 0.97, "Preliminary",
                    transform=ax.transAxes,
                    fontsize=11, fontstyle="italic", fontweight="bold",
                    va="top", ha="left")
            ax.legend(loc="best", framealpha=0.9,
                      title=rf"$m_\pi = {mpi:g}$ GeV, $m_A = {mA:g}$ GeV",
                      title_fontsize=10)
            ax.tick_params(direction="in", top=True, right=True, which="both")
            fig.tight_layout()
            fig.savefig(os.path.join(outdir, f"{var}.png"), dpi=130)
            plt.close(fig)

        print("    Done.")

print("\nAll done.")