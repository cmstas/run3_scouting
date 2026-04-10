import uproot
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import sys

def compare_histos(file1, file2, histoname1, histoname2, label1, label2, xlabel, output="comparison.png", extra="False"):

    hep.style.use("CMS")

    # Abrir y leer histogramas
    with uproot.open(file1) as f1, uproot.open(file2) as f2:
        h1 = f1[histoname1]
        h2 = f2[histoname2]

        counts1, edges1 = h1.to_numpy()
        counts2, edges2 = h2.to_numpy()

        # Errores directamente del TH1
        variances1 = h1.variances()
        variances2 = h2.variances()
        errors1 = np.sqrt(variances1) if variances1 is not None else np.sqrt(counts1)
        errors2 = np.sqrt(variances2) if variances2 is not None else np.sqrt(counts2)

    # Plot
    fig, ax = plt.subplots(figsize=(8.5,7))

    hep.histplot(
        (counts1, edges1),
        histtype="errorbar",
        yerr=errors1,
        label=r"%s"%label1,
        color="C0",
        markersize=12,
        elinewidth=2,
        ax=ax,
    )

    hep.histplot(
        (counts2, edges2),
        histtype="errorbar",
        yerr=errors2,
        label=r"%s"%label2,
        color="C3",
        markersize=12,
        elinewidth=2,
        ax=ax,
    )

    ax.set_xlabel(r"%s"%xlabel)
    ax.set_xlabel(r"B-hadron $p_T$ [GeV]")
    ax.set_ylabel("Entries")
    ax.set_yscale("log")
    ax.set_xlim([0, 40.])
    ax.set_ylim([0.1, 1e4])
    ax.legend(fontsize=22)
    #ax.grid(False, which="both", linestyle="--", linewidth=0.5)

    extra = r'$B\rightarrow\phi\rightarrow\mu\mu$'
    ax.text(
    0.05, 0.95, extra,
    transform=ax.transAxes,
    ha="left", va="top",
    fontsize=18
    )

    hep.cms.label(ax=ax, data=True, com=13.6, lumi=None, label="Preliminary")

    plt.tight_layout()
    plt.savefig(output, dpi=150)
    print(f"Comparación guardada en {output}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Use: python compare.py file1.root file2.root histoname [output.png]")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        histoname1 = sys.argv[3]
        histoname2 = sys.argv[4]
        label1 = sys.argv[5]
        label2 = sys.argv[6]        
        xlabel = sys.argv[7]        
        output = sys.argv[8] if len(sys.argv) > 8 else "comparison.png"
        extra = sys.argv[9] if len(sys.argv) > 9 else ""
        compare_histos(file1, file2, histoname1, histoname2, label1, label2, xlabel, output, extra)
