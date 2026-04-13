from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_plot(df: pd.DataFrame, output_path: Path) -> None:
    """Save a simple chart showing total day length and daily increase."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    axes[0].plot(df["date"], df["day_length"].dt.total_seconds() / 3600, linewidth=2)
    axes[0].set_title("Day Length Over Time")
    axes[0].set_ylabel("Hours")
    axes[0].grid(alpha=0.3)

    axes[1].bar(df["date"], df["daily_increase"].dt.total_seconds() / 60, width=1.5)
    axes[1].set_title("Daily Increase")
    axes[1].set_ylabel("Minutes")
    axes[1].grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
