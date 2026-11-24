import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM CSS STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Mexico Automotive Market Strategy (2016-2026)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Clean executive typography and spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1350px;
    }

    /* REDESIGNED DARK EXECUTIVE SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #0F2537;
        border-right: 2px solid #1E3A5F;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FFFFFF !important;
        font-size: 1.15rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        border-bottom: 2px solid #C0392B;
        padding-bottom: 0.5rem;
        margin-bottom: 0.8rem;
    }
    /* Sidebar input boxes & multiselect tags */
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
    /* Sidebar metadata card */
    .sidebar-card {
        background-color: #16324A;
        border-left: 3px solid #C0392B;
        padding: 0.85rem 1rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.83rem;
        line-height: 1.45;
        margin-top: 1rem;
        color: #E2E8F0 !important;
    }

    /* Executive Header Banner */
    .exec-banner {
        background-color: #0F2537;
        color: #FFFFFF;
        padding: 1.8rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 6px solid #C0392B;
    }
    .exec-banner h1 {
        color: #FFFFFF;
        font-size: 1.9rem;
        margin-bottom: 0.4rem;
        font-weight: 700;
    }
    .exec-banner p {
        color: #D6E0E8;
        font-size: 0.98rem;
        margin-bottom: 0.2rem;
    }

    /* Styled KPI Cards */
    div[data-testid="metric-container"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0F2537;
        padding: 1rem 1.2rem;
        border-radius: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    /* Insight Callout Box */
    .insight-box {
        background-color: #F1F5F9;
        border-left: 4px solid #2B5C8F;
        padding: 1rem 1.2rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 1.2rem;
        color: #1E293B;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. LOAD CLEAN DATA (WITH FALLBACK SAFETY)
# ---------------------------------------------------------
import os
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
# ---------------------------------------------------------
# 3. EXECUTIVE HEADER BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="exec-banner">
    <h1>Reshaping Mexico's Light-Vehicle Market (2016–2026)</h1>
    <p><strong>Role:</strong> Market Strategy Analyst (Legacy Automaker in Mexico) &nbsp;|&nbsp; <strong>Stakeholders:</strong> Executive Committee & Product Planning</p>
    <p><strong>Strategic Decision:</strong> How should we reallocate our 2027 product portfolio across SUVs, sedans, and electrified powertrains amid Asian brand expansion and the January 2026 tariff shift?</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. REDESIGNED SIDEBAR: INTERACTIVE CONTROLS
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
# 5. EXECUTIVE KPIs
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

k1, k2, k3, k4 = st.columns(4)
k1.metric("Cumulative Retail Sales", f"{total_units:,.0f}", f"{year_range[0]}–{year_range[1]}")
k2.metric("2026 YTD Sales (Jan–Oct)", f"{sales_2026:,.0f}", f"{yoy_2026:+.1f}% YoY vs 2025")
k3.metric("Chinese Brand Share (2026)", f"{chinese_share_2026:.1f}%", "RAIAVL reporting panel only")
k4.metric("Electrified Vehicles Sold", f"{total_electrified:,.0f}", "HEV + PHEV + BEV")

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
        <strong>Key Takeaway:</strong> Stripping out December seasonality via a 12-month rolling total shows that Mexico's light-vehicle market required nearly four years to recover from the 2020 pandemic and 2021–2022 semiconductor bottlenecks. Growth since 2023 has been heavily shaped by new entrants and the January 2026 tariff realignment.
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
        fig_ts = px.line(
            ts_total.dropna(subset=['ROLLING_12M']),
            x='FECHA',
            y='ROLLING_12M',
            labels={'FECHA': '', 'ROLLING_12M': 'Trailing 12-Month Units'}
        )
        fig_ts.update_traces(line=dict(color='#0F2537', width=3.2))
        chart_title = "12-Month Rolling Light-Vehicle Retail Sales (Units)"
    else:
        fig_ts = px.bar(
            ts_monthly,
            x='FECHA',
            y='UNI_VEH',
            color='ESTATUS_EN',
            labels={'FECHA': '', 'UNI_VEH': 'Monthly Units', 'ESTATUS_EN': 'Data Status'},
            color_discrete_map={'Revised Figures': '#0F2537', 'Preliminary Figures': '#D97706'}
        )
        chart_title = "Monthly Retail Sales Breakdown (Revised vs. Preliminary)"

    events = [
        ("2020-04-01", "COVID-19 Shock", "left"),
        ("2021-09-01", "Chip Shortage", "right"),
        ("2023-06-01", "Chinese Brand Wave", "left"),
        ("2026-01-01", "Jan 2026 Tariffs", "right")
    ]

    for event_date, event_label, align in events:
        if year_range[0] <= int(event_date[:4]) <= year_range[1]:
            fig_ts.add_vline(x=event_date, line_dash="dot", line_color="#C0392B", line_width=1.5)
            fig_ts.add_annotation(
                x=event_date, y=1.03, yref="paper", text=event_label,
                showarrow=False, font=dict(color="#C0392B", size=11, family="Arial"),
                xanchor=align
            )

    fig_ts.update_layout(
        title=dict(text=chart_title, font=dict(size=16, color="#0F2537")),
        template="plotly_white",
        height=460,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=20)
    )
    st.plotly_chart(fig_ts, use_container_width=True)

# === TAB 2: SEGMENT & COMPETITIVE SHIFT ===
with tab2:
    st.markdown("""
    <div class="insight-box">
        <strong>Key Takeaway:</strong> Two structural forces are squeezing legacy automakers: consumer migration from traditional subcompact/compact sedans toward SUVs, and the rapid entry of Chinese brands into the RAIAVL panel since 2022.
    </div>
    """, unsafe_allow_html=True)

    c_left, c_right = st.columns(2)

    with c_left:
        df_seg = df_sales_f.groupby(['ANIO', 'SEGMENTO'], as_index=False)['UNI_VEH'].sum()
        fig_seg = px.area(
            df_seg,
            x='ANIO',
            y='UNI_VEH',
            color='SEGMENTO',
            groupnorm='percent',
            labels={'ANIO': '', 'UNI_VEH': 'Share of Retail Market (%)', 'SEGMENTO': 'Segment'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_seg.update_layout(
            title=dict(text="Market Share by Vehicle Segment (%)", font=dict(size=15, color="#0F2537")),
            template="plotly_white",
            height=430,
            legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
            margin=dict(t=50, b=80)
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    with c_right:
        df_origen = df_sales_f.groupby(['ANIO', 'ORIGEN_MARCA'], as_index=False)['UNI_VEH'].sum()
        fig_origen = px.bar(
            df_origen,
            x='ANIO',
            y='UNI_VEH',
            color='ORIGEN_MARCA',
            barmode='stack',
            labels={'ANIO': '', 'UNI_VEH': 'Annual Units', 'ORIGEN_MARCA': ''},
            color_discrete_map={
                'Traditional / Other Brands': '#0F2537',
                'Chinese Brands (in RAIAVL)': '#C0392B'
            }
        )
        fig_origen.update_layout(
            title=dict(text="Annual Sales: Legacy vs. Chinese Brands (in RAIAVL)", font=dict(size=15, color="#0F2537")),
            template="plotly_white",
            height=430,
            legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
            margin=dict(t=50, b=80)
        )
        st.plotly_chart(fig_origen, use_container_width=True)

# === TAB 3: ELECTROMOBILITY ADOPTION ===
with tab3:
    st.markdown("""
    <div class="insight-box">
        <strong>Key Takeaway:</strong> Electrification in Mexico is overwhelmingly a conventional hybrid (HEV) story rather than pure battery-electric (BEV), with demand heavily concentrated in five metropolitan states.
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
            labels={'ANIO': '', 'Units': 'Units Sold', 'Technology': ''},
            color_discrete_map={
                'Conventional Hybrid (HEV)': '#1E8449',
                'Plug-In Hybrid (PHEV)': '#2E86C1',
                'Battery Electric (BEV)': '#F39C12'
            }
        )
        fig_tech.update_layout(
            title=dict(text="Electrified Sales by Powertrain Technology", font=dict(size=15, color="#0F2537")),
            template="plotly_white",
            height=430,
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            margin=dict(t=50, b=70)
        )
        st.plotly_chart(fig_tech, use_container_width=True)

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
            labels={'TOTAL_ELECTRIFICADOS': 'Cumulative Units', 'ESTADO': ''}
        )
        fig_est.update_traces(marker_color='#1E8449')
        fig_est.update_layout(
            title=dict(text="Top 10 Mexican States in Hybrid & EV Adoption", font=dict(size=15, color="#0F2537")),
            template="plotly_white",
            height=430,
            margin=dict(t=50, b=40)
        )
        st.plotly_chart(fig_est, use_container_width=True)

# === TAB 4: STRATEGY, LIMITATIONS & COVERAGE ===
with tab4:
    st.subheader("Methodological Honesty & RAIAVL Coverage Gaps")
    st.warning("""
    **Critical Coverage Caveats (Vintage: October 2026):**
    * **Non-Reporting Brands:** RAIAVL relies on voluntary reporting from AMIA/INEGI-affiliated automakers. **BYD and Tesla do not report to INEGI**, meaning actual BEV volumes and Chinese brand penetration in Mexico are understated here.
    * **Panel Entries & Exits:** Aggregate series jumps partly reflect registry panel changes—for instance, **GAC** joined with retroactive data back to January 2024, while **MOTORNATION** exits the registry starting November 2026.
    * **Brand Harmonization:** *Chrysler, Fiat, Peugeot, Alfa Romeo, and Leapmotor* were consolidated under **Stellantis**; *JETOUR* and *Jetour Soueast* were unified to ensure decade-long consistency.
    * **Preliminary vs. Revised Data:** Recent 2026 months contain *Preliminary Figures* subject to automaker revisions.
    """)

    st.markdown("---")
    s1, s2 = st.columns(2)

    with s1:
        st.subheader("Actionable Recommendations for 2027")
        st.markdown("""
        1. **Lead with Conventional Hybrids (HEV):** Allocate near-term product engineering and marketing toward HEV trims rather than pure BEVs, matching Mexican infrastructure realities and consumer demand.
        2. **Defend Core SUVs Over Entry Sedans:** Concentrate North American plant capacity on compact and subcompact SUVs, where profit pools and structural demand are expanding.
        3. **Deploy a Tiered Geographic Rollout:** Focus electrified inventory and dealer incentives on the top 5 adopting states (Mexico City, State of Mexico, Nuevo Leon, Jalisco, and Puebla).
        4. **Capitalize on the January 2026 Tariff Shift:** Leverage USMCA-compliant regional production to recapture share from non-FTA imported vehicles facing higher duties.
        """)

    with s2:
        st.subheader("What RAIAVL Cannot See (Limitations)")
        st.markdown("""
        * **Blind Spots in EV & Chinese Competition:** Without BYD and Tesla, RAIAVL cannot capture the full competitive threat in entry-level EVs. Management must triangulate this dashboard with state vehicle registration (emplacamiento) and customs import data.
        * **No Pricing or Incentive Visibility:** The registry tracks physical unit volumes (`UNI_VEH`), omitting transaction prices, financing rates, and dealer margin compression.
        * **No Plant-Level Output in Retail Tables:** Retail sales distinguish *Domestic* vs. *Imported* origin, but do not identify specific assembly plants or regional content percentages.
        """)