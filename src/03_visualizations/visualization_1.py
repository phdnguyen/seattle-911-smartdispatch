# streamlit run visualization_1.py
import os
import streamlit as st
import pandas as pd
import plotly.express as px

RESP = "call_sign_total_service_time_s"  # seconds
CAD_ID = "cad_event_number"
DATETIME_COL = "cad_event_original_time_queued_datetime"

st.set_page_config(page_title="Seattle 911 Explorer", layout="wide")

MONTH_MAP = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct"
}
INV_MONTH_MAP = {v: k for k, v in MONTH_MAP.items()}


def order_for(colname: str):
    if colname == "dow":
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    if colname == "month_name":
        return [MONTH_MAP[m] for m in range(1, 13)]
    if colname == "hour":
        return list(range(24))
    return None


def apply_global_filters_to_anom(
    df_anom: pd.DataFrame,
    sel_call: str,
    sel_sect: str,
    sel_neigh: str,
    sel_year: int | None,
    sel_month: int | None,
) -> pd.DataFrame:
    d = df_anom.copy()
    if "call_type" in d.columns and sel_call != "All":
        d = d[d["call_type"] == sel_call]
    if "dispatch_sector" in d.columns and sel_sect != "All":
        d = d[d["dispatch_sector"] == sel_sect]
    if "dispatch_neighborhood" in d.columns and sel_neigh != "All":
        d = d[d["dispatch_neighborhood"] == sel_neigh]
    if "Year" in d.columns and sel_year is not None:
        d = d[d["Year"] == sel_year]
    if "Month" in d.columns and sel_month is not None:
        d = d[d["Month"] == sel_month]
    return d


@st.cache_data(show_spinner=False)
def load_main_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    if RESP in df.columns:
        df = df[df[RESP].notna() & (df[RESP] > 0)]

    for c in ["dispatch_neighborhood", "dispatch_sector"]:
        if c in df.columns:
            df = df[df[c].notna()]
            df = df[~df[c].astype(str).str.contains("redacted", case=False, na=False)]
    if "dispatch_neighborhood" in df.columns:
        df = df[~df["dispatch_neighborhood"].isin(["-", "Unknown", "UNKNOWN"])]

    ts = pd.to_datetime(df[DATETIME_COL], errors="coerce")
    df = df[ts.notna()].copy()
    df["queued_ts"] = ts

    df["Year"] = df["queued_ts"].dt.year
    df = df[df["Year"] == 2025]
    df["Month"] = df["queued_ts"].dt.month
    df["month_name"] = df["Month"].map(MONTH_MAP)
    df["dow_num"] = df["queued_ts"].dt.dayofweek + 1
    df["dow"] = pd.Categorical(
        df["queued_ts"].dt.strftime("%a"),
        categories=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        ordered=True,
    )
    df["hour"] = df["queued_ts"].dt.hour

    if RESP in df.columns:
        df["response_time_min"] = df[RESP].astype(float) / 60.0

    return df


@st.cache_data(show_spinner=False)
def load_volume_anomaly_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = df["hour"].astype(int)
    df = df[df["date"].notna()].copy()
    df["datetime"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

    if "call_type_filtered" in df.columns:
        df = df.rename(columns={"call_type_filtered": "call_type"})

    df["Year"] = df["datetime"].dt.year
    df = df[df["Year"] == 2025]
    df["Month"] = df["datetime"].dt.month
    df["DayOfWeek"] = df["datetime"].dt.day_name()

    for c in ["dispatch_neighborhood", "dispatch_sector"]:
        if c in df.columns:
            df[c] = df[c].fillna("Unknown")

    df["is_anomaly"] = df.get("is_anomaly", 0).fillna(0).astype(int)
    df["total_calls"] = df["total_calls"].fillna(0).astype(float)

    return df


@st.cache_data(show_spinner=False)
def load_response_anomaly_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = df["hour"].astype(int)
    df = df[df["date"].notna()].copy()
    df["datetime"] = df["date"] + pd.to_timedelta(df["hour"], unit="h")

    if "call_type_filtered" in df.columns:
        df = df.rename(columns={"call_type_filtered": "call_type"})

    df["Year"] = df["datetime"].dt.year
    df = df[df["Year"] == 2025]
    df["Month"] = df["datetime"].dt.month
    df["DayOfWeek"] = df["datetime"].dt.day_name()

    for c in ["dispatch_neighborhood", "dispatch_sector"]:
        if c in df.columns:
            df[c] = df[c].fillna("Unknown")

    df["is_anomaly"] = df.get("is_anomaly", 0).fillna(0).astype(int)
    df["avg_service_time"] = df["avg_service_time"].astype(float) / 60.0
    df["std_service_time"] = df["std_service_time"].astype(float) / 60.0

    return df


@st.cache_data(show_spinner=False)
def build_volume_baseline(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    base = (
        df.groupby(
            [
                "call_type",
                "Year",
                "Month",
                "dispatch_sector",
                "dispatch_neighborhood",
                "DayOfWeek",
                "hour",
            ],
            dropna=False,
            observed=False,
        )["total_calls"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    base["std"] = base["std"].replace(0, 1.0)
    return base


@st.cache_data(show_spinner=False)
def build_response_baseline(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    base = (
        df.groupby(
            [
                "call_type",
                "Year",
                "Month",
                "dispatch_sector",
                "dispatch_neighborhood",
                "DayOfWeek",
                "hour",
            ],
            dropna=False,
            observed=False,
        )["avg_service_time"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    base["std"] = base["std"].replace(0, 1.0)
    return base


st.sidebar.title("Load data")
main_path = st.sidebar.text_input(
    "Processed CSV path (main call data)",
    value="data/processed/calldata_20251019_processed_v4_small.parquet",
)
vol_path = st.sidebar.text_input(
    "Hourly volume anomaly CSV (burst_anomaly_table)",
    value="data/output/burst_anomaly_table.parquet",
)
resp_path = st.sidebar.text_input(
    "Hourly response-time anomaly CSV (response_anomaly_table)",
    value="data/output/response_anomaly_table.parquet",
)

try:
    df = load_main_data(main_path)
    vol_df = load_volume_anomaly_data(vol_path)
    resp_df = load_response_anomaly_data(resp_path)
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

st.sidebar.title("Filters")

call_types = ["All"]
if "call_type" in df.columns:
    call_types += sorted(df["call_type"].dropna().unique().tolist())
priorities = ["All"]
if "priority" in df.columns:
    priorities += sorted(df["priority"].dropna().unique().tolist(), key=lambda x: str(x))

sectors = ["All"]
if "dispatch_sector" in df.columns:
    sectors += sorted(df["dispatch_sector"].dropna().unique().tolist())

sel_call = st.sidebar.selectbox("Call Type", call_types, index=0)
sel_prio = st.sidebar.selectbox("Priority", priorities, index=0)
sel_sect = st.sidebar.selectbox("Dispatch Sector", sectors, index=0)

if "dispatch_neighborhood" in df.columns:
    if sel_sect != "All":
        neigh_options = (
            df.loc[df["dispatch_sector"] == sel_sect, "dispatch_neighborhood"]
            .dropna()
            .unique()
            .tolist()
        )
    else:
        neigh_options = df["dispatch_neighborhood"].dropna().unique().tolist()
    neighborhoods = ["All"] + sorted(neigh_options)
else:
    neighborhoods = ["All"]

sel_neigh = st.sidebar.selectbox("Dispatch Neighborhood", neighborhoods, index=0)

years = ["All"]
if "Year" in df.columns:
    years += sorted(df["Year"].dropna().astype(int).unique().tolist())
sel_year_label = st.sidebar.selectbox("Year", years, index=0)
sel_year = None if sel_year_label == "All" else int(sel_year_label)

months = ["All"] + [MONTH_MAP[m] for m in range(1, 11)]
sel_month_label = st.sidebar.selectbox("Month", months, index=0)
sel_month = None if sel_month_label == "All" else INV_MONTH_MAP[sel_month_label]

metric = st.sidebar.radio(
    "Metric to show in Response Time Explorer",
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

st.sidebar.title("Heatmap Time Axes")
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

df_f = df.copy()
if sel_call != "All" and "call_type" in df_f.columns:
    df_f = df_f[df_f["call_type"] == sel_call]
if sel_prio != "All" and "priority" in df_f.columns:
    df_f = df_f[df_f["priority"] == sel_prio]
if sel_sect != "All" and "dispatch_sector" in df_f.columns:
    df_f = df_f[df_f["dispatch_sector"] == sel_sect]
if sel_neigh != "All" and "dispatch_neighborhood" in df_f.columns:
    df_f = df_f[df_f["dispatch_neighborhood"] == sel_neigh]
if sel_year is not None and "Year" in df_f.columns:
    df_f = df_f[df_f["Year"] == sel_year]
if sel_month is not None and "Month" in df_f.columns:
    df_f = df_f[df_f["Month"] == sel_month]

if df_f.empty:
    st.warning("No rows after filters.")
    st.stop()

vol_filtered = apply_global_filters_to_anom(
    vol_df, sel_call, sel_sect, sel_neigh, sel_year, sel_month
)
resp_filtered = apply_global_filters_to_anom(
    resp_df, sel_call, sel_sect, sel_neigh, sel_year, sel_month
)

st.title("Seattle 911 Dashboard Demo (2025 Data Only)")
st.caption(
    "Source: Seattle Open Data Portal — https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy/about_data"
)

st.header("Response Time Explorer")
st.caption("Interactive analysis of SPD response time by incident context and time patterns (in minutes).")

mins = df_f["response_time_min"].dropna()
p95 = mins.quantile(0.95)
rows_ct = len(df_f)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Rows (after filters)", f"{rows_ct:,}")
c2.metric("Avg (min)", f"{mins.mean():.2f}")
c3.metric("Median (min)", f"{mins.median():.2f}")
c4.metric("95th percentile (min)", f"{p95:.2f}")
c5.metric("Min (min)", f"{mins.min():.2f}")
c6.metric("Max (min)", f"{mins.max():.2f}")

agg_df = (
    df_f.groupby([y_col, x_col], dropna=False, observed=False)["response_time_min"]
    .agg([agg_fn, "count"])
    .reset_index()
    .rename(columns={agg_fn: "value", "count": "n"})
)

if order_x is not None:
    agg_df[x_col] = pd.Categorical(agg_df[x_col], categories=order_x, ordered=True)
if order_y is not None:
    agg_df[y_col] = pd.Categorical(agg_df[y_col], categories=order_y, ordered=True)

pivot = (
    agg_df.pivot_table(
        index=y_col,
        columns=x_col,
        values="value",
        aggfunc="mean",
        observed=False,
    )
    .sort_index()
    .sort_index(axis=1)
)

title_rt = (
    f"{metric_label} Response Time (min) • "
    f"CallType: {sel_call} • Priority: {sel_prio} • "
    f"Sector: {sel_sect} • Neighborhood: {sel_neigh} • "
    f"Year: {sel_year_label} • Month: {sel_month_label}"
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
st.plotly_chart(fig_rt, width="stretch")

cell_stats = (
    df_f.groupby([y_col, x_col], observed=False)["response_time_min"]
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
    # st.caption(f"**Worst median-response cell:** {worst_label}")

# with st.expander("Show aggregated table (response time)"):
#     st.dataframe(agg_df.sort_values("value", ascending=False), width="stretch")

st.markdown("---")

st.header("Call Volume Explorer")
st.caption(
    "Unique CAD events per time cell. KPIs use aggregate statistics across cells; the heatmap shows per-cell frequency (counts)."
)

freq_df = (
    df_f.groupby([y_col, x_col], dropna=False, observed=False)[CAD_ID]
    .nunique()
    .reset_index()
    .rename(columns={CAD_ID: "freq"})
)

if order_x is not None:
    freq_df[x_col] = pd.Categorical(freq_df[x_col], categories=order_x, ordered=True)
if order_y is not None:
    freq_df[y_col] = pd.Categorical(freq_df[y_col], categories=order_y, ordered=True)

freq_vals = freq_df["freq"]

fc1, fc2, fc3, fc4, fc5, fc6 = st.columns(6)
fc1.metric(
    "Total calls (unique CAD)",
    f"{df_f[CAD_ID].nunique():,}" if CAD_ID in df_f.columns else "—",
)
fc2.metric("Avg calls / cell", f"{freq_vals.mean():.2f}" if not freq_df.empty else "—")
fc3.metric("Median calls / cell", f"{freq_vals.median():.2f}" if not freq_df.empty else "—")
fc4.metric("95th percentile calls / cell", f"{freq_vals.quantile(0.95):.2f}")
fc5.metric("Min calls / cell", f"{freq_vals.min():.0f}" if not freq_df.empty else "—")
fc6.metric("Max calls / cell", f"{freq_vals.max():.0f}" if not freq_df.empty else "—")

pivot_freq = (
    freq_df.pivot_table(
        index=y_col,
        columns=x_col,
        values="freq",
        aggfunc="sum",
        observed=False,
    )
    .sort_index()
    .sort_index(axis=1)
)

title_freq = (
    f"Call Frequency (unique CAD per cell) • "
    f"CallType: {sel_call} • Priority: {sel_prio} • "
    f"Sector: {sel_sect} • Neighborhood: {sel_neigh} • "
    f"Year: {sel_year_label} • Month: {sel_month_label}"
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
st.plotly_chart(fig_freq, width="stretch")

# with st.expander("Show aggregated table (frequency)"):
#     st.dataframe(freq_df.sort_values("freq", ascending=False), width="stretch")

st.markdown("---")

st.header("Incident Flow Timeline — Hourly 911 Call Volume Anomalies")

if vol_filtered.empty:
    st.info("No volume anomaly rows for the selected filters.")
else:
    vol_rows = len(vol_filtered)
    vol_total_calls = int(vol_filtered["total_calls"].sum())
    vol_anom_hours = int(vol_filtered["is_anomaly"].sum())

    t1, t2, t3 = st.columns(3)
    t1.metric("Rows (hourly bins)", f"{vol_rows:,}")
    t2.metric("Total calls (sum of total_calls)", f"{vol_total_calls:,}")
    t3.metric("Anomaly hours", f"{vol_anom_hours:,}")

    fig_vol = px.scatter(
        vol_filtered,
        x="datetime",
        y="total_calls",
        color="call_type",
        symbol="is_anomaly",
        symbol_map={0: "circle", 1: "x"},
        labels={"total_calls": "Number of calls per hour", "datetime": "Date / Hour"},
        hover_data=["call_type", "total_calls", "is_anomaly"],
        title="Hourly 911 Calls — Volume Anomalies Highlighted",
    )
    fig_vol.update_traces(marker=dict(size=6, opacity=0.7))
    fig_vol.update_layout(height=520, margin=dict(l=40, r=20, t=70, b=60))
    st.plotly_chart(fig_vol, width="stretch")

    # with st.expander("Show volume anomaly table"):
    #     st.dataframe(vol_filtered.sort_values("datetime"), width="stretch")

st.markdown("---")

st.header("Incident Flow Timeline — Slow Response Time Anomalies")

if resp_filtered.empty:
    st.info("No response-time anomaly rows for the selected filters.")
else:
    rt_rows = len(resp_filtered)
    rt_anom_hours = int(resp_filtered["is_anomaly"].sum())
    rt_avg = resp_filtered["avg_service_time"].mean()
    rt_p95 = resp_filtered["avg_service_time"].quantile(0.95)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Rows (hourly bins)", f"{rt_rows:,}")
    r2.metric("Anomaly hours", f"{rt_anom_hours:,}")
    r3.metric("Avg response time (min)", f"{rt_avg:.2f}")
    r4.metric("95th percentile (min)", f"{rt_p95:.2f}")

    fig_rt_anom = px.scatter(
        resp_filtered,
        x="datetime",
        y="avg_service_time",
        color="call_type",
        symbol="is_anomaly",
        symbol_map={0: "circle", 1: "x"},
        labels={
            "avg_service_time": "Average response time (min)",
            "datetime": "Date / Hour",
        },
        hover_data=["call_type", "avg_service_time", "total_calls", "is_anomaly"],
        title="Incident Flow Timeline — Slow Response Time Anomalies",
    )
    fig_rt_anom.update_traces(marker=dict(size=6, opacity=0.7))
    fig_rt_anom.update_layout(height=520, margin=dict(l=40, r=20, t=70, b=60))
    st.plotly_chart(fig_rt_anom, width="stretch")

    # with st.expander("Show response-time anomaly table"):
    #     st.dataframe(resp_filtered.sort_values("datetime"), width="stretch")

st.markdown("---")

st.header("What-If Anomaly Checker — Volume")

vol_baseline = build_volume_baseline(vol_df)

if vol_baseline.empty:
    st.info("Baseline statistics for volume are unavailable.")
else:
    st.markdown(
        f"Context from filters — **Call type:** `{sel_call}` • "
        f"**Sector:** `{sel_sect}` • **Neighborhood:** `{sel_neigh}` • "
        f"**Year:** `{sel_year_label}` • **Month:** `{sel_month_label}`"
    )

    days_order = [
        "All",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    ctx_dow = st.selectbox("Day of week (volume)", days_order, index=0)
    ctx_hour = st.slider("Hour of day (volume)", 0, 23, 12)
    observed_calls = st.number_input(
        "Observed calls this hour", min_value=0, value=20, step=1
    )

    rows = vol_baseline.copy()
    if sel_call != "All":
        rows = rows[rows["call_type"] == sel_call]
    if sel_sect != "All":
        rows = rows[rows["dispatch_sector"] == sel_sect]
    if sel_neigh != "All":
        rows = rows[rows["dispatch_neighborhood"] == sel_neigh]
    if sel_year is not None:
        rows = rows[rows["Year"] == sel_year]
    if sel_month is not None:
        rows = rows[rows["Month"] == sel_month]
    if ctx_dow != "All":
        rows = rows[rows["DayOfWeek"] == ctx_dow]
    rows = rows[rows["hour"] == ctx_hour]

    if rows.empty:
        st.warning("No historical baseline for this context yet.")
    else:
        mu = float(rows["mean"].mean())
        sigma = float(rows["std"].mean())
        if sigma <= 0:
            sigma = 1.0
        z = (observed_calls - mu) / sigma

        c1, c2, c3 = st.columns(3)
        c1.metric("Expected calls (μ)", f"{mu:.2f}")
        c2.metric("Std dev (σ)", f"{sigma:.2f}")
        c3.metric("Z-score", f"{z:.2f}")

        if abs(z) >= 3:
            st.error(
                "This would be flagged as a **strong anomaly** (|z| ≥ 3) "
                "given historical call volume for this context."
            )
        elif abs(z) >= 2:
            st.warning(
                "This looks **unusual** (|z| between 2 and 3). It may warrant attention."
            )
        else:
            st.success("Within the **normal range** for call volume in this context.")

        hist_data = apply_global_filters_to_anom(
            vol_df, sel_call, sel_sect, sel_neigh, sel_year, sel_month
        )
        if ctx_dow != "All":
            hist_data = hist_data[hist_data["DayOfWeek"] == ctx_dow]
        hist_data = hist_data[hist_data["hour"] == ctx_hour]["total_calls"].dropna()

        if not hist_data.empty:
            fig_hist_vol = px.histogram(
                hist_data,
                nbins=20,
                labels={"value": "Historical hourly call counts"},
                title="Historical distribution of hourly call counts for this context",
            )
            fig_hist_vol.add_vline(
                x=observed_calls,
                line_dash="dash",
                line_color="red",
                annotation_text="Observed",
                annotation_position="top right",
            )
            st.plotly_chart(fig_hist_vol, width="stretch")

st.markdown("---")

st.header("What-If Anomaly Checker — Response Time")

resp_baseline = build_response_baseline(resp_df)

if resp_baseline.empty:
    st.info("Baseline statistics for response time are unavailable.")
else:
    st.markdown(
        f"Context from filters — **Call type:** `{sel_call}` • "
        f"**Sector:** `{sel_sect}` • **Neighborhood:** `{sel_neigh}` • "
        f"**Year:** `{sel_year_label}` • **Month:** `{sel_month_label}`"
    )

    days_order_rt = [
        "All",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    ctx_dow_rt = st.selectbox("Day of week (response time)", days_order_rt, index=0)
    ctx_hour_rt = st.slider("Hour of day (response time)", 0, 23, 12)
    observed_rt = st.number_input(
        "Observed average response time this hour (minutes)",
        min_value=0.0,
        value=10.0,
        step=0.5,
    )

    rows_rt = resp_baseline.copy()
    if sel_call != "All":
        rows_rt = rows_rt[rows_rt["call_type"] == sel_call]
    if sel_sect != "All":
        rows_rt = rows_rt[rows_rt["dispatch_sector"] == sel_sect]
    if sel_neigh != "All":
        rows_rt = rows_rt[rows_rt["dispatch_neighborhood"] == sel_neigh]
    if sel_year is not None:
        rows_rt = rows_rt[rows_rt["Year"] == sel_year]
    if sel_month is not None:
        rows_rt = rows_rt[rows_rt["Month"] == sel_month]
    if ctx_dow_rt != "All":
        rows_rt = rows_rt[rows_rt["DayOfWeek"] == ctx_dow_rt]
    rows_rt = rows_rt[rows_rt["hour"] == ctx_hour_rt]

    if rows_rt.empty:
        st.warning("No historical baseline for this response-time context yet.")
    else:
        mu_rt = float(rows_rt["mean"].mean())
        sigma_rt = float(rows_rt["std"].mean())
        if sigma_rt <= 0:
            sigma_rt = 1.0
        z_rt = (observed_rt - mu_rt) / sigma_rt

        c1, c2, c3 = st.columns(3)
        c1.metric("Expected avg response (μ, min)", f"{mu_rt:.2f}")
        c2.metric("Std dev (σ, min)", f"{sigma_rt:.2f}")
        c3.metric("Z-score", f"{z_rt:.2f}")

        if z_rt >= 3:
            st.error(
                "This would be flagged as a **slow-response anomaly** (z ≥ 3) "
                "given historical patterns for this context."
            )
        elif z_rt >= 2:
            st.warning("This response looks **slower than usual** (z between 2 and 3).")
        elif z_rt <= -2:
            st.success(
                "This response is **faster than historical average** (z ≤ -2) "
                "for this context."
            )
        else:
            st.success("Within the **normal response-time range** for this context.")

        hist_rt = apply_global_filters_to_anom(
            resp_df, sel_call, sel_sect, sel_neigh, sel_year, sel_month
        )
        if ctx_dow_rt != "All":
            hist_rt = hist_rt[hist_rt["DayOfWeek"] == ctx_dow_rt]
        hist_rt = hist_rt[hist_rt["hour"] == ctx_hour_rt]["avg_service_time"].dropna()

        if not hist_rt.empty:
            fig_hist_rt = px.histogram(
                hist_rt,
                nbins=20,
                labels={"value": "Historical avg response time (min)"},
                title="Historical distribution of avg response time for this context",
            )
            fig_hist_rt.add_vline(
                x=observed_rt,
                line_dash="dash",
                line_color="red",
                annotation_text="Observed",
                annotation_position="top right",
            )
            st.plotly_chart(fig_hist_rt, width="stretch")