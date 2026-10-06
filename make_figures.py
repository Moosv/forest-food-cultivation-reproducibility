"""Generate publication-count figures from validated, recounted workbook records."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from analysis import run_checks, new_output_dir, write_json

TECHNOLOGIES = ["Sensing and measurement", "Automatic and remote control",
                "Communication and platforms", "Modeling and artificial intelligence",
                "Task automation and robotics", "Artificial lighting",
                "Nutrient solution and root zone", "Energy, climate control, and covering"]


def render_figures(tables, out):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.facecolor": "white"})

    def save(fig, stem):
        fig.savefig(out / f"{stem}.jpg", dpi=600, bbox_inches="tight",
                    pil_kwargs={"quality": 98, "subsampling": 0})
        plt.close(fig)

    annual = tables["annual_counts.csv"]
    years, counts = [r["year"] for r in annual], [r["n"] for r in annual]
    fig, ax = plt.subplots(figsize=(7.4, 4.1))
    ax.bar(years, counts, color="#506F88", width=.76)
    ax.set(xlim=(1999.3, 2025.7), ylim=(0, max(181, max(counts) * 1.12)),
           xlabel="Publication year", ylabel="Number of publications")
    ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
    ax.set_yticks([0, 40, 80, 120, 160])
    ax.grid(axis="y", color="#DDDDDD", linewidth=.6)
    ax.set_axisbelow(True)
    ax.annotate(str(counts[-1]), (years[-1], counts[-1]), xytext=(0, 5),
                textcoords="offset points", ha="center")
    fig.tight_layout()
    save(fig, "Figure1_annual_publications_1590")

    rows = tables["period_technology.csv"]
    periods = list(dict.fromkeys(r["period"] for r in rows))
    indexed = {(r["period"], r["code"]): r for r in rows}
    values = [[indexed[p, f"T{i}"]["percent"] for p in periods] for i in range(1, 9)]
    denoms = [indexed[p, "T1"]["denominator"] for p in periods]
    fig, ax = plt.subplots(figsize=(9.8, 5.3))
    im = ax.imshow(values, cmap="Blues", vmin=0, vmax=max(45, max(map(max, values))), aspect="auto")
    ax.set_yticks(range(8), TECHNOLOGIES)
    ax.set_xticks(range(len(periods)), [f"{p}\nn = {n:,}" for p, n in zip(periods, denoms)], fontsize=9)
    ax.tick_params(length=0, pad=8)
    for i, row in enumerate(values):
        for j, value in enumerate(row):
            ax.text(j, i, f"{value:.1f}", ha="center", va="center",
                    color="white" if value > 30 else "#172A39", fontsize=10)
    bar = fig.colorbar(im, ax=ax, fraction=.04, pad=.025)
    bar.set_label("Publications within each period (%)")
    fig.tight_layout()
    save(fig, "Figure2_period_technology_1590")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        tables, report = run_checks(args.input)
        new_output_dir(args.output_dir)
        render_figures(tables, args.output_dir)
        write_json(args.output_dir / "validation_report.json", report)
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"Figure generation failed: {exc}\n")
    print(f"Saved two figures to {args.output_dir}")


if __name__ == "__main__":
    main()
