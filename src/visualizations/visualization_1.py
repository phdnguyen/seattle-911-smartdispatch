# streamlit run app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

RESP = "first_spd_call_sign_response_time_s"
DATETIME_COL = "cad_event_original_time_queued_datetime"

st.set_page_config(page_title="Seattle 911 – Response Time Explorer", layout="wide")

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # basic clean
    df = df[df[RESP].notna() & (df[RESP] > 0)]
    # remove REDACTED location fields 
    for c in ["dispatch_neighborhood", "dispatch_sector"]:
        if c in df.columns:
            df = df[~df[c].astype(str).str.lower().str.contains("redacted", na=False)]
    # time fields
    ts = pd.to_datetime(df[DATETIME_COL], errors="coerce")
    df = df[ts.notna()].copy()
    df["queued_ts"] = pd.to_datetime(df[DATETIME_COL], errors="coerce")
    df["month"] = df["queued_ts"].dt.month
    df["month_name"] = df["queued_ts"].dt.strftime("%b")
    df["dow_num"] = df["queued_ts"].dt.dayofweek + 1
    df["dow"] = pd.Categorical(
        df["queued_ts"].dt.strftime("%a"),
        categories=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        ordered=True
    )
    df["hour"] = df["queued_ts"].dt.hour
    # convert seconds → minutes for easier interpretation
    df["response_time_min"] = df[RESP] / 60.0
    return df

# ---------------- Sidebar ----------------
st.sidebar.title("Load data")
path = st.sidebar.text_input(
    "Processed CSV path",
    value="data/processed/call_data_20251019_processed_v3.csv"
)
try:
    df = load_data(path)
except Exception as e:
    st.error(f"Could not load CSV: {e}")
    st.stop()

st.sidebar.title("Filters")
call_types = ["All"] + sorted(df["call_type"].dropna().unique().tolist()) if "call_type" in df.columns else ["All"]
priorities = ["All"] + sorted(df["priority"].dropna().unique().tolist(), key=lambda x: str(x)) if "priority" in df.columns else ["All"]
sectors    = ["All"] + sorted(df["dispatch_sector"].dropna().unique().tolist()) if "dispatch_sector" in df.columns else ["All"]

sel_call = st.sidebar.selectbox("Call Type", call_types, index=0)
sel_prio = st.sidebar.selectbox("Priority", priorities, index=0)
sel_sect = st.sidebar.selectbox("Dispatch Sector", sectors, index=0)

# ---------------- Metric selector ----------------
metric = st.sidebar.radio("Metric", ["avg", "median", "min", "max"], horizontal=True)
metric_map = {
    "avg": ("Average (min)", "mean"),
    "median": ("Median (min)", "median"),
    "min": ("Minimum (min)", "min"),
    "max": ("Maximum (min)", "max")
}
metric_label, agg_fn = metric_map[metric]

# Time axes
st.sidebar.title("Time Axes")
axis_options = {
    "Month": "month_name",
    "Day of Week": "dow",
    "Hour of Day": "hour",
}
x_axis_label = st.sidebar.selectbox("X-Axis", list(axis_options.keys()), index=1)
y_axis_label = st.sidebar.selectbox("Y-Axis", list(axis_options.keys()), index=2)

if x_axis_label == y_axis_label:
    st.sidebar.warning("Pick two different axes; they must not be the same.")
    st.stop()

# ---------------- Filtering ----------------
df_f = df.copy()
if sel_call != "All":
    df_f = df_f[df_f["call_type"] == sel_call]
if sel_prio != "All":
    df_f = df_f[df_f["priority"] == sel_prio]
if sel_sect != "All":
    df_f = df_f[df_f["dispatch_sector"] == sel_sect]

st.title("Seattle 911 – Response Time Explorer")
st.caption("Interactive analysis of SPD response time by incident context and time patterns (in minutes).")

# ---------------- KPIs ----------------
mins = df_f["response_time_min"]
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Rows (after filters)", f"{len(df_f):,}")
c2.metric("Avg (min)", f"{mins.mean():.2f}" if not df_f.empty else "—")
c3.metric("Median (min)", f"{mins.median():.2f}" if not df_f.empty else "—")
c4.metric("Min (min)", f"{mins.min():.2f}" if not df_f.empty else "—")
c5.metric("Max (min)", f"{mins.max():.2f}" if not df_f.empty else "—")

if df_f.empty:
    st.warning("No rows after filters.")
    st.stop()

# ---------------- Aggregation & Heatmap ----------------
x_col = axis_options[x_axis_label]
y_col = axis_options[y_axis_label]

def order_for(colname: str):
    if colname == "dow":
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if colname == "month_name":
        return ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    if colname == "hour":
        return list(range(24))
    return None

order_x = order_for(x_col)
order_y = order_for(y_col)

agg_df = (
    df_f.groupby([y_col, x_col], dropna=False)["response_time_min"]
        .agg([agg_fn, "count"])
        .reset_index()
        .rename(columns={agg_fn: "value", "count": "n"})
)

if order_x is not None:
    agg_df[x_col] = pd.Categorical(agg_df[x_col], categories=order_x, ordered=True)
if order_y is not None:
    agg_df[y_col] = pd.Categorical(agg_df[y_col], categories=order_y, ordered=True)

pivot = agg_df.pivot_table(index=y_col, columns=x_col, values="value", aggfunc="mean")
pivot = pivot.sort_index().sort_index(axis=1)

title = (
    f"{metric_label} Response Time (min) • "
    f"CallType: {sel_call} • Priority: {sel_prio} • Sector: {sel_sect}"
)

fig = px.imshow(
    pivot,
    color_continuous_scale="YlOrRd",
    origin="upper",
    aspect="auto",
    labels=dict(x=x_axis_label, y=y_axis_label, color="Minutes"),
    title=title
)
fig.update_layout(margin=dict(l=50, r=20, t=70, b=50), height=560)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Optional aggregated table ----------------
with st.expander("Show aggregated table"):
    st.dataframe(agg_df.sort_values(["value"], ascending=False), use_container_width=True)