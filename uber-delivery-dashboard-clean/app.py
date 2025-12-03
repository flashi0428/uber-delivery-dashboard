# app.py

from __future__ import annotations

import streamlit as st

from modules.data_loader import load_data
from modules.preprocessing import add_derived_columns, filter_data
from modules.metrics import compute_kpis
from modules.charts import (
    plot_atd_histogram,
    plot_atd_by_courier_flow,
    plot_atd_by_territory,
    plot_distance_scatter,
)
from modules.model import (
    train_random_forest_model,
    model_summary_text,
    get_feature_importance_df,
    plot_feature_importance,
    plot_pdp,
)


def main() -> None:
    st.set_page_config(
        page_title="Delivery Time & ATD Dashboard",
        layout="wide",
    )

    # Small CSS tweak for black background around charts
    st.markdown(
        """
        <style>
        .stPlotlyChart {
            background-color: #000000 !important;
        }
        .block-container {
            padding-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Uber – Delivery Time & ATD Dashboard")
    st.caption(
        "Analyze Actual Time of Delivery (ATD), distances and operational "
        "performance by territory, courier flow and other dimensions."
    )

    # -------------------------
    # Data loading & prep
    # -------------------------
    df_raw = load_data("data/delivery_weekly.csv")
    df = add_derived_columns(df_raw)

    # -------------------------
    # Sidebar filters
    # -------------------------
    st.sidebar.header("Filters")

    territories = sorted(df["territory"].dropna().unique().tolist())
    selected_territories = st.sidebar.multiselect(
        "Territory", options=territories, default=territories
    )

    courier_flows = sorted(df["courier_flow"].dropna().unique().tolist())
    selected_flows = st.sidebar.multiselect(
        "Courier flow", options=courier_flows, default=courier_flows
    )

    surfaces = sorted(df["merchant_surface"].dropna().unique().tolist())
    selected_surfaces = st.sidebar.multiselect(
        "Merchant surface", options=surfaces, default=surfaces
    )

    atd_threshold = st.sidebar.slider(
        "On-time threshold (minutes)",
        min_value=10,
        max_value=90,
        value=35,
        step=5,
        help="Deliveries with ATD <= threshold are considered on-time.",
    )

    df_filtered = filter_data(
        df=df,
        territories=selected_territories,
        courier_flows=selected_flows,
        merchant_surfaces=selected_surfaces,
    )

    if df_filtered.empty:
        st.warning("No data for the selected filters. Try widening the filters.")
        return

    # -------------------------
    # KPIs
    # -------------------------
    kpis = compute_kpis(df_filtered, atd_threshold)

    kpi_cols = st.columns(5)
    kpi_cols[0].metric("Avg ATD (min)", f"{kpis.avg_atd:.1f}")
    kpi_cols[1].metric("P95 ATD (min)", f"{kpis.p95_atd:.1f}")
    kpi_cols[2].metric("On-time rate", f"{kpis.on_time_rate:.1%}")
    kpi_cols[3].metric("Avg pickup distance (km)", f"{kpis.avg_pickup_km:.2f}")
    kpi_cols[4].metric("Avg dropoff distance (km)", f"{kpis.avg_dropoff_km:.2f}")

    st.markdown("---")

    # -------------------------
    # ATD distribution & by courier_flow
    # -------------------------
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader("ATD distribution")
        fig_hist = plot_atd_histogram(df_filtered)
        st.plotly_chart(fig_hist, use_container_width=True)

    with row1_col2:
        st.subheader("ATD by courier flow")
        fig_box = plot_atd_by_courier_flow(df_filtered)
        st.plotly_chart(fig_box, use_container_width=True)

    # -------------------------
    # Geography & distances
    # -------------------------
    st.markdown("---")
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.subheader("ATD by territory")
        fig_territory = plot_atd_by_territory(df_filtered)
        st.plotly_chart(fig_territory, use_container_width=True)

    with row2_col2:
        st.subheader("ATD vs distance")
        fig_scatter = plot_distance_scatter(df_filtered)
        st.plotly_chart(fig_scatter, use_container_width=True)

    # -------------------------
    # Predictive model (Random Forest)
    # -------------------------
    st.markdown("---")
    st.subheader("Predictive model Random Forest")

    enable_rf = st.checkbox(
        "Train Random Forest ", value=False
    )

    if enable_rf:
        result = train_random_forest_model(df_filtered)

        if result is None:
            st.warning("Not enough data to train the model.")
        else:
            model, X_test, y_test, y_pred, num_cols, cat_cols = result

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Model performance")
                st.text(model_summary_text(y_test, y_pred))

            with col2:
                st.markdown("### Feature importance")
                imp_df = get_feature_importance_df(model, num_cols, cat_cols)
                fig_imp = plot_feature_importance(imp_df)
                st.plotly_chart(fig_imp, use_container_width=True)

            # PDP for top features
            st.markdown("---")
            st.markdown("### Partial dependence – top predictors")

            top3 = imp_df.head(3)

            for feature in top3["feature"]:
                try:
                    idx = list(imp_df["feature"]).index(feature)
                    fig_pdp = plot_pdp(
                        model,
                        X_test,
                        feature_name=feature,
                        feature_index=idx,
                    )
                    st.plotly_chart(fig_pdp, use_container_width=True)
                except Exception:
                    continue

    # -------------------------
    # Insight note
    # -------------------------
    st.markdown("---")
    st.markdown(
        "💡 *Tip for users:* use the filters on the left to identify "
        "territories, courier flows or surfaces where ATD is high or "
        "on-time rate is low, and prioritize operational interventions there."
    )


if __name__ == "__main__":
    main()
