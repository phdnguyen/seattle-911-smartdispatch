# streamlit run visualization_1.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------
RESP = "call_sign_total_service_time_s"   
CAD_ID = "cad_event_number"
DATETIME_COL = "cad_event_original_time_queued_datetime"

st.set_page_config(page_title="Seattle 911 Explorer", layout="wide")

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# -------------------------------------------------------------------
# Data loaders
# -------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_main_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # ensure datetime
    df[DATETIME_COL] = pd.to_datetime(df[DATETIME_COL], errors="coerce")
    df = df[df[DATETIME_COL].notna()].copy()

    # mimic Spark filtering for neighborhood / sector
    for c in ["dispatch_neighborhood", "dispatch_sector"]:
        if c in df.columns:
            df[c] = df[c].astype("string")

    if "dispatch_neighborhood" in df.columns and "dispatch_sector" in df.columns:
        mask = (
            df["dispatch_neighborhood"].notna()
            & df["dispatch_sector"].notna()
            & ~df["dispatch_neighborhood"].str.contains("redacted", case=False, na=False)
            & ~df["dispatch_sector"].str.contains("redacted", case=False, na=False)
            & ~df["dispatch_neighborhood"].isin(["-", "Unknown", "UNKNOWN"])
        )
        df = df[mask].copy()

    # keep only valid response-time rows
    if RESP in df.columns:
        df[RESP] = pd.to_numeric(df[RESP], errors="coerce")
        df = df[df[RESP].notna() & (df[RESP] > 0)]

    # time features
    df["queued_ts"] = df[DATETIME_COL]
    df["year"] = df["queued_ts"].dt.year
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
def load_burst_anomaly(path: str) -> pd.DataFrame:
    """
    burst_anomaly_table: volume anomalies (hourly bins).
    Columns expected:
      cad_event_number,is_anomaly,date,hour,call_type_filtered,total_calls,
      mean_calls,std_calls,dispatch_sector,dispatch_neighborhood
    """
    vis = pd.read_csv(path)

    # datetime + time features
    vis["date"] = pd.to_datetime(vis["date"], errors="coerce")
    vis = vis[vis["date"].notna()].copy()
    vis["hour"] = pd.to_numeric(vis["hour"], errors="coerce").fillna(0).astype(int)
    vis["datetime"] = vis["date"] + pd.to_timedelta(vis["hour"], unit="h")
    vis["year"] = vis["date"].dt.year
    vis["month"] = vis["date"].dt.month
    vis["month_name"] = vis["date"].dt.strftime("%b")
    vis["DayOfWeek"] = vis["date"].dt.day_name()

    # clean core fields
    vis["total_calls"] = pd.to_numeric(vis["total_calls"], errors="coerce").fillna(0)
    vis["is_anomaly"] = vis["is_anomaly"].fillna(0).astype(int)

    # normalize names to match main df
    vis = vis.rename(
        columns={
            "call_type_filtered": "call_type",
        }
    )

    return vis


@st.cache_data(show_spinner=False)
def load_response_anomaly(path: str) -> pd.DataFrame:
    """
    response_anomaly_table: response-time anomalies (hourly bins).
    Columns expected:
      cad_event_number,is_anomaly,date,hour,call_type_filtered,total_calls,
      iso_score,dispatch_sector,dispatch_neighborhood,avg_service_time,std_service_time
    """
    vis = pd.read_csv(path)

    vis["date"] = pd.to_datetime(vis["date"], errors="coerce")
    vis = vis[vis["date"].notna()].copy()
    vis["hour"] = pd.to_numeric(vis["hour"], errors="coerce").fillna(0).astype(int)
    vis["datetime"] = vis["date"] + pd.to_timedelta(vis["hour"], unit="h")
    vis["year"] = vis["date"].dt.year
    vis["month"] = vis["date"].dt.month
    vis["month_name"] = vis["date"].dt.strftime("%b")
    vis["DayOfWeek"] = vis["date"].dt.day_name()

    vis["is_anomaly"] = vis["is_anomaly"].fillna(0).astype(int)
    vis["avg_service_time"] = pd.to_numeric(
        vis["avg_service_time"], errors="coerce"
    )
    vis["std_service_time"] = pd.to_numeric(
        vis["std_service_time"], errors="coerce"
    )
    vis = vis[vis["avg_service_time"].notna()]  # avoid NAType issues

    vis = vis.rename(
        columns={
            "call_type_filtered": "call_type",
        }
    )

    return vis


@st.cache_data(show_spinner=False)
def build_volume_baseline(vis: pd.DataFrame) -> pd.DataFrame:
    """
    Baseline stats by (call_type, DayOfWeek, hour, sector, neighborhood)
    for the volume What-If checker.
    """
    df = vis.copy()
    baselines = (
        df.groupby(
            ["call_type", "dispatch_sector", "dispatch_neighborhood", "DayOfWeek", "hour"],
            dropna=False,
        )["total_calls"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    baselines["std"] = baselines["std"].replace(0, 1.0)
    return baselines


@st.cache_data(show_spinner=False)
def build_response_baseline(vis: pd.DataFrame) -> pd.DataFrame:
    """
    Baseline stats by (call_type, sector, neighborhood, DayOfWeek, hour)
    for response-time What-If checker, using avg_service_time.
    """
    df = vis.copy()
    baselines = (
        df.groupby(
            ["call_type", "dispatch_sector", "dispatch_neighborhood", "DayOfWeek", "hour"],
            dropna=False,
        )["avg_service_time"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    baselines["std"] = baselines["std"].replace(0, 1.0)
    return baselines


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def order_for(colname: str):
    if colname == "dow":
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if colname == "month_name":
        return [m for m in MONTH_ORDER]
    if colname == "hour":
        return list(range(24))
    return None


# -------------------------------------------------------------------
# Sidebar: file paths and global filters
# -------------------------------------------------------------------
st.sidebar.title("Load data")
main_path = st.sidebar.text_input(
    "Processed call data CSV path",
    value="data/processed/calldata_20251019_processed_v4.csv",
)
burst_path = st.sidebar.text_input(
    "Burst anomaly CSV path (volume)",
    value="data/output/burst_anomaly_table.csv",
)
resp_path = st.sidebar.text_input(
    "Response-time anomaly CSV path",
    value="data/output/response_anomaly_table.csv",
)

try:
    df = load_main_data(main_path)
    burst_df = load_burst_anomaly(burst_path)
    resp_df = load_response_anomaly(resp_path)
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

st.sidebar.title("Filters")

# global categorical filters
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
neighborhoods_all = (
    ["All"]
    + sorted(df.get("dispatch_neighborhood", pd.Series()).dropna().unique().tolist())
    if "dispatch_neighborhood" in df.columns
    else ["All"]
)

sel_call = st.sidebar.selectbox("Call Type", call_types, index=0)
sel_prio = st.sidebar.selectbox("Priority", priorities, index=0)
sel_sect = st.sidebar.selectbox("Dispatch Sector", sectors, index=0)

# neighborhood choices depend on sector (if one is selected)
if sel_sect != "All":
    neigh_opts = (
        ["All"]
        + sorted(
            df[df["dispatch_sector"] == sel_sect]["dispatch_neighborhood"]
            .dropna()
            .unique()
            .tolist()
        )
    )
else:
    neigh_opts = neighborhoods_all

sel_neigh = st.sidebar.selectbox("Dispatch Neighborhood", neigh_opts, index=0)

# year & month filters
years = ["All"] + sorted(df["year"].dropna().unique().tolist())
months_available = [m for m in MONTH_ORDER if m in df["month_name"].unique()]
months = ["All"] + months_available

sel_year = st.sidebar.selectbox("Year", years, index=0)
sel_month = st.sidebar.selectbox("Month", months, index=0)

# Metric for Response Time Explorer
metric = st.sidebar.radio(
    "Metric for Response Time Explorer",
    ["avg", "median", "min", "max"],
    horizontal=True,
)
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
x_axis_label = st.sidebar.selectbox("X-Axis", list(axis_options.keys()), index=1)
y_axis_label = st.sidebar.selectbox("Y-Axis", list(axis_options.keys()), index=2)

if x_axis_label == y_axis_label:
    st.sidebar.warning("Pick two different axes; they must not be the same.")
    st.stop()

x_col = axis_options[x_axis_label]
y_col = axis_options[y_axis_label]
order_x = order_for(x_col)
order_y = order_for(y_col)

# -------------------------------------------------------------------
# Apply global filters to main dataframe
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
if sel_year != "All":
    df_f = df_f[df_f["year"] == sel_year]
if sel_month != "All":
    df_f = df_f[df_f["month_name"] == sel_month]

if df_f.empty:
    st.warning("No rows after filters.")
    st.stop()

# Subsets of anomaly tables with the same global filters
def filter_anomaly_df(vis):
    out = vis.copy()
    if sel_call != "All":
        out = out[out["call_type"] == sel_call]
    if sel_sect != "All":
        out = out[out["dispatch_sector"] == sel_sect]
    if sel_neigh != "All":
        out = out[out["dispatch_neighborhood"] == sel_neigh]
    if sel_year != "All":
        out = out[out["year"] == sel_year]
    if sel_month != "All":
        out = out[out["month_name"] == sel_month]
    return out


burst_sub = filter_anomaly_df(burst_df)
resp_sub = filter_anomaly_df(resp_df)

# -------------------------------------------------------------------
# SECTION 1: Seattle 911 – Response Time Explorer
# -------------------------------------------------------------------
st.title("Seattle 911 – Response Time Explorer")
st.caption(
    "Interactive analysis of SPD response time by incident context and time patterns (in minutes)."
)

mins = df_f["response_time_min"]
p95 = mins.quantile(0.95)

# KPIs
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Rows (after filters)", f"{len(df_f):,}")
c2.metric("Avg (min)", f"{mins.mean():.2f}")
c3.metric("Median (min)", f"{mins.median():.2f}")
c4.metric("95th percentile (min)", f"{p95:.2f}")
c5.metric("Min (min)", f"{mins.min():.2f}")
c6.metric("Max (min)", f"{mins.max():.2f}")

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
    f"{metric_label} • CallType: {sel_call} • Priority: {sel_prio} • "
    f"Sector: {sel_sect} • Neighborhood: {sel_neigh} • Year: {sel_year} • Month: {sel_month}"
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
    f"Sector: {sel_sect} • Neighborhood: {sel_neigh} • Year: {sel_year} • Month: {sel_month}"
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

if not burst_sub.empty:
    t1, t2, t3 = st.columns(3)
    t1.metric("Rows (hourly bins)", f"{len(burst_sub):,}")
    t2.metric("Total calls (sum of total_calls)", f"{int(burst_sub['total_calls'].sum()):,}")
    t3.metric("Anomaly hours", f"{int(burst_sub['is_anomaly'].sum()):,}")

    fig_vol = px.scatter(
        burst_sub,
        x="date",
        y="total_calls",
        color="call_type",
        symbol="is_anomaly",
        symbol_map={0: "circle", 1: "x"},
        labels={"total_calls": "Number of calls per hour", "date": "Date"},
        hover_data=["call_type", "total_calls", "is_anomaly", "dispatch_sector", "dispatch_neighborhood"],
        title="Hourly 911 Calls — Volume Anomalies Highlighted",
    )
    fig_vol.update_traces(marker=dict(size=7, opacity=0.7))
    fig_vol.update_layout(height=520, margin=dict(l=40, r=20, t=70, b=60))
    st.plotly_chart(fig_vol, use_container_width=True)

with st.expander("Show volume anomaly table"):
    st.dataframe(burst_sub.sort_values("date"), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 3B: Incident Flow Timeline — Response-Time Anomalies
# -------------------------------------------------------------------
st.header("Incident Flow Timeline — Slow Response Time Anomalies")

if not resp_sub.empty:
    r1, r2, r3 = st.columns(3)
    r1.metric("Rows (hourly bins)", f"{len(resp_sub):,}")
    r2.metric("Total calls (sum of total_calls)", f"{int(resp_sub['total_calls'].sum()):,}")
    r3.metric("Anomaly hours", f"{int(resp_sub['is_anomaly'].sum()):,}")

    fig_resp = px.scatter(
        resp_sub,
        x="date",
        y="avg_service_time",
        color="call_type",
        symbol="is_anomaly",
        symbol_map={0: "circle", 1: "x"},
        labels={"avg_service_time": "Average response time (sec)", "date": "Date"},
        hover_data=[
            "call_type",
            "avg_service_time",
            "std_service_time",
            "total_calls",
            "dispatch_sector",
            "dispatch_neighborhood",
            "is_anomaly",
        ],
        title="Hourly 911 Calls — Slow Response Time Anomalies Highlighted",
    )
    fig_resp.update_traces(marker=dict(size=7, opacity=0.7))
    fig_resp.update_layout(height=520, margin=dict(l=40, r=20, t=70, b=60))
    st.plotly_chart(fig_resp, use_container_width=True)

with st.expander("Show response-time anomaly table"):
    st.dataframe(resp_sub.sort_values("date"), use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 4A: What-If Anomaly Checker — Volume
# -------------------------------------------------------------------
st.header("What-If Anomaly Checker — Volume")

volume_baseline = build_volume_baseline(burst_df)

if volume_baseline.empty:
    st.info("Baseline statistics unavailable – cannot run volume What-If checker.")
else:
    # default to global selections when possible
    ctx_call_list = sorted(volume_baseline["call_type"].dropna().unique().tolist())
    ctx_call_default = ctx_call_list.index(sel_call) if sel_call in ctx_call_list else 0
    ctx_call = st.selectbox("Call type (volume)", ctx_call_list, index=ctx_call_default)

    ctx_sector_list = sorted(
        volume_baseline["dispatch_sector"].dropna().unique().tolist()
    )
    ctx_sector_default = (
        ctx_sector_list.index(sel_sect) if sel_sect in ctx_sector_list else 0
    )
    ctx_sector = st.selectbox(
        "Dispatch sector (volume)", ctx_sector_list, index=ctx_sector_default
    )

    neigh_choices = sorted(
        volume_baseline[
            volume_baseline["dispatch_sector"] == ctx_sector
        ]["dispatch_neighborhood"]
        .dropna()
        .unique()
        .tolist()
    )
    ctx_neigh_default = (
        neigh_choices.index(sel_neigh) if sel_neigh in neigh_choices else 0
    ) if neigh_choices else 0
    ctx_neigh = st.selectbox(
        "Dispatch neighborhood (volume)", neigh_choices or ["(none)"], index=ctx_neigh_default
    )

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"]
    ctx_dow = st.selectbox("Day of week (volume)", days_order, index=0)
    ctx_hour = st.slider("Hour of day (volume)", 0, 23, 12)
    observed_calls = st.number_input(
        "Observed calls this hour", min_value=0, value=20, step=1
    )

    row = volume_baseline[
        (volume_baseline["call_type"] == ctx_call)
        & (volume_baseline["dispatch_sector"] == ctx_sector)
        & (volume_baseline["dispatch_neighborhood"] == ctx_neigh)
        & (volume_baseline["DayOfWeek"] == ctx_dow)
        & (volume_baseline["hour"] == ctx_hour)
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
            st.error("This would be a **strong volume anomaly** (|z| ≥ 3).")
        elif abs(z) >= 2:
            st.warning("This looks **unusual** (|z| between 2 and 3).")
        else:
            st.success("Within the **normal range** for hourly call volume.")

        hist_data = burst_df[
            (burst_df["call_type"] == ctx_call)
            & (burst_df["dispatch_sector"] == ctx_sector)
            & (burst_df["dispatch_neighborhood"] == ctx_neigh)
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

st.markdown("---")

# -------------------------------------------------------------------
# SECTION 4B: What-If Anomaly Checker — Response Time
# -------------------------------------------------------------------
st.header("What-If Anomaly Checker — Response Time")

response_baseline = build_response_baseline(resp_df)

if response_baseline.empty:
    st.info("Baseline statistics unavailable – cannot run response-time checker.")
else:
    ctx_call_list = sorted(response_baseline["call_type"].dropna().unique().tolist())
    ctx_call_default = ctx_call_list.index(sel_call) if sel_call in ctx_call_list else 0
    ctx_call_r = st.selectbox(
        "Call type (response time)", ctx_call_list, index=ctx_call_default
    )

    ctx_sector_list = sorted(
        response_baseline["dispatch_sector"].dropna().unique().tolist()
    )
    ctx_sector_default = (
        ctx_sector_list.index(sel_sect) if sel_sect in ctx_sector_list else 0
    )
    ctx_sector_r = st.selectbox(
        "Dispatch sector (response time)", ctx_sector_list, index=ctx_sector_default
    )

    neigh_choices_r = sorted(
        response_baseline[
            response_baseline["dispatch_sector"] == ctx_sector_r
        ]["dispatch_neighborhood"]
        .dropna()
        .unique()
        .tolist()
    )
    ctx_neigh_default_r = (
        neigh_choices_r.index(sel_neigh) if sel_neigh in neigh_choices_r else 0
    ) if neigh_choices_r else 0
    ctx_neigh_r = st.selectbox(
        "Dispatch neighborhood (response time)",
        neigh_choices_r or ["(none)"],
        index=ctx_neigh_default_r,
    )

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"]
    ctx_dow_r = st.selectbox("Day of week (response time)", days_order, index=0)
    ctx_hour_r = st.slider("Hour of day (response time)", 0, 23, 12)
    observed_rt = st.number_input(
        "Observed average response time this hour (sec)",
        min_value=0.0,
        value=300.0,
        step=10.0,
    )

    row_r = response_baseline[
        (response_baseline["call_type"] == ctx_call_r)
        & (response_baseline["dispatch_sector"] == ctx_sector_r)
        & (response_baseline["dispatch_neighborhood"] == ctx_neigh_r)
        & (response_baseline["DayOfWeek"] == ctx_dow_r)
        & (response_baseline["hour"] == ctx_hour_r)
    ]

    if row_r.empty:
        st.warning("No historical baseline for this response-time context yet.")
    else:
        mu_r = float(row_r["mean"].iloc[0])
        sigma_r = float(row_r["std"].iloc[0]) if float(row_r["std"].iloc[0]) > 0 else 1.0
        z_r = (observed_rt - mu_r) / sigma_r

        c1, c2, c3 = st.columns(3)
        c1.metric("Expected avg response (μ, sec)", f"{mu_r:.1f}")
        c2.metric("Std dev (σ, sec)", f"{sigma_r:.1f}")
        c3.metric("Z-score", f"{z_r:.2f}")

        if z_r >= 3:
            st.error("This would be a **strong slow-response anomaly** (z ≥ 3).")
        elif z_r >= 2:
            st.warning("This looks **unusually slow** (z between 2 and 3).")
        elif z_r <= -2:
            st.success("This is **unusually fast** compared to history (z ≤ -2).")
        else:
            st.success("Within the **normal range** for response time in this context.")

        hist_rt = resp_df[
            (resp_df["call_type"] == ctx_call_r)
            & (resp_df["dispatch_sector"] == ctx_sector_r)
            & (resp_df["dispatch_neighborhood"] == ctx_neigh_r)
            & (resp_df["DayOfWeek"] == ctx_dow_r)
            & (resp_df["hour"] == ctx_hour_r)
        ]["avg_service_time"]

        if not hist_rt.empty:
            fig_hist_rt = px.histogram(
                hist_rt,
                nbins=20,
                labels={"value": "Historical avg hourly response time (sec)"},
                title="Historical distribution of hourly response time for this context",
            )
            fig_hist_rt.add_vline(
                x=observed_rt,
                line_dash="dash",
                line_color="red",
                annotation_text="Observed",
                annotation_position="top right",
            )
            st.plotly_chart(fig_hist_rt, use_container_width=True)