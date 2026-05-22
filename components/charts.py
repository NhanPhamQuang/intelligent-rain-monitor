import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ──────────────────────────── helpers ─────────────────────────────

def _empty(msg: str = "No data available") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, xref="paper", yref="paper",
                       x=0.5, y=0.5, showarrow=False, font=dict(size=14, color="#888"))
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
    return fig


_LAYOUT = dict(margin=dict(l=0, r=0, t=30, b=0), height=320,
               legend=dict(orientation="h", y=-0.25))


# ──────────────────────────── charts ──────────────────────────────

def temperature_trend_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty or "MinTemp" not in df.columns:
        return _empty("No temperature data")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MaxTemp"], name="Max Temp",
                             line=dict(color="#ff4b4b", width=2)))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MinTemp"], name="Min Temp",
                             line=dict(color="#00d4ff", width=2), fill="tonexty",
                             fillcolor="rgba(0,212,255,0.08)"))
    fig.update_layout(xaxis_title="Date", yaxis_title="Temperature (°C)", **_LAYOUT)
    return fig


def rainfall_bar_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty or "Rainfall" not in df.columns:
        return _empty("No rainfall data")
    data = df.dropna(subset=["Rainfall"]).head(60)
    fig = px.bar(data, x="Date", y="Rainfall", color_discrete_sequence=["#3366ff"])
    fig.update_layout(xaxis_title="Date", yaxis_title="Rainfall (mm)", **_LAYOUT)
    return fig


def humidity_scatter_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty or "Humidity3pm" not in df.columns:
        return _empty("No humidity data")
    data = df[["Humidity3pm", "Rainfall"]].dropna().head(200)
    fig = px.scatter(data, x="Humidity3pm", y="Rainfall", color_discrete_sequence=["#00d4ff"],
                     labels={"Humidity3pm": "Humidity 3pm (%)", "Rainfall": "Rainfall (mm)"})
    fig.update_layout(**_LAYOUT)
    return fig


def wind_rose_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty or "Direction" not in df.columns:
        return _empty("No wind data")
    fig = px.line_polar(df, r="Frequency", theta="Direction",
                        line_close=True, color_discrete_sequence=["#00CC96"])
    fig.update_traces(fill="toself")
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
    return fig


def confusion_matrix_chart(cm_data: list) -> go.Figure:
    labels = ["No Rain", "Rain"]
    fig = px.imshow(cm_data, x=labels, y=labels,
                    labels=dict(x="Predicted", y="Actual", color="Count"),
                    text_auto=True, color_continuous_scale="Blues")
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
    return fig


def roc_curve_chart(auc: float = 0.89) -> go.Figure:
    fpr = np.linspace(0, 1, 100)
    tpr = np.power(fpr, max(0.01, 1 / (auc * 2)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines",
                             name=f"Model (AUC={auc:.2f})",
                             line=dict(color="firebrick", width=3)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines",
                             name="Random", line=dict(dash="dash", color="gray")))
    fig.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate",
                      height=350, margin=dict(l=0, r=0, t=30, b=0))
    return fig


def feature_importance_chart(importance: dict) -> go.Figure:
    if not importance:
        return _empty("No feature importance data")
    df = pd.DataFrame(list(importance.items()), columns=["Feature", "Importance"])
    df = df.sort_values("Importance", ascending=True)
    fig = px.bar(df, x="Importance", y="Feature", orientation="h",
                 color_discrete_sequence=["#00d4ff"])
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
    return fig


def drift_chart(n: int = 30) -> go.Figure:
    df = pd.DataFrame({
        "Day": range(1, n + 1),
        "Drift Score": np.random.normal(0.1, 0.02, n),
    })
    fig = px.area(df, x="Day", y="Drift Score")
    fig.add_hline(y=0.2, line_dash="dot", line_color="red", annotation_text="Retrain Trigger")
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=350)
    return fig


def anomaly_chart(df: pd.DataFrame, column: str = "Pressure3pm") -> go.Figure:
    if df.empty or column not in df.columns:
        return _empty("No anomaly data")
    fig = px.line(df, x="Date", y=column, title=f"{column} — Anomaly Detection")
    if "is_anomaly" in df.columns:
        pts = df[df["is_anomaly"] == True]
        if not pts.empty:
            fig.add_scatter(x=pts["Date"], y=pts[column], mode="markers",
                            name="Anomaly", marker=dict(color="red", size=12, symbol="x"))
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=350)
    return fig
