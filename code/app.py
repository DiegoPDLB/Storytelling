import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & LIGHT EXECUTIVE CSS STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Mexico Automotive Market Strategy (2016-2026)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Force clean Light Theme across main app & header */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F4F6F9 !important;
        color: #0F172A !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1360px;
    }

    /* Base light-mode text */
    .stApp p, .stApp span, .stApp label, .stApp li {
        color: #1E293B;
    }
    .stApp h2, .stApp h3, .stApp h4 {
        color: #0F2537 !important;
    }

    /* DARK EXECUTIVE SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #0F2537 !important;
        border-right: 1px solid #1E3A5F;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #F8FAFC !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-size: 1.05rem;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        border-bottom: 2px solid #C0392B;
        padding-bottom: 0.5rem;
        margin-bottom: 0.8rem;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #16324A !important;
        border: 1px solid #2C5282 !important;
        border-radius: 6px;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #C0392B !important;
        color: #FFFFFF !important;
        border-radius: 4px;
    }
    .sidebar-card {
        background-color: #16324A;
        border-left: 3px solid #C0392B;
        padding: 0.9rem 1rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.82rem;
        line-height: 1.5;
        margin-top: 1.2rem;
        color: #E2E8F0 !important;
    }

    /* EXECUTIVE HEADER BANNER (HIGH SPECIFICITY FOR WHITE TEXT) */
    .exec-banner {
        background: linear-gradient(135deg, #0F2537 0%, #1B3B5A 100%) !important;
        padding: 1.8rem 2.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 6px solid #C0392B;
        box-shadow: 0 4px 12px rgba(15, 37, 55, 0.10);
    }
    .exec-banner .banner-title {
        color: #FFFFFF !important;
        font-size: 1.9rem !important;
        margin: 0 0 0.5rem 0 !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    .exec-banner p {
        color: #E2E8F0 !important;
        font-size: 0.96rem !important;
        margin-bottom: 0.25rem !important;
    }
    .exec-banner strong {
        color: #FFFFFF !important;
    }

    /* CUSTOM LIGHT KPI CARDS (FIXES DARK DELTA PILLS) */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0F2537;
        padding: 1.15rem 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    }
    .kpi-label {
        font-size: 0.84rem;
        font-weight: 600;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0F2537 !important;
        line-height: 1.15;
        margin-bottom: 0.45rem;
    }
    .kpi-badge-neutral {
        display: inline-block;
        background-color: #F1F5F9;
        color: #334155 !important;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
    }
    .kpi-badge-pos {
        display: inline-block;
        background-color: #DCFCE7;
        color: #166534 !important;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
    }
    .kpi-badge-alert {
        display: inline-block;
        background-color: #FEE2E2;
        color: #991B1B !important;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
    }

    /* CLEAN TAB STYLING */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #475569 !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding-bottom: 0.6rem;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #0F2537 !important;
        border-bottom-color: #C0392B !important;
    }

    /* TOP CHAPTER INTRO BANNER */
    .insight-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0F2537;
        padding: 1rem 1.3rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1.2rem;
        color: #1E293B !important;
        font-size: 0.95rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    /* CHART EXPLANATION CARD */
    .chart-explain {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin-top: 0.35rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(15, 23, 42, 0.03);
    }
    .chart-explain-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #1D4ED8 !important;
        margin-bottom: 0.35rem;
    }
    .chart-explain p {
        font-size: 0.91rem;
        line-height: 1.55;
        color: #334155 !important;
        margin-bottom: 0;
    }

    /* STRATEGY & LIMITATIONS WHITE CARDS */
    .strategy-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 1.4rem 1.6rem;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LOAD CLEAN DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sales_path = os.path.join(base_dir, "..", "data", "processed", "clean_retail_sales.csv")
    hyb_path = os.path.join(base_dir, "..", "data", "processed", "clean_ev_hybrids.csv")
    
    df_sales = pd.read_csv(sales_path, parse_dates=['FECHA'])
    df_hyb = pd.read_csv(hyb_path, parse_dates=['FECHA'])
    
    if 'ESTATUS_EN' not in df_sales.columns:
        df_sales['ESTATUS_EN'] = df_sales['ESTATUS'].replace({
            'Cifras Definitivas': 'Revised Figures',
            'Cifras Preliminares': 'Preliminary Figures'
        })
    return df_sales, df_hyb

df_sales, df_hyb = load_data()

# Helper to enforce crisp Light Mode on all Plotly charts & axes
def style_light_chart(fig, title_text, y_title="", x_title="", height=440, legend_bottom=False, hovermode="x unified"):
    legend_cfg = (
        dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, font=dict(color="#1E293B", size=12))
        if legend_bottom else
        dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#1E293B", size=12))
    )
    fig.update_layout(
        title=dict(text=f"<b>{title_text}</b>", font=dict(size=16, color="#0F2537", family="sans-serif"), x=0.01),
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#1E293B", family="sans-serif"),
        height=height,
        hovermode=hovermode,
        legend=legend_cfg,
        margin=dict(t=65, b=85 if legend_bottom else 35, l=55, r=25)
    )
    fig.update_xaxes(
        title=dict(text=x_title, font=dict(color="#334155", size=12)),
        showgrid=False,
        linecolor="#CBD5E1",
        tickfont=dict(color="#334155", size=11)
    )
    fig.update_yaxes(
        title=dict(text=y_title, font=dict(color="#334155", size=12)),
        gridcolor="#E2E8F0",
        gridwidth=1,
        linecolor="#CBD5E1",
        tickfont=dict(color="#334155", size=11)
    )
    return fig

# ---------------------------------------------------------
# 3. EXECUTIVE HEADER BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="exec-banner">
    <div class="banner-title">Reshaping Mexico's Light-Vehicle Market (2016–2026)</div>
    <p><strong>Role:</strong> Market Strategy Analyst (Legacy Automaker in Mexico) &nbsp;|&nbsp; <strong>Stakeholders:</strong> Executive Committee & Product Planning</p>
    <p><strong>Strategic Decision:</strong> How should we reallocate our 2027 product portfolio across SUVs, sedans, and electrified powertrains amid Asian brand expansion and the January 2026 tariff shift?</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. SIDEBAR: INTERACTIVE CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### Analytical Controls")
    st.caption("Slice the 10-year RAIAVL dataset by timeframe, segment, corporate group, or state.")
    
    st.markdown("**1. Time Horizon**")
    min_year = int(df_sales['ANIO'].min())
    max_year = int(df_sales['ANIO'].max())
    year_range = st.slider(
        "Select Year Window",
        min_value=min_year,
        max_value=max_year,
        value=(2016, max_year),
        label_visibility="collapsed"
    )

    st.markdown("**2. Market & Portfolio Scope**")
    segments = sorted(df_sales['SEGMENTO'].dropna().unique())
    sel_segments = st.multiselect(
        "Vehicle Segment",
        options=segments,
        default=segments
    )

    groups = sorted(df_sales['GRUPO_AUTOMOTRIZ'].dropna().unique())
    sel_groups = st.multiselect(
        "Corporate Group (All if empty)",
        options=groups,
        default=[]
    )

    st.markdown("**3. Regional Electromobility**")
    states = sorted(df_hyb['ESTADO'].dropna().unique())
    sel_states = st.multiselect(
        "State (Electromobility Tab)",
        options=states,
        default=[]
    )

    st.markdown("""
    <div class="sidebar-card">
        <strong>Dataset Metadata</strong><br>
        Source: INEGI RAIAVL<br>
        Vintage: October 2026<br>
        Panel: AMIA/INEGI Reporting Brands<br>
        Note: Stellantis & Jetour groups harmonized across years.
    </div>
    """, unsafe_allow_html=True)

# Apply filters
mask_sales = (
    (df_sales['ANIO'] >= year_range[0]) &
    (df_sales['ANIO'] <= year_range[1]) &
    (df_sales['SEGMENTO'].isin(sel_segments))
)
if sel_groups:
    mask_sales = mask_sales & (df_sales['GRUPO_AUTOMOTRIZ'].isin(sel_groups))
df_sales_f = df_sales[mask_sales].copy()

mask_hyb = (
    (df_hyb['ANIO'] >= year_range[0]) &
    (df_hyb['ANIO'] <= year_range[1])
)
if sel_states:
    mask_hyb = mask_hyb & (df_hyb['ESTADO'].isin(sel_states))
df_hyb_f = df_hyb[mask_hyb].copy()

# ---------------------------------------------------------
# 5. EXECUTIVE KPIs (CUSTOM HIGH-CONTRAST LIGHT CARDS)
# ---------------------------------------------------------
total_units = df_sales_f['UNI_VEH'].sum()
sales_2026 = df_sales_f[df_sales_f['ANIO'] == 2026]['UNI_VEH'].sum()
max_month_2026 = df_sales_f[df_sales_f['ANIO'] == 2026]['ID_MES'].max()
sales_2025_ytd = df_sales_f[
    (df_sales_f['ANIO'] == 2025) & 
    (df_sales_f['ID_MES'] <= max_month_2026)
]['UNI_VEH'].sum()

yoy_2026 = ((sales_2026 / sales_2025_ytd) - 1) * 100 if sales_2025_ytd > 0 else 0
chinese_share_2026 = (
    df_sales_f[(df_sales_f['ANIO'] == 2026) & (df_sales_f['ORIGEN_MARCA'] == 'Chinese Brands (in RAIAVL)')]['UNI_VEH'].sum()
    / sales_2026 * 100
) if sales_2026 > 0 else 0
total_electrified = df_hyb_f['TOTAL_ELECTRIFICADOS'].sum()

yoy_badge_class = "kpi-badge-pos" if yoy_2026 >= 0 else "kpi-badge-alert"

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Cumulative Retail Sales</div>
        <div class="kpi-value">{total_units:,.0f}</div>
        <span class="kpi-badge-neutral">{year_range[0]}–{year_range[1]} Window</span>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">2026 YTD Sales (Jan–Oct)</div>
        <div class="kpi-value">{sales_2026:,.0f}</div>
        <span class="{yoy_badge_class}">{yoy_2026:+.1f}% YoY vs 2025</span>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Chinese Brand Share (2026)</div>
        <div class="kpi-value">{chinese_share_2026:.1f}%</div>
        <span class="kpi-badge-alert">RAIAVL reporting panel only</span>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Electrified Vehicles Sold</div>
        <div class="kpi-value">{total_electrified:,.0f}</div>
        <span class="kpi-badge-pos">HEV + PHEV + BEV</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. ORGANIZED STORYTELLING TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Macro Trend & Shocks",
    "2. Segment & Competitive Shift",
    "3. Electromobility Adoption",
    "4. Strategy & Data Coverage"
])

# === TAB 1: MACRO TREND & SHOCKS ===
with tab1:
    st.markdown("""
    <div class="insight-box">
        <strong>Chapter Overview:</strong> To evaluate structural industry health without seasonal distortion, we track light-vehicle demand across a full decade alongside major supply, health, and trade shocks.
    </div>
    """, unsafe_allow_html=True)

    time_view = st.radio(
        "Select Time Series View:",
        ["12-Month Rolling Total (Seasonally Adjusted Trend)", "Monthly Volume (Revised vs. Preliminary Figures)"],
        horizontal=True
    )

    ts_monthly = df_sales_f.groupby(['FECHA', 'ESTATUS_EN'], as_index=False)['UNI_VEH'].sum().sort_values('FECHA')
    ts_total = df_sales_f.groupby('FECHA', as_index=False)['UNI_VEH'].sum().sort_values('FECHA')
    ts_total['ROLLING_12M'] = ts_total['UNI_VEH'].rolling(12).sum()

    if "12-Month Rolling" in time_view:
        fig_ts = px.area(
            ts_total.dropna(subset=['ROLLING_12M']),
            x='FECHA',
            y='ROLLING_12M'
        )
        fig_ts.update_traces(
            line=dict(color='#0F2537', width=3),
            fillcolor='rgba(15, 37, 55, 0.08)',
            hovertemplate='<b>%{x|%b %Y}</b><br>Trailing 12M Sales: %{y:,.0f} units<extra></extra>'
        )
        chart_title = "12-Month Rolling Light-Vehicle Retail Sales (Units)"
        y_axis_label = "Trailing 12-Month Units"
    else:
        fig_ts = px.bar(
            ts_monthly,
            x='FECHA',
            y='UNI_VEH',
            color='ESTATUS_EN',
            color_discrete_map={'Revised Figures': '#0F2537', 'Preliminary Figures': '#D97706'}
        )
        chart_title = "Monthly Retail Sales Breakdown (Revised vs. Preliminary)"
        y_axis_label = "Monthly Units Sold"

    events = [
        ("2020-04-01", "COVID-19 Shock", "right", 1.03),
        ("2021-09-01", "Chip Shortage", "left", 0.90),
        ("2023-06-01", "Chinese Brand Wave", "left", 1.03),
        ("2026-01-01", "Jan 2026 Tariffs", "right", 1.03)
    ]

    for event_date, event_label, align, y_pos in events:
        if year_range[0] <= int(event_date[:4]) <= year_range[1]:
            fig_ts.add_vline(x=event_date, line_dash="dot", line_color="#C0392B", line_width=1.5)
            fig_ts.add_annotation(
                x=event_date, y=y_pos, yref="paper", text=f"<b>{event_label}</b>",
                showarrow=False, font=dict(color="#C0392B", size=11),
                xanchor=align, bgcolor="rgba(255,255,255,0.9)", bordercolor="#FECACA", borderwidth=1, borderpad=3
            )

    fig_ts = style_light_chart(fig_ts, chart_title, y_title=y_axis_label, height=460, legend_bottom=False)
    st.plotly_chart(fig_ts, use_container_width=True)

    st.markdown("""
    <div class="chart-explain">
        <div class="chart-explain-title">What This Chart Means</div>
        <p><strong>1. Why 12-Month Rolling Matters:</strong> Monthly Mexican auto sales spike every December due to year-end fleet purchases and promotions. Summing the trailing 12 months removes seasonal noise to reveal true underlying momentum.<br>
        <strong>2. Four-Year Recovery Cycle:</strong> After peaking above 1.6M annual units in 2016–2017, the April 2020 pandemic lockdown drove trailing volume down toward ~950K units. Global semiconductor shortages (2021–2022) prolonged the trough, delaying full recovery until late 2023.<br>
        <strong>3. Recent Inflection Points:</strong> Expansion from 2023 onward was propelled by new Asian entrants joining the market, while the January 2026 tariff adjustment marks a new regulatory regime affecting non-USMCA imports. Note that the most recent 2026 bars (in amber) represent preliminary figures subject to minor automaker revisions.</p>
    </div>
    """, unsafe_allow_html=True)

# === TAB 2: SEGMENT & COMPETITIVE SHIFT ===
with tab2:
    st.markdown("""
    <div class="insight-box">
        <strong>Chapter Overview:</strong> Beyond aggregate volume, two structural forces are reshaping competitive advantage in Mexico: consumer migration toward SUVs and the rapid scaling of Chinese brands.
    </div>
    """, unsafe_allow_html=True)

    c_left, c_right = st.columns(2)

    with c_left:
        # Remade as clean multi-line trend of market share (%) so every segment trajectory is crisp & legible
        df_seg = df_sales_f.groupby(['ANIO', 'SEGMENTO'], as_index=False)['UNI_VEH'].sum()
        year_totals = df_seg.groupby('ANIO')['UNI_VEH'].transform('sum')
        df_seg['SHARE_PCT'] = (df_seg['UNI_VEH'] / year_totals) * 100

        seg_colors = {
            "SUV's": "#C0392B",
            "Subcompactos": "#0F2537",
            "Compactos": "#2563EB",
            "Pick Ups": "#0D9488",
            "Minivans": "#D97706",
            "De Lujo": "#7C3AED",
            "Deportivos": "#64748B"
        }

        fig_seg = px.line(
            df_seg,
            x='ANIO',
            y='SHARE_PCT',
            color='SEGMENTO',
            markers=True,
            color_discrete_map=seg_colors
        )
        fig_seg.update_traces(line=dict(width=2.6), marker=dict(size=6))
        fig_seg = style_light_chart(
            fig_seg,
            "Segment Market Share Trajectory (2016–2026)",
            y_title="Share of Retail Market (%)",
            height=440,
            legend_bottom=True
        )
        fig_seg.update_yaxes(ticksuffix="%")
        st.plotly_chart(fig_seg, use_container_width=True)

        st.markdown("""
        <div class="chart-explain">
            <div class="chart-explain-title">What This Chart Means</div>
            <p><strong>SUVs Overtook Entry Sedans as Mexico's Core Segment:</strong> Tracking each segment's share directly reveals a decisive crossover: <em>SUVs</em> (red line) surged from ~21% of the market in 2016 to over 40% by 2026, while <em>Subcompactos</em> and <em>Compactos</em> steadily contracted. Defending profit pools requires reallocating North American plant capacity toward small and compact crossovers.</p>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        df_origen = df_sales_f.groupby(['ANIO', 'ORIGEN_MARCA'], as_index=False)['UNI_VEH'].sum()
        yr_tot_orig = df_origen.groupby('ANIO')['UNI_VEH'].transform('sum')
        df_origen['PCT_LABEL'] = df_origen.apply(
            lambda r: f"{(r['UNI_VEH']/yr_tot_orig[r.name]*100):.1f}%" if r['ORIGEN_MARCA'] == 'Chinese Brands (in RAIAVL)' and (r['UNI_VEH']/yr_tot_orig[r.name]*100) >= 1.0 else "",
            axis=1
        )

        fig_origen = px.bar(
            df_origen,
            x='ANIO',
            y='UNI_VEH',
            color='ORIGEN_MARCA',
            barmode='stack',
            text='PCT_LABEL',
            color_discrete_map={
                'Traditional / Other Brands': '#0F2537',
                'Chinese Brands (in RAIAVL)': '#C0392B'
            }
        )
        fig_origen.update_traces(textposition='outside', textfont=dict(color='#C0392B', size=11, family='sans-serif'))
        fig_origen = style_light_chart(
            fig_origen,
            "Annual Sales: Legacy vs. Chinese Brands (in RAIAVL)",
            y_title="Annual Units Sold",
            height=440,
            legend_bottom=True
        )
        fig_origen.update_yaxes(range=[0, df_origen.groupby('ANIO')['UNI_VEH'].sum().max() * 1.15])
        st.plotly_chart(fig_origen, use_container_width=True)

        st.markdown("""
        <div class="chart-explain">
            <div class="chart-explain-title">What This Chart Means</div>
            <p><strong>Rapid Scaling of Asian Challengers:</strong> Chinese brands reporting to INEGI (MG Motor, Chirey/Omoda, JAC, Changan, Geely, Great Wall, GAC) scaled from under 1% prior to 2021 to <strong>11.8%</strong> of the RAIAVL panel in 2026. Because major players like <strong>BYD</strong> do not report to INEGI, actual competitive pressure in entry SUVs and sedans is even higher than shown.</p>
        </div>
        """, unsafe_allow_html=True)

# === TAB 3: ELECTROMOBILITY ADOPTION ===
with tab3:
    st.markdown("""
    <div class="insight-box">
        <strong>Chapter Overview:</strong> Crossing retail volume with INEGI's state-level electromobility registry reveals which powertrain technologies Mexican buyers actually adopt—and where demand is geographically concentrated.
    </div>
    """, unsafe_allow_html=True)

    h_left, h_right = st.columns(2)

    with h_left:
        df_tech = df_hyb_f.groupby('ANIO', as_index=False)[['VEH_HIBRIDAS', 'VEH_HIBRIDAS_PLUGIN', 'VEH_ELECTR']].sum()
        df_tech_melt = df_tech.melt(
            id_vars='ANIO',
            value_vars=['VEH_HIBRIDAS', 'VEH_HIBRIDAS_PLUGIN', 'VEH_ELECTR'],
            var_name='Technology',
            value_name='Units'
        )
        tech_map = {
            'VEH_HIBRIDAS': 'Conventional Hybrid (HEV)',
            'VEH_HIBRIDAS_PLUGIN': 'Plug-In Hybrid (PHEV)',
            'VEH_ELECTR': 'Battery Electric (BEV)'
        }
        df_tech_melt['Technology'] = df_tech_melt['Technology'].map(tech_map)

        fig_tech = px.bar(
            df_tech_melt,
            x='ANIO',
            y='Units',
            color='Technology',
            color_discrete_map={
                'Conventional Hybrid (HEV)': '#0D9488',
                'Plug-In Hybrid (PHEV)': '#2563EB',
                'Battery Electric (BEV)': '#F59E0B'
            }
        )
        fig_tech = style_light_chart(
            fig_tech,
            "Electrified Sales by Powertrain Technology",
            y_title="Annual Units Sold",
            height=440,
            legend_bottom=True
        )
        st.plotly_chart(fig_tech, use_container_width=True)

        st.markdown("""
        <div class="chart-explain">
            <div class="chart-explain-title">What This Chart Means</div>
            <p><strong>Hybrids (HEV) Lead the Transition:</strong> Unlike markets where pure battery-electric vehicles (BEVs) dominate policy narratives, Mexico's electrification wave is overwhelmingly driven by conventional hybrids (HEVs). HEVs eliminate range anxiety and public charging bottlenecks while offering immediate fuel economy gains—making them the highest-ROI near-term powertrain bet for 2027.</p>
        </div>
        """, unsafe_allow_html=True)

    with h_right:
        top_states = (
            df_hyb_f[df_hyb_f['ESTADO'] != 'Unspecified']
            .groupby('ESTADO', as_index=False)['TOTAL_ELECTRIFICADOS']
            .sum()
            .sort_values('TOTAL_ELECTRIFICADOS', ascending=True)
            .tail(10)
        )
        fig_est = px.bar(
            top_states,
            x='TOTAL_ELECTRIFICADOS',
            y='ESTADO',
            orientation='h',
            text='TOTAL_ELECTRIFICADOS'
        )
        fig_est.update_traces(
            marker_color='#0D9488',
            texttemplate='%{text:,.0f}',
            textposition='outside',
            textfont=dict(color='#0F2537', size=11)
        )
        fig_est = style_light_chart(
            fig_est,
            "Top 10 Mexican States in Hybrid & EV Adoption",
            x_title="Cumulative Electrified Units",
            height=440,
            legend_bottom=False,
            hovermode="y unified"
        )
        fig_est.update_xaxes(range=[0, top_states['TOTAL_ELECTRIFICADOS'].max() * 1.18], showgrid=True, gridcolor="#E2E8F0")
        fig_est.update_yaxes(showgrid=False)
        fig_est.update_layout(margin=dict(t=65, b=85, l=115, r=35))
        st.plotly_chart(fig_est, use_container_width=True)

        st.markdown("""
        <div class="chart-explain">
            <div class="chart-explain-title">What This Chart Means</div>
            <p><strong>Extreme Geographic Concentration:</strong> Electrified vehicle adoption is heavily concentrated in five major urban hubs—led by Mexico City, State of Mexico, Nuevo Leon, Jalisco, and Puebla—where higher incomes, corporate fleets, and local environmental exemptions (such as <em>Hoy No Circula</em>) incentivize adoption. Outside these hubs, internal combustion remains dominant.</p>
        </div>
        """, unsafe_allow_html=True)

# === TAB 4: STRATEGY, LIMITATIONS & COVERAGE ===
with tab4:
    st.markdown("""
    <div class="insight-box">
        <strong>Methodological Transparency & Coverage Caveats (Vintage: October 2026):</strong><br>
        • <strong>Non-Reporting Brands:</strong> RAIAVL is based on voluntary reporting by AMIA/INEGI-affiliated automakers. <strong>BYD and Tesla do not report to INEGI</strong>, meaning actual BEV volumes and Chinese market share are understated.<br>
        • <strong>Panel Entries & Exits:</strong> Aggregate movements partly reflect registry panel changes—for example, <strong>GAC</strong> joined with retroactive data back to Jan 2024, while <strong>MOTORNATION</strong> exits starting Nov 2026.<br>
        • <strong>Brand Harmonization:</strong> <em>Chrysler, Fiat, Peugeot, Alfa Romeo, and Leapmotor</em> are consolidated under <strong>Stellantis</strong>; <em>JETOUR</em> and <em>Jetour Soueast</em> are unified for decade-long consistency.
    </div>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        st.markdown("""
        <div class="strategy-card">
            <h3 style="color:#0F2537; margin-top:0;">Actionable Recommendations for 2027</h3>
            <ol style="color:#334155; line-height:1.65; font-size:0.94rem;">
                <li><strong>Lead with Conventional Hybrids (HEV):</strong> Prioritize HEV trims over pure BEVs in near-term product launches and marketing spend to match Mexican consumer demand and charging infrastructure realities.</li>
                <li><strong>Defend Core SUVs Over Entry Sedans:</strong> Reallocate North American manufacturing capacity toward compact and subcompact SUVs, where structural demand and margin pools are expanding.</li>
                <li><strong>Deploy a Tiered Geographic Rollout:</strong> Concentrate electrified inventory and dealer incentives in the top 5 adopting states (CDMX, State of Mexico, Nuevo Leon, Jalisco, Puebla) while defending share with efficient ICE models elsewhere.</li>
                <li><strong>Capitalize on the January 2026 Tariff Shift:</strong> Leverage USMCA-compliant regional production to recapture share from non-FTA imported vehicles facing higher duties.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="strategy-card">
            <h3 style="color:#0F2537; margin-top:0;">What RAIAVL Cannot See (Limitations)</h3>
            <ul style="color:#334155; line-height:1.65; font-size:0.94rem;">
                <li><strong>Competitive Blind Spots in EVs:</strong> Without BYD and Tesla, RAIAVL cannot capture the full competitive threat in entry-level electric vehicles. Management must triangulate this dashboard with state vehicle registration (<em>emplacamiento</em>) and customs import data.</li>
                <li><strong>No Pricing or Incentive Visibility:</strong> The registry tracks physical unit volumes (<code>UNI_VEH</code>), omitting transaction prices, financing subsidies, and dealer margin compression.</li>
                <li><strong>No Plant-Level Output in Retail Tables:</strong> Retail sales distinguish between <em>Domestic</em> and <em>Imported</em> origin, but do not disclose specific assembly plants or regional value content percentages.</li>
                <li><strong>Preliminary Data Revisions:</strong> Recent 2026 monthly figures include preliminary automaker reports subject to future adjustment.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)