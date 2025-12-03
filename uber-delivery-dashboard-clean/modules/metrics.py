from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Kpis:
    avg_atd: float
    p95_atd: float
    on_time_rate: float
    avg_pickup_km: float
    avg_dropoff_km: float


def compute_kpis(df: pd.DataFrame, atd_threshold: int) -> Kpis:
    atd = df["ATD"].dropna()
    pickup = df["pickup_distance"].dropna()
    dropoff = df["dropoff_distance"].dropna()

    avg_atd = float(atd.mean()) if not atd.empty else float("nan")
    p95_atd = float(np.percentile(atd, 95)) if not atd.empty else float("nan")

    on_time = (df["ATD"] <= atd_threshold).astype("float")
    on_time_rate = float(on_time.mean()) if not on_time.empty else float("nan")

    avg_pickup_km = float(pickup.mean()) if not pickup.empty else float("nan")
    avg_dropoff_km = float(dropoff.mean()) if not dropoff.empty else float("nan")

    return Kpis(
        avg_atd=avg_atd,
        p95_atd=p95_atd,
        on_time_rate=on_time_rate,
        avg_pickup_km=avg_pickup_km,
        avg_dropoff_km=avg_dropoff_km,
    )
