from __future__ import annotations

import pandas as pd
import plotly.express as px


def apply_uber_theme(fig):
    """Apply dark theme """
    fig.update_layout(
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font=dict(color="white"),
        xaxis=dict(color="white", gridcolor="#333333"),
        yaxis=dict(color="white", gridcolor="#333333"),
        title_font=dict(color="white"),
    )
    return fig


def plot_atd_histogram(df: pd.DataFrame):
    df = df.copy()

    # Remove extreme outliers
    df = df[df["ATD"].between(0, 120)]

    fig = px.histogram(
        df,
        x="ATD",
        nbins=100,  # more bins = more detail
        title="ATD distribution (0–120 minutes)",
        labels={"ATD": "ATD (minutes)", "count": "Count"},
        color_discrete_sequence=["#06C167"],  # Uber green
    )

    fig.update_layout(
        bargap=0.01,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
    )

    return apply_uber_theme(fig)


def plot_atd_by_courier_flow(df: pd.DataFrame):
    fig = px.box(
        df,
        x="courier_flow",
        y="ATD",
        title="ATD by courier flow",
        color_discrete_sequence=["#06C167"],
    )
    fig.update_layout(
        xaxis_title="Courier flow",
        yaxis_title="ATD (minutes)",
    )
    return apply_uber_theme(fig)


def plot_atd_by_territory(df: pd.DataFrame):
    grouped = (
        df.groupby("territory", as_index=False)["ATD"]
        .mean()
        .rename(columns={"ATD": "avg_ATD"})
    )

    fig = px.bar(
        grouped,
        x="territory",
        y="avg_ATD",
        title="Average ATD by territory",
        color_discrete_sequence=["#06C167"],
    )
    fig.update_layout(
        xaxis_title="Territory",
        yaxis_title="Avg ATD (minutes)",
        xaxis_tickangle=-45,
    )
    return apply_uber_theme(fig)


def plot_distance_scatter(df: pd.DataFrame):
    df = df.copy()
    df["total_distance"] = (
        df["pickup_distance"].fillna(0.0)
        + df["dropoff_distance"].fillna(0.0)
    )

    fig = px.scatter(
        df,
        x="total_distance",
        y="ATD",
        color="courier_flow",
        title="ATD vs total distance",
        opacity=0.6,
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(
        xaxis_title="Total distance (km)",
        yaxis_title="ATD (minutes)",
    )
    return apply_uber_theme(fig)
