from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["ATD"] = pd.to_numeric(df["ATD"], errors="coerce")
    df["pickup_distance"] = pd.to_numeric(
        df["pickup_distance"], errors="coerce"
    )
    df["dropoff_distance"] = pd.to_numeric(
        df["dropoff_distance"], errors="coerce"
    )

    for col in [
        "restaurant_offered_timestamp_utc",
        "order_final_state_timestamp_local",
        "eater_request_timestamp_local",
    ]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def filter_data(
    df: pd.DataFrame,
    territories: Optional[Iterable[str]] = None,
    courier_flows: Optional[Iterable[str]] = None,
    merchant_surfaces: Optional[Iterable[str]] = None,
) -> pd.DataFrame:

    df_filtered = df.copy()

    if territories:
        df_filtered = df_filtered[df_filtered["territory"].isin(territories)]

    if courier_flows:
        df_filtered = df_filtered[
            df_filtered["courier_flow"].isin(courier_flows)
        ]

    if merchant_surfaces:
        df_filtered = df_filtered[
            df_filtered["merchant_surface"].isin(merchant_surfaces)
        ]

    return df_filtered
