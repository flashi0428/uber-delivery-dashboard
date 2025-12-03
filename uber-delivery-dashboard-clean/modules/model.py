from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Optional, Tuple

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

import plotly.express as px
from sklearn.inspection import partial_dependence



def prepare_features(df: pd.DataFrame):
    df = df.copy()

    df = df.dropna(subset=["ATD"])
    df = df[df["ATD"].between(5, 180)]

    if df.shape[0] < 200:
        return None

    ts = pd.to_datetime(df["order_final_state_timestamp_local"], errors="coerce")
    df["hour_of_day"] = ts.dt.hour
    df["day_of_week"] = ts.dt.weekday
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Distance feature
    df["total_distance_km"] = (
        df["pickup_distance"].fillna(0.0)
        + df["dropoff_distance"].fillna(0.0)
    )

    numeric = [
        "pickup_distance",
        "dropoff_distance",
        "total_distance_km",
        "hour_of_day",
        "day_of_week",
        "is_weekend",
    ]

    categorical = [
        "territory",
        "courier_flow",
        "merchant_surface",
        "geo_archetype",
    ]

    X = df[numeric + categorical]
    y = df["ATD"].astype(float)

    return X, y, numeric, categorical


# -------------------------------------------------------
# Random Forest Model
# -------------------------------------------------------
def train_random_forest_model(df: pd.DataFrame):
    prepared = prepare_features(df)
    if prepared is None:
        return None

    X, y, numeric_cols, categorical_cols = prepared

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    model = Pipeline(
        steps=[
            ("prep", preprocessor),
            ("rf", RandomForestRegressor(
                n_estimators=120,
                max_depth=12,
                min_samples_split=10,
                n_jobs=-1,
                random_state=42
            ))
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return model, X_test, y_test, y_pred, numeric_cols, categorical_cols



def model_summary_text(y_test, y_pred):
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return (
        f"MAE: {mae:.2f} minutes\n"
        f"R-squared: {r2:.3f}\n\n"
        "Interpretation:\n"
        "- MAE = average prediction error.\n"
        "- Higher R² means better ability to explain ATD variation.\n"
        "- Random Forest models capture non-linear effects and interactions.\n"
    )


# -------------------------------------------------------
# Feature Importance
# -------------------------------------------------------
def get_feature_importance_df(model, numeric_cols, categorical_cols):
    ohe = model.named_steps["prep"].named_transformers_["cat"]["onehot"]
    cat_feature_names = ohe.get_feature_names_out(categorical_cols)

    final_features = numeric_cols + list(cat_feature_names)

    importances = model.named_steps["rf"].feature_importances_

    df_imp = pd.DataFrame({
        "feature": final_features,
        "importance": importances
    }).sort_values("importance", ascending=False)

    return df_imp


def plot_feature_importance(df_imp):
    fig = px.bar(
        df_imp.head(15),
        x="importance",
        y="feature",
        orientation="h",
        title="Top 15 Feature Importances",
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig


# -------------------------------------------------------
# Partial Dependence Plot
# -------------------------------------------------------
def plot_pdp(model, X, feature_name, feature_index):
    pdp = partial_dependence(
        model,
        X,
        features=[feature_index],
        kind="average"
    )

    values = pdp["values"][0]
    pd_values = pdp["average"][0]

    fig = px.line(
        x=values,
        y=pd_values,
        labels={"x": feature_name, "y": "ATD"},
        title=f"Partial Dependence: {feature_name}"
    )
    return fig
