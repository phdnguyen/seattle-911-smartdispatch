# streamlit run visualization_1.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
RESP = "first_spd_call_sign_response_time_s"
CAD_ID = "cad_event_number"
DATETIME_COL = "cad_event_original_time_queued_datetime"

st.set_page_config(page_title="Seattle 911 Explorer", layout="wide")

# -------------------------------------------------------------------
# Data loaders
# -------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_main_data(path: str) -> pd.DataFrame:
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
    df["queued_ts"] = ts

    df["month"] = df["queued_ts"].dt.month
    df["month_name"] = df["queued_ts"].dt.strftime("%b")
    df["dow_num"] = df["queued_ts"].dt.dayofweek + 1
    df["dow"] = pd.Categorical(
        df["queued_ts"].dt.strftime("%a"),
        categories=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        ordered=True,
    )
    df["hour"] = df["queued_ts"].dt.hour

    # seconds → minutes (for response time)
    df["response_time_min"] = df[RESP] / 60.0
    return df


@st.cache_data(show_spinner=False)
def load_burst_data(path: str) -> pd.DataFrame:
    """
    Burst / volume anomaly table:
    cad_event_number,is_anomaly,date,hour,call_type_filtered,total_calls, ...
    """
    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = df["hour"].astype(int)
    df = df[df["date"].notna()].copy()

    df["datetime"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

    if "call_type_filtered" in df.columns:
        df["call_type"] = df["call_type_filtered"]

    if "is_anomaly" in df.columns:
        df["is_anomaly"] = df["is_anomaly"].fillna(0).astype(int)

    df["DayOfWeek"] = df["datetime"].dt.day_name()

    return df


@st.cache_data(show_spinner=False)
def load_response_data(path: str) -> pd.DataFrame:
    """
    Response-time anomaly table:
    cad_event_number,is_anomaly,date,hour,call_type_filtered,total_calls,
    avg_service_time,...
    """
    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = df["hour"].astype(int)
    df = df[df["date"].notna()].copy()

    df["datetime"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

    if "call_type_filtered" in df.columns:
        df["call_type"] = df["call_type_filtered"]

    # avg_service_time must be numeric and non-null
    df["avg_service_time"] = pd.to_numeric(df.get("avg_service_time"), errors="coerce")
    df = df[df["avg_service_time"].notna()].copy()

    if "is_anomaly" in df.columns:
        df["is_anomaly"] = df["is_anomaly"].fillna(0).astype(int)

    df["DayOfWeek"] = df["datetime"].dt.day_name()

    return df


@st.cache_data(show_spinner=False)
def build_volume_baseline(vis: pd.DataFrame) -> pd.DataFrame:
    """
    Baseline stats by (call_type, DayOfWeek, hour) for volume anomalies.
    """
    df = vis.copy()
    baselines = (
        df.groupby(["call_type", "DayOfWeek", "hour"], dropna=False)["total_calls"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    baselines["std"] = baselines["std"].replace(0, 1.0)
    return baselines


@st.cache_data(show_spinner=False)
def build_response_baseline(vis: pd.DataFrame) -> pd.DataFrame:
    """
    Baseline stats by (call_type, DayOfWeek, hour) for response-time anomalies.
    """
    df = vis.copy()
    df = df[df["avg_service_time"].notna()]
    baselines = (
        df.groupby(["call_type", "DayOfWeek", "hour"], dropna=False)["avg_service_time"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    baselines["std"] = baselines["std"].replace(0, 1.0)
    baselines = baselines[baselines["mean"].notna()].copy()
    return baselines


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def order_for(colname: str):
    if colname == "dow":
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if colname == "month_name":
        return [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
    if colname == "hour":
        return list(range(24))
    return None


# -------------------------------------------------------------------
# Sidebar: file paths and filters
# -------------------------------------------------------------------
st.sidebar.title("Load data")
main_path = st.sidebar.text_input(
    "Processed CSV path (main data)",
    value="data/processed/calldata_20251019_processed_v4.csv",
)
burst_path = st.sidebar.text_input(
    "Burst anomaly CSV path",
    value="data/output/burst_anomaly_table.csv",
)
resp_path = st.sidebar.text_input(
    "Response-time anomaly CSV path",
    value="data/output/response_anomaly_table.csv",
)

try:
    df = load_main_data(main_path)
    burst_df = load_burst_data(burst_path)
    resp_df = load_response_data(resp_path)
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

st.sidebar.title("Filters")

call_types = (
    ["All"]
    + sorted(df.get("call_type", pd.Series()).dropna().unique().tolist())
    if "call_type" in df.columns
    else ["All"]
)
priorities = (
    ["All"]
    + sorted(df.get("priority", pd.Series()).dropna().unique().tolist(), key=lambda x: str(x))
    if "priority" in df.columns
    else ["All"]
)
sectors = (
    ["All"]
    + sorted(df.get("dispatch_sector", pd.Series()).dropna().unique().tolist())
    if "dispatch_sector" in df.columns
    else ["All"]
)
neighborhoods = (
    ["All"]
    + sorted(df.get("dispatch_neighborhood", pd.Series()).dropna().unique().tolist())
    if "dispatch_neighborhood" in df.columns
    else ["All"]
)

sel_call = st.sidebar.selectbox("Call Type", call_types, index=0)
sel_prio = st.sidebar.selectbox("Priority", priorities, index=0)
sel_sect = st.sidebar.selectbox("Dispatch Sector", sectors, index=0)
sel_neigh = st.sidebar.selectbox("Dispatch Neighborhood", neighborhoods, index=0)

# Metric selector (for response-time heatmap values)
metric = st.sidebar.radio("Metric", ["avg", "median", "min", "max"], horizontal=True)
metric_map = {
    "avg": ("Average (min)", "mean"),
    "median": ("Median (min)", "median"),
    "min": ("Minimum (min)", "min"),
    "max": ("Maximum (min)", "max"),
}
metric_label, agg_fn = metric_map[metric]

# Time axes
st.sidebar.title("Time Axes")
axis_options = {
    "Month": "month_name",
    "Day of Week": "dow",
    "Hour of Day": "hour",
}
x_axis_label = st.sidebar.selectbox("X-Axis", list(axis_options.keys()), index=1)  # DOW
y_axis_label = st.sidebar.selectbox("Y-Axis", list(axis_options.keys()), index=2)  # Hour

if x_axis_label == y_axis_label:
    st.sidebar.warning("Pick two different axes; they must not be the same.")
    st.stop()

x_col = axis_options[x_axis_label]
y_col = axis_options[y_axis_label]
order_x = order_for(x_col)
order_y = order_for(y_col)

# -------------------------------------------------------------------
# Apply filters to main dataframe
# -------------------------------------------------------------------
df_f = df.copy()
if sel_call != "All" and "call_type" in df_f.columns:
    df_f = df_f[df_f["call_type"] == sel_call]
if sel_prio != "All" and "priority" in df_f.columns:
    df_f = df_f[df_f["priority"] == sel_prio]
if sel_sect != "All" and "dispatch_sector" in df_f.columns:
    df_f = df_f[df_f["dispatch_sector"] == sel_sect]
if sel_neigh != "All" and "dispatch_neighborhood" in df_f.columns:
    df_f = df_f[df_f["dispatch_neighborhood"] == sel_neigh]

if df_f.empty:
    st.warning("No rows after filters.")
    st.stop()

# -------------------------------------------------------------------
# SECTION 1: Seattle 911 – Response Time Explorer
# -------------------------------------------------------------------
st.title("Seattle 911 – Response Time Explorer")
st.caption(
    "Interactive analysis of SPD response time by incident context and time patterns (in minutes)."
)

mins = df_f["response_time_min"]
p95 = mins.quantile(0.95)

# response anomaly subset for anomaly % (filtered by same context)
resp_subset_for_pct = resp_df.copy()
if sel_call != "All" and "call_type" in resp_subset_for_pct.columns:
    resp_subset_for_pct = resp_subset_for_pct[resp_subset_for_pct["call_type"] == sel_call]
if sel_sect != "All" and "dispatch_sector" in resp_subset_for_pct.columns:
    resp_subset_for_pct = resp_subset_for_pct[resp_subset_for_pct["dispatch_sector"] == sel_sect]
if sel_neigh != "All" and "dispatch_neighborhood" in resp_subset_for_pct.columns:
    resp_subset_for_pct = resp_subset_for_pct[
        resp_subset_for_pct["dispatch_neighborhood"] == sel_neigh
    ]

total_hours_resp = len(resp_subset_for_pct)
anomaly_hours_resp = (
    int(resp_subset_for_pct["is_anomaly"].sum()) if total_hours_resp > 0 else 0
)
anomaly_pct_resp = (
    anomaly_hours_resp / total_hours_resp * 100.0 if total_hours_resp > 0 else 0.0
)

# KPIs
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Rows (after filters)", f"{len(df_f):,}")
c2.metric("Avg (min)", f"{mins.mean():.2f}")
c3.metric("Median (min)", f"{mins.median():.2f}")
c4.metric("95th percentile (min)", f"{p95:.2f}")
c5.metric("Min (min)", f"{mins.min():.2f}")
c6.metric("Max (min)", f"{mins.max():.2f}")

st.write(
    f"**Slow-response anomaly hours (context-filtered):** {anomaly_hours_resp:,} / "
    f"{total_hours_resp:,} ({anomaly_pct_resp:.2f}%)"
)

# Aggregation for heatmap
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

pivot = (
    agg_df.pivot_table(index=y_col, columns=x_col, values="value", aggfunc="mean")
    .sort_index()
    .sort_index(axis=1)
)

title_rt = (
    f"{metric_label} Response Time (min) • "
    f"CallType: {sel_call} • Priority: {sel_prio} • "
    f"Sector: {sel_sect} • Neighborhood: {sel_neigh}"
)

fig_rt = px.imshow(
    pivot,
    color_continuous_scale="YlOrRd",
    origin="upper",
    aspect="auto",
    labels=dict(x=x_axis_label, y=y_axis_label, color="Minutes"),
    title=title_rt,
)
fig_rt.update_layout(margin=dict(l=50, r=20, t=70, b=50), height=560)
st.plotly_chart(fig_rt, use_container_width=True)

# Worst-performing cell (by median response time)
cell_stats = (
    df_f.groupby([y_col, x_col])["response_time_min"]
    .median()
    .reset_index()
    .rename(columns={"response_time_min": "median_rt"})
)
if not cell_stats.empty:
    worst = cell_stats.loc[cell_stats["median_rt"].idxmax()]
    worst_label = (
        f"{y_axis_label}={worst[y_col]}, {x_axis_label}={worst[x_col]} "
        f"({worst['median_rt']:.1f} min median)"
    )
    st.caption(f"**Worst median-response cell:** {worst_label}")

with st.expander("Show aggregated table (response time)"):
    st.dataframe(agg_df.sort_values("value", ascending=False), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 2: Seattle 911 – Call Frequency Explorer
# -------------------------------------------------------------------
st.header("Seattle 911 – Call Frequency Explorer")
st.caption(
    "Unique CAD events per time cell. KPIs use aggregate statistics across cells; "
    "the heatmap shows per-cell frequency (counts)."
)

freq_df = (
    df_f.groupby([y_col, x_col], dropna=False)[CAD_ID]
    .nunique()
    .reset_index()
    .rename(columns={CAD_ID: "freq"})
)

if order_x is not None:
    freq_df[x_col] = pd.Categorical(freq_df[x_col], categories=order_x, ordered=True)
if order_y is not None:
    freq_df[y_col] = pd.Categorical(freq_df[y_col], categories=order_y, ordered=True)

freq_vals = freq_df["freq"]

fc1, fc2, fc3, fc4, fc5 = st.columns(5)
fc1.metric(
    "Total calls (unique CAD)", f"{df_f[CAD_ID].nunique():,}"
    if CAD_ID in df_f.columns
    else "—",
)
fc2.metric("Avg calls / cell", f"{freq_vals.mean():.2f}" if not freq_df.empty else "—")
fc3.metric(
    "Median calls / cell", f"{freq_vals.median():.2f}" if not freq_df.empty else "—"
)
fc4.metric(
    "Min calls / cell", f"{freq_vals.min():.0f}" if not freq_df.empty else "—"
)
fc5.metric(
    "Max calls / cell", f"{freq_vals.max():.0f}" if not freq_df.empty else "—"
)

pivot_freq = (
    freq_df.pivot_table(index=y_col, columns=x_col, values="freq", aggfunc="sum")
    .sort_index()
    .sort_index(axis=1)
)

title_freq = (
    f"Call Frequency (unique CAD per cell) • "
    f"CallType: {sel_call} • Priority: {sel_prio} • "
    f"Sector: {sel_sect} • Neighborhood: {sel_neigh}"
)

fig_freq = px.imshow(
    pivot_freq,
    color_continuous_scale="YlOrRd",
    origin="upper",
    aspect="auto",
    labels=dict(x=x_axis_label, y=y_axis_label, color="Calls"),
    title=title_freq,
)
fig_freq.update_layout(margin=dict(l=50, r=20, t=70, b=50), height=560)
st.plotly_chart(fig_freq, use_container_width=True)

with st.expander("Show aggregated table (frequency)"):
    st.dataframe(freq_df.sort_values("freq", ascending=False), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 3A: Incident Flow Timeline — Volume Anomalies
# -------------------------------------------------------------------
st.header("Incident Flow Timeline — Hourly 911 Calls (Volume Anomalies)")

vol_subset = burst_df.copy()
if sel_call != "All" and "call_type" in vol_subset.columns:
    vol_subset = vol_subset[vol_subset["call_type"] == sel_call]
if sel_sect != "All" and "dispatch_sector" in vol_subset.columns:
    vol_subset = vol_subset[vol_subset["dispatch_sector"] == sel_sect]
if sel_neigh != "All" and "dispatch_neighborhood" in vol_subset.columns:
    vol_subset = vol_subset[vol_subset["dispatch_neighborhood"] == sel_neigh]

t1, t2, t3 = st.columns(3)
t1.metric("Rows (hourly bins)", f"{len(vol_subset):,}")
t2.metric("Total calls (sum of total_calls)", f"{int(vol_subset['total_calls'].sum()):,}")
t3.metric("Anomaly hours", f"{int(vol_subset['is_anomaly'].sum()):,}")

if not vol_subset.empty:
    fig_tl = px.scatter(
        vol_subset,
        x="datetime",
        y="total_calls",
        color="call_type",
        symbol="is_anomaly",
        symbol_map={0: "circle", 1: "x"},
        labels={"total_calls": "Number of calls per hour", "datetime": "Date / Hour"},
        hover_data=[
            "call_type",
            "total_calls",
            "is_anomaly",
            "dispatch_sector",
            "dispatch_neighborhood",
        ],
        title="Hourly 911 Calls — Volume Anomalies Highlighted",
    )
    fig_tl.update_traces(marker=dict(size=7, opacity=0.7))
    fig_tl.update_layout(height=520, margin=dict(l=40, r=20, t=70, b=60))
    st.plotly_chart(fig_tl, use_container_width=True)

with st.expander("Show volume anomaly table"):
    st.dataframe(vol_subset.sort_values("datetime"), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 3B: Incident Flow Timeline — Response-Time Anomalies
# -------------------------------------------------------------------
st.header("Incident Flow Timeline — Slow Response Time Anomalies")

resp_subset = resp_df.copy()
if sel_call != "All" and "call_type" in resp_subset.columns:
    resp_subset = resp_subset[resp_subset["call_type"] == sel_call]
if sel_sect != "All" and "dispatch_sector" in resp_subset.columns:
    resp_subset = resp_subset[resp_subset["dispatch_sector"] == sel_sect]
if sel_neigh != "All" and "dispatch_neighborhood" in resp_subset.columns:
    resp_subset = resp_subset[resp_subset["dispatch_neighborhood"] == sel_neigh]

resp_subset = resp_subset[resp_subset["avg_service_time"].notna()]

r1, r2, r3 = st.columns(3)
r1.metric("Rows (hourly bins)", f"{len(resp_subset):,}")
r2.metric("Total calls (sum of total_calls)", f"{int(resp_subset['total_calls'].sum()):,}")
r3.metric("Anomaly hours", f"{int(resp_subset['is_anomaly'].sum()):,}")

if not resp_subset.empty:
    fig_resp = px.scatter(
        resp_subset,
        x="datetime",
        y="avg_service_time",
        color="call_type",
        symbol="is_anomaly",
        symbol_map={0: "circle", 1: "x"},
        labels={
            "avg_service_time": "Average Response Time (sec)",
            "datetime": "Date / Hour",
        },
        hover_data=[
            "call_type",
            "avg_service_time",
            "total_calls",
            "is_anomaly",
            "dispatch_sector",
            "dispatch_neighborhood",
        ],
        title="Hourly 911 Calls — Slow Response Time Anomalies",
    )
    fig_resp.update_traces(marker=dict(size=7, opacity=0.75))
    fig_resp.update_layout(height=520, margin=dict(l=40, r=20, t=70, b=60))
    st.plotly_chart(fig_resp, use_container_width=True)

with st.expander("Show response-time anomaly table"):
    st.dataframe(resp_subset.sort_values("datetime"), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 4: What-If Anomaly Checker (volume + response)
# -------------------------------------------------------------------
st.header("What-If Anomaly Checker")

base_vol = build_volume_baseline(burst_df)
base_resp = build_response_baseline(resp_df)

tab1, tab2 = st.tabs(["Volume anomalies (call counts)", "Response-time anomalies"])

# ---- Volume what-if ----
with tab1:
    if base_vol.empty:
        st.info("Baseline statistics unavailable for volume anomalies.")
    else:
        ctx_call = st.selectbox(
            "Call type (volume)",
            sorted(base_vol["call_type"].dropna().unique().tolist()),
            key="vol_call",
        )
        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        ctx_dow = st.selectbox("Day of week", days_order, index=0, key="vol_dow")
        ctx_hour = st.slider("Hour of day", 0, 23, 12, key="vol_hour")
        observed_calls = st.number_input(
            "Observed calls this hour", min_value=0, value=20, step=1, key="vol_obs"
        )

        row = base_vol[
            (base_vol["call_type"] == ctx_call)
            & (base_vol["DayOfWeek"] == ctx_dow)
            & (base_vol["hour"] == ctx_hour)
        ]

        if row.empty:
            st.warning("No historical baseline for this combination yet.")
        else:
            mu = float(row["mean"].iloc[0])
            sigma = float(row["std"].iloc[0]) if float(row["std"].iloc[0]) > 0 else 1.0
            z = (observed_calls - mu) / sigma

            c1, c2, c3 = st.columns(3)
            c1.metric("Expected calls (μ)", f"{mu:.2f}")
            c2.metric("Std dev (σ)", f"{sigma:.2f}")
            c3.metric("Z-score", f"{z:.2f}")

            if abs(z) >= 3:
                st.error(
                    "This would be flagged as a **strong volume anomaly** (|z| ≥ 3) "
                    "given historical patterns for this context."
                )
            elif abs(z) >= 2:
                st.warning(
                    "This looks **unusual** (|z| between 2 and 3). It may warrant attention."
                )
            else:
                st.success(
                    "Within the **normal range** for this context based on historical volume."
                )

            hist_data = burst_df[
                (burst_df["call_type"] == ctx_call)
                & (burst_df["DayOfWeek"] == ctx_dow)
                & (burst_df["hour"] == ctx_hour)
            ]["total_calls"]

            if not hist_data.empty:
                fig_hist = px.histogram(
                    hist_data,
                    nbins=20,
                    labels={"value": "Historical hourly call counts"},
                    title="Historical distribution of hourly call counts for this context",
                )
                fig_hist.add_vline(
                    x=observed_calls,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Observed",
                    annotation_position="top right",
                )
                st.plotly_chart(fig_hist, use_container_width=True)

# ---- Response-time what-if ----
with tab2:
    if base_resp.empty:
        st.info("Baseline statistics unavailable for response-time anomalies.")
    else:
        ctx_call2 = st.selectbox(
            "Call type (response time)",
            sorted(base_resp["call_type"].dropna().unique().tolist()),
            key="resp_call",
        )
        days_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        ctx_dow2 = st.selectbox(
            "Day of week", days_order, index=0, key="resp_dow"
        )
        ctx_hour2 = st.slider("Hour of day", 0, 23, 12, key="resp_hour")
        observed_rt = st.number_input(
            "Observed average response time this hour (sec)",
            min_value=0.0,
            value=1800.0,
            step=60.0,
            key="resp_obs",
        )

        row2 = base_resp[
            (base_resp["call_type"] == ctx_call2)
            & (base_resp["DayOfWeek"] == ctx_dow2)
            & (base_resp["hour"] == ctx_hour2)
        ]

        if row2.empty or pd.isna(row2["mean"].iloc[0]):
            st.warning("No usable response-time baseline for this combination yet.")
        else:
            mu2 = float(row2["mean"].iloc[0])
            sigma2 = float(row2["std"].iloc[0]) if float(row2["std"].iloc[0]) > 0 else 1.0
            z2 = (observed_rt - mu2) / sigma2

            c1, c2, c3 = st.columns(3)
            c1.metric("Expected avg response (μ, sec)", f"{mu2:.1f}")
            c2.metric("Std dev (σ, sec)", f"{sigma2:.1f}")
            c3.metric("Z-score", f"{z2:.2f}")

            if abs(z2) >= 3:
                st.error(
                    "This would be flagged as a **strong slow/fast response anomaly** (|z| ≥ 3) "
                    "for this context."
                )
            elif abs(z2) >= 2:
                st.warning(
                    "This response time looks **unusual** (|z| between 2 and 3)."
                )
            else:
                st.success(
                    "Within the **normal range** of response time for this context."
                )

            hist_rt = resp_df[
                (resp_df["call_type"] == ctx_call2)
                & (resp_df["DayOfWeek"] == ctx_dow2)
                & (resp_df["hour"] == ctx_hour2)
            ]["avg_service_time"].dropna()

            if not hist_rt.empty:
                fig_hist2 = px.histogram(
                    hist_rt,
                    nbins=20,
                    labels={"value": "Historical avg response time (sec)"},
                    title=(
                        "Historical distribution of hourly avg response time "
                        "for this context"
                    ),
                )
                fig_hist2.add_vline(
                    x=observed_rt,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Observed",
                    annotation_position="top right",
                )
                st.plotly_chart(fig_hist2, use_container_width=True)