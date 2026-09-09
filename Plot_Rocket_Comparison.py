import os
import matplotlib.pyplot as plt
import pandas as pd

CSV_FILE = "rocket_comparison.csv"


def plot_rocket_comparison(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"Error: Could not find '{csv_path}'. Run KSPData_Logger_2.py for at least one flight first.")
        return

    df = pd.read_csv(csv_path)

    if df.empty:
        print(f"'{csv_path}' has no rows yet -- log at least one flight that reaches LKO.")
        return

    # Sort configs by delta-v remaining at LKO -- the main efficiency ranking
    df = df.sort_values("dv_remaining_at_lko_ms", ascending=False).reset_index(drop=True)
    configs = df["config_name"]

    plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Rocket Configuration Efficiency Comparison: Path to LKO", fontsize=16, fontweight="bold")

    # -------------------------------------------------------------
    # PLOT 1: dV remaining at LKO -- the headline efficiency ranking
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    bars1 = ax1.bar(configs, df["dv_remaining_at_lko_ms"], color="tab:green")
    ax1.set_title("Delta-V Remaining at LKO\n(more = better head start for Duna)", fontweight="bold")
    ax1.set_ylabel("Delta-V Remaining (m/s)")
    ax1.tick_params(axis="x", rotation=30)
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f"{height:.0f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)

    # -------------------------------------------------------------
    # PLOT 2: Stacked bar -- dV spent to reach LKO vs dV remaining
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    ax2.bar(configs, df["dv_spent_to_lko_ms"], label="Spent Reaching LKO", color="tab:red")
    ax2.bar(configs, df["dv_remaining_at_lko_ms"], bottom=df["dv_spent_to_lko_ms"],
             label="Remaining for Duna", color="tab:green")
    ax2.set_title("Delta-V Budget Breakdown per Configuration", fontweight="bold")
    ax2.set_ylabel("Delta-V (m/s)")
    ax2.tick_params(axis="x", rotation=30)
    ax2.legend(loc="upper right")

    # -------------------------------------------------------------
    # PLOT 3: Peak TWR vs dV remaining -- design tradeoff scatter
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    ax3.scatter(df["peak_twr"], df["dv_remaining_at_lko_ms"], s=90, color="tab:blue", zorder=3)
    for _, row in df.iterrows():
        ax3.annotate(row["config_name"], (row["peak_twr"], row["dv_remaining_at_lko_ms"]),
                     textcoords="offset points", xytext=(6, 4), fontsize=8)
    ax3.set_title("Peak Thrust-to-Weight Ratio vs. Delta-V Remaining", fontweight="bold")
    ax3.set_xlabel("Peak TWR")
    ax3.set_ylabel("Delta-V Remaining at LKO (m/s)")
    ax3.grid(True)

    # -------------------------------------------------------------
    # PLOT 4: Max Q comparison -- aerodynamic loss indicator
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    bars4 = ax4.bar(configs, df["peak_dynamic_pressure_pa"] / 1000.0, color="tab:purple")
    ax4.set_title("Max Dynamic Pressure (Q) per Configuration\n(higher = more drag loss)", fontweight="bold")
    ax4.set_ylabel("Max Q (kPa)")
    ax4.tick_params(axis="x", rotation=30)
    for bar in bars4:
        height = bar.get_height()
        ax4.annotate(f"{height:.1f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig("rocket_comparison.png", dpi=300)
    print("Comparison dashboard saved as 'rocket_comparison.png'. Displaying plot window...")
    plt.show()


if __name__ == "__main__":
    plot_rocket_comparison(CSV_FILE)