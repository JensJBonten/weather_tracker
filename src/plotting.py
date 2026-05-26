from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_plot(daylight_dataframe: pd.DataFrame, output_path: Path) -> None:
    """Lagrer en enkel graf som viser dagslengde og daglig økning."""
    # Sørger for at målmappen finnes før PNG-filen skrives.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Lager to grafer under hverandre med samme datoakse.
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    # Første graf viser total dagslengde i timer.
    axes[0].plot(
        daylight_dataframe["date"],
        daylight_dataframe["day_length"].dt.total_seconds() / 3600,
        linewidth=2,
    )
    axes[0].set_title("Day Length Over Time")
    axes[0].set_ylabel("Hours")
    axes[0].grid(alpha=0.3)

    # Andre graf viser hvor mange minutter dagen øker fra måling til måling.
    axes[1].bar(
        daylight_dataframe["date"],
        daylight_dataframe["daily_increase"].dt.total_seconds() / 60,
        width=1.5,
    )
    axes[1].set_title("Daily Increase")
    axes[1].set_ylabel("Minutes")
    axes[1].grid(alpha=0.3)

    # Strammer inn layouten før figuren lagres og lukkes.
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
