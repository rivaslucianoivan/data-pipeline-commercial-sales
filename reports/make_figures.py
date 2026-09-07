"""Generate the figures embedded in README.md.

Run from the project root:  python reports/make_figures.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.extract import (
    cargar_config_rutas,
    leer_productos,
    leer_ventas_ecommerce,
    leer_ventas_local,
)
from src.transform import preparar_datos_ventas

FIG_DIR = Path("reports/figures")
NAVY, TEAL, GREY, RED = "#1f3b57", "#2a9d8f", "#9bb0c1", "#c0392b"

plt.rcParams.update({
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.axisbelow": True,
})


def load_clean() -> pd.DataFrame:
    paths = cargar_config_rutas()
    _, clean = preparar_datos_ventas(
        leer_ventas_ecommerce(paths["ventas_ecommerce"]),
        leer_ventas_local(paths["ventas_local"]),
        leer_productos(paths["productos"]),
    )
    return clean


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = load_clean()
    total = df["ingreso_bruto"].sum()

    # 1) Channel comparison: same units, different value
    ch = df.groupby("canal").agg(
        ingreso=("ingreso_bruto", "sum"),
        margen=("margen_bruto", "sum"),
        unidades=("cantidad", "sum"),
        docs=("id_documento", "nunique"),
    ).reset_index()
    ch["margen_pct"] = ch["margen"] / ch["ingreso"] * 100
    ch["ticket"] = ch["ingreso"] / ch["docs"]
    ch["canal"] = ch["canal"].str.replace("ecommerce", "E-commerce").str.replace("local", "Physical POS")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, col, title, fmt in [
        (axes[0], "unidades", "Units sold", "{:,.0f}"),
        (axes[1], "ingreso", "Revenue", "${:,.0f}"),
        (axes[2], "margen_pct", "Gross margin %", "{:.1f}%"),
    ]:
        bars = ax.bar(ch["canal"], ch[col], color=[TEAL, NAVY], width=0.55)
        for bar, v in zip(bars, ch[col]):
            ax.text(bar.get_x() + bar.get_width() / 2, v, fmt.format(v),
                    ha="center", va="bottom", fontweight="bold", fontsize=9)
        ax.set_title(title, fontweight="bold", loc="left")
        ax.set_ylim(0, ch[col].max() * 1.20)
        ax.tick_params(axis="x", labelsize=9)
    fig.suptitle(
        "Identical unit volume, very different value: the physical POS sells a richer mix",
        fontweight="bold", x=0.01, ha="left", fontsize=12,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(FIG_DIR / "channel_comparison.png", dpi=150)
    plt.close(fig)

    # 2) Category: revenue share vs margin rate
    cat = df.groupby("categoria").agg(
        ingreso=("ingreso_bruto", "sum"),
        margen=("margen_bruto", "sum"),
    ).reset_index()
    cat["share"] = cat["ingreso"] / total * 100
    cat["margen_pct"] = cat["margen"] / cat["ingreso"] * 100
    cat = cat.sort_values("share", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = range(len(cat))
    ax.bar([i - 0.2 for i in x], cat["share"], width=0.4, color=NAVY, label="% of revenue")
    ax.bar([i + 0.2 for i in x], cat["margen_pct"], width=0.4, color=TEAL, label="Gross margin %")
    for i, (s, m) in enumerate(zip(cat["share"], cat["margen_pct"])):
        ax.text(i - 0.2, s + 0.8, f"{s:.1f}%", ha="center", fontsize=9, fontweight="bold")
        ax.text(i + 0.2, m + 0.8, f"{m:.1f}%", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(cat["categoria"])
    ax.set_ylim(0, 72)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(
        "Footwear leads revenue but lags on margin\n"
        "Accessories convert a smaller share of sales into a larger share of profit",
        loc="left", fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(FIG_DIR / "category_revenue_vs_margin.png", dpi=150)
    plt.close(fig)

    # 3) Daily revenue by channel
    daily = df.groupby([df["fecha"].dt.date, "canal"])["ingreso_bruto"].sum().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.plot(daily.index, daily["local"] / 1000, color=NAVY, lw=1.8, label="Physical POS")
    ax.plot(daily.index, daily["ecommerce"] / 1000, color=TEAL, lw=1.8, label="E-commerce")
    ax.set_ylabel("Daily revenue (thousands)")
    ax.legend(frameon=False)
    ax.set_title(
        "Daily revenue by channel (1 Oct - 11 Nov 2025)",
        loc="left", fontweight="bold",
    )
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "daily_revenue_by_channel.png", dpi=150)
    plt.close(fig)

    print(f"Figures written to {FIG_DIR.resolve()}")


if __name__ == "__main__":
    main()
