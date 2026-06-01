"""
NSAP-AI · Government of India · Ministry of Rural Development
Deceased Beneficiary Fraud Detection Portal
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# ── Page config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NSAP-AI | Fraud Detection Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- fonts & reset ---------- */
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .block-container,
[class*="css"] {
    font-family: 'Segoe UI', Arial, sans-serif !important;
    background-color: #f2f4f7 !important;
}

/* ---------- hide streamlit chrome ---------- */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem !important; }

/* ============================================================
   HEADER
   ============================================================ */
.gov-wrap {
    background: #003087;
    margin: -1rem -2rem 1.5rem -2rem;
    padding: 0;
    border-bottom: 5px solid #FF9933;
}
.gov-top {
    display: flex; align-items: center; gap: 18px;
    padding: 16px 32px 12px;
}
.gov-emblem-circle {
    width: 64px; height: 64px; border-radius: 50%;
    background: rgba(255,255,255,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; flex-shrink: 0;
}
.gov-text { flex: 1; }
.gov-ministry {
    font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; color: rgba(255,255,255,0.7);
    margin-bottom: 3px;
}
.gov-name {
    font-size: 22px; font-weight: 800; color: #fff;
    letter-spacing: 0.2px; line-height: 1.15;
}
.gov-sub { font-size: 11.5px; color: rgba(255,255,255,0.6); margin-top: 3px; }
.gov-status {
    text-align: right;
    font-size: 11px; color: rgba(255,255,255,0.6); line-height: 2;
}
.status-pill {
    display: inline-block; background: #16a34a;
    color: #fff; font-size: 10px; font-weight: 700;
    letter-spacing: 1px; padding: 3px 10px; border-radius: 2px;
    text-transform: uppercase;
}
.gov-nav-bar {
    background: #002070;
    display: flex; flex-wrap: wrap;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding: 0 24px;
}
.gov-nav-bar a {
    color: rgba(255,255,255,0.75) !important;
    font-size: 12.5px; font-weight: 500;
    padding: 10px 18px; text-decoration: none !important;
    border-bottom: 3px solid transparent;
    letter-spacing: 0.2px;
}
.gov-nav-bar a:hover { color: #fff !important; border-bottom-color: #FF9933; }

/* ============================================================
   SIDEBAR
   ============================================================ */
[data-testid="stSidebar"] {
    background: #fff !important;
    border-right: 1px solid #dde2ec !important;
}
/* Force all sidebar text to dark */
[data-testid="stSidebar"] * {
    font-family: 'Segoe UI', Arial, sans-serif !important;
    color: #1e293b !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #1e293b !important;
}
/* Radio button labels */
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stRadio span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #1e293b !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
}
/* Selected radio item */
[data-testid="stSidebar"] .stRadio [aria-checked="true"] span {
    color: #003087 !important;
    font-weight: 700 !important;
}
/* Sidebar background areas */
[data-testid="stSidebar"] > div:first-child {
    background: #fff !important;
}
.sidebar-logo {
    background: #003087 !important;
    margin: -1rem -1rem 1rem -1rem;
    padding: 16px 18px;
    border-bottom: 3px solid #FF9933;
}
.sidebar-logo-txt { color: #fff !important; font-size: 15px; font-weight: 700; }
.sidebar-logo-sub { color: rgba(255,255,255,0.65) !important; font-size: 10.5px; margin-top: 2px; }
.sidebar-stats {
    background: #f8fafc !important;
    border: 1px solid #dde2ec;
    border-radius: 6px;
    padding: 14px 16px;
    margin-top: 8px;
}
.sidebar-stat-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #eef0f4; font-size: 12px; }
.sidebar-stat-row:last-child { border-bottom: none; }
.ss-label { color: #64748b !important; }
.ss-value { color: #003087 !important; font-weight: 700; }

/* ============================================================
   KPI CARDS  — fully custom HTML
   ============================================================ */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.kpi-card {
    background: #ffffff;
    border: 1px solid #dde2ec;
    border-radius: 8px;
    padding: 18px 20px 16px;
    border-top: 4px solid #003087;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.kpi-card.orange { border-top-color: #FF9933; }
.kpi-card.red    { border-top-color: #dc2626; }
.kpi-card.green  { border-top-color: #16a34a; }
.kpi-card.teal   { border-top-color: #0891b2; }
.kpi-label {
    font-size: 10.5px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #64748b; margin-bottom: 8px;
}
.kpi-value {
    font-size: 28px; font-weight: 800; color: #0f172a;
    line-height: 1; letter-spacing: -0.5px;
}
.kpi-sub { font-size: 11px; color: #94a3b8; margin-top: 5px; }

/* ── Mobile responsive ── */
@media (max-width: 768px) {
    .kpi-grid   { grid-template-columns: repeat(2, 1fr) !important; }
    .kpi-grid-4 { grid-template-columns: repeat(2, 1fr) !important; }
    .gov-top { flex-direction: column; align-items: flex-start; gap: 10px; padding: 12px 16px 8px; }
    .gov-status { text-align: left; }
    .gov-name { font-size: 16px !important; }
    .gov-nav-bar a { font-size: 11px; padding: 8px 10px; }
    .kpi-value { font-size: 22px !important; }
    .chips { gap: 6px; }
    .chip { font-size: 10.5px; padding: 3px 8px; }
    .result-name { font-size: 18px !important; }
    .page-banner { flex-direction: column; gap: 6px; }
    .sec-card { padding: 14px 14px 12px; }
}
@media (max-width: 480px) {
    .kpi-grid   { grid-template-columns: 1fr 1fr !important; }
    .kpi-grid-4 { grid-template-columns: 1fr 1fr !important; }
    .kpi-value  { font-size: 20px !important; }
    .gov-name   { font-size: 14px !important; }
    .gov-ministry { font-size: 9px !important; }
}

/* 4-col variant */
.kpi-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}

/* ============================================================
   SECTION CARDS
   ============================================================ */
.sec-card {
    background: #ffffff;
    border: 1px solid #dde2ec;
    border-radius: 8px;
    padding: 20px 22px 18px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.sec-title {
    font-size: 12px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1px; color: #003087;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 10px; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}

/* ============================================================
   PAGE HEADING BANNER
   ============================================================ */
.page-banner {
    background: #fff;
    border: 1px solid #dde2ec;
    border-left: 6px solid #FF9933;
    border-radius: 6px;
    padding: 14px 20px;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.pb-icon { font-size: 1.6rem; }
.pb-title { font-size: 16px; font-weight: 800; color: #003087; margin-bottom: 2px; }
.pb-sub   { font-size: 11.5px; color: #64748b; }

/* ============================================================
   RISK BADGES
   ============================================================ */
.risk-critical { display:inline-block; background:#fee2e2; color:#991b1b; border:1px solid #fca5a5; padding:2px 9px; border-radius:3px; font-size:11px; font-weight:700; letter-spacing:0.5px; }
.risk-high     { display:inline-block; background:#ffedd5; color:#9a3412; border:1px solid #fdba74; padding:2px 9px; border-radius:3px; font-size:11px; font-weight:700; letter-spacing:0.5px; }
.risk-medium   { display:inline-block; background:#fef9c3; color:#854d0e; border:1px solid #fde047; padding:2px 9px; border-radius:3px; font-size:11px; font-weight:700; letter-spacing:0.5px; }
.risk-low      { display:inline-block; background:#dcfce7; color:#166534; border:1px solid #86efac; padding:2px 9px; border-radius:3px; font-size:11px; font-weight:700; letter-spacing:0.5px; }

/* ============================================================
   SEARCH RESULT CARD
   ============================================================ */
.result-wrap {
    background: #fff; border: 1px solid #dde2ec; border-radius: 8px;
    padding: 22px 26px; margin-top: 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.result-rec-id { font-size: 10.5px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #64748b; margin-bottom: 4px; }
.result-name   { font-size: 22px; font-weight: 800; color: #003087; margin-bottom: 14px; line-height: 1.2; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }
.chip  { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; font-size: 11.5px; font-weight: 500; padding: 4px 12px; border-radius: 4px; }
.chip.warn { background: #fff7ed; border-color: #fed7aa; color: #9a3412; }
.chip.ok   { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }

/* ============================================================
   ALERT BOXES
   ============================================================ */
.alert-warn { background: #fffbeb; border: 1px solid #fcd34d; border-left: 4px solid #f59e0b; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #78350f; margin: 8px 0; }
.alert-err  { background: #fef2f2; border: 1px solid #fca5a5; border-left: 4px solid #dc2626; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #7f1d1d; margin: 8px 0; }
.alert-ok   { background: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #16a34a; padding: 12px 16px; border-radius: 4px; font-size: 13px; color: #14532d; margin: 8px 0; }

/* ============================================================
   TABLE STYLING
   ============================================================ */
[data-testid="stDataFrame"] { border: 1px solid #dde2ec !important; border-radius: 6px !important; }
[data-testid="stDataFrame"] table { font-size: 13px !important; }
[data-testid="stDataFrame"] th { background: #f1f5f9 !important; color: #003087 !important; font-weight: 700 !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }

/* ============================================================
   DIVIDER & MISC
   ============================================================ */
hr { border-color: #e2e8f0 !important; margin: 16px 0 !important; }
.stRadio label { font-size: 13.5px !important; color: #1e293b !important; }
.stSelectbox label, .stTextInput label { font-size: 13px !important; font-weight: 600 !important; color: #374151 !important; }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────────────────
now = datetime.now()
st.markdown(f"""
<div class="gov-wrap">
  <div class="gov-top">
    <div class="gov-emblem-circle">🏛️</div>
    <div class="gov-text">
      <div class="gov-ministry">Government of India &nbsp;·&nbsp; Ministry of Rural Development &nbsp;·&nbsp; National Social Assistance Programme</div>
      <div class="gov-name">NSAP-AI &nbsp;|&nbsp; Deceased Beneficiary Fraud Detection Portal</div>
      <div class="gov-sub">AI-Powered Welfare Fraud Prevention &amp; Real-time Risk Monitoring System</div>
    </div>
    <div class="gov-status">
      <div>{now.strftime("%d %B %Y, %I:%M %p IST")}</div>
      <div style="margin-top:6px;"><span class="status-pill">● System Online</span></div>
    </div>
  </div>
  <div class="gov-nav-bar">
    <a href="#" onclick="nsapNav('Overview'); return false;">🏠 Home</a>
    <a href="#" onclick="nsapNav('Overview'); return false;">📋 Overview</a>
    <a href="#" onclick="nsapNav('High-Risk'); return false;">🚨 High Risk</a>
    <a href="#" onclick="nsapNav('Search'); return false;">🔍 Search</a>
    <a href="#" onclick="nsapNav('Analytics'); return false;">📊 Reports</a>
    <a href="#" onclick="nsapNav('About'); return false;">ℹ️ Help</a>
  </div>
</div>
<script>
function nsapNav(keyword) {
    var labels = window.parent.document.querySelectorAll('[data-testid="stSidebar"] label');
    if (!labels.length) {
        labels = document.querySelectorAll('[data-testid="stSidebar"] label');
    }
    for (var i = 0; i < labels.length; i++) {
        if (labels[i].innerText.indexOf(keyword) >= 0) {
            labels[i].click();
            return;
        }
    }
}
</script>
""", unsafe_allow_html=True)

# ── LOAD DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        ben  = pd.read_csv(os.path.join(base, "enhanced_beneficiaries.csv"))
        risk = pd.read_csv(os.path.join(base, "risk_scores.csv"))
        txn  = pd.read_csv(os.path.join(base, "enhanced_transactions.csv"))
        dth  = pd.read_csv(os.path.join(base, "enhanced_death_records.csv"))
        risk['risk_level'] = risk['risk_level'].fillna('LOW')
        return ben, risk, txn, dth
    except Exception as e:
        st.error(f"Data load error: {e}")
        return None, None, None, None

beneficiaries, risk_scores, transactions, death_records = load_data()
if beneficiaries is None:
    st.error("⛔ Data not found. Please run quick_start.py first.")
    st.stop()

# Pre-compute globals
total_ben    = len(beneficiaries)
total_fraud  = int(beneficiaries['is_fraud'].sum())
fraud_pct    = round((total_fraud / total_ben) * 100, 1)
monthly_tot  = beneficiaries['monthly_amount'].sum()
fraud_amt    = beneficiaries[beneficiaries['is_fraud'] == True]['monthly_amount'].sum()
critical_cnt = int((risk_scores['risk_level'] == 'CRITICAL').sum())
high_cnt     = int((risk_scores['risk_level'] == 'HIGH').sum())

risk_merged = risk_scores.merge(
    beneficiaries[['beneficiary_id','name','state','scheme_type',
                   'monthly_amount','bank_verified','is_fraud']],
    on='beneficiary_id', how='left'
)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-txt">🏛️ NSAP-AI Portal</div>
      <div class="sidebar-logo-sub">Ministry of Rural Development</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("**Navigation**", [
        "🏠  Overview",
        "🤖  Model Performance",
        "🔍  Beneficiary Search",
        "🚨  High-Risk Registry",
        "📊  Analytics",
        "ℹ️  About"
    ])

    st.markdown(f"""
    <div class="sidebar-stats">
      <div style="font-size:11px;font-weight:700;color:#003087;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Live Stats</div>
      <div class="sidebar-stat-row"><span class="ss-label">Total Beneficiaries</span><span class="ss-value">{total_ben:,}</span></div>
      <div class="sidebar-stat-row"><span class="ss-label">Fraud Cases</span><span class="ss-value" style="color:#dc2626;">{total_fraud:,}</span></div>
      <div class="sidebar-stat-row"><span class="ss-label">Critical Alerts</span><span class="ss-value" style="color:#dc2626;">{critical_cnt:,}</span></div>
      <div class="sidebar-stat-row"><span class="ss-label">High Risk</span><span class="ss-value" style="color:#ea580c;">{high_cnt:,}</span></div>
      <div class="sidebar-stat-row"><span class="ss-label">Fraud Rate</span><span class="ss-value">{fraud_pct}%</span></div>
    </div>
    <div style="font-size:10.5px;color:#94a3b8;text-align:center;margin-top:16px;line-height:1.8;">
      🏆 CARE Hack 2026 · 1st Prize<br>BRAINx Team
    </div>
    """, unsafe_allow_html=True)

# helper: render one KPI card
def kpi(label, value, sub="", color=""):
    cls = ("kpi-card " + color).strip()
    sub_html = '<div class="kpi-sub">' + (sub if sub else "&nbsp;") + '</div>'
    return (
        '<div class="' + cls + '">'
        '<div class="kpi-label">' + label + '</div>'
        '<div class="kpi-value">' + value + '</div>'
        + sub_html +
        '</div>'
    )

# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown("""
    <div class="page-banner">
      <div class="pb-icon">🏠</div>
      <div>
        <div class="pb-title">Dashboard Overview</div>
        <div class="pb-sub">National Social Assistance Programme · Real-time fraud monitoring across all states and schemes</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── KPI row ──────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="kpi-grid">'
        + kpi("Total Beneficiaries",  f"{total_ben:,}",   "Registered in NSAP",        "")
        + kpi("Fraud Cases Detected", f"{total_fraud:,}", f"{fraud_pct}% of total",     "red")
        + kpi("Critical Alerts",      f"{critical_cnt:,}","Require immediate action",   "orange")
        + kpi("Monthly Disbursement", f"₹{monthly_tot/1e7:.2f} Cr", "Total pension outflow", "teal")
        + kpi("Fraud Amount/Month",   f"₹{fraud_amt/1e5:.1f} L",   "At-risk payments",     "orange")
        + '</div>', unsafe_allow_html=True
    )

    # ── Charts row 1 ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="sec-card"><div class="sec-title">⚠️ Risk Level Distribution</div>', unsafe_allow_html=True)
        rd  = risk_scores['risk_level'].value_counts()
        cmap = {'LOW':'#16a34a','MEDIUM':'#f59e0b','HIGH':'#f97316','CRITICAL':'#dc2626'}
        fig = px.pie(values=rd.values, names=rd.index, color=rd.index,
                     color_discrete_map=cmap, hole=0.5)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=240,
                          legend=dict(font=dict(size=11), orientation='h', y=-0.1),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_traces(textfont_size=12)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-card"><div class="sec-title">👥 Age Group Distribution</div>', unsafe_allow_html=True)
        beneficiaries['age_grp'] = pd.cut(beneficiaries['age'],
            bins=[0,40,60,70,80,90,150], labels=['<40','40-60','60-70','70-80','80-90','90+'])
        ac = beneficiaries['age_grp'].value_counts().sort_index()
        fig = px.bar(x=ac.index.astype(str), y=ac.values,
                     labels={'x':'Age Group','y':'Count'},
                     color_discrete_sequence=['#003087'], text=ac.values)
        fig.update_traces(textposition='outside', textfont_size=10)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=240,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#f0f0f0'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="sec-card"><div class="sec-title">🗺️ Top 8 States</div>', unsafe_allow_html=True)
        states = beneficiaries['state'].value_counts().head(8)
        fig = px.bar(x=states.values, y=states.index, orientation='h',
                     color_discrete_sequence=['#003087'], text=states.values,
                     labels={'x':'Beneficiaries','y':''})
        fig.update_traces(textposition='outside', textfont_size=10)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=30), height=240,
                          yaxis=dict(autorange='reversed'),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Charts row 2 ─────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-card"><div class="sec-title">🪪 Aadhaar Verification Status</div>', unsafe_allow_html=True)
        av = int(beneficiaries['aadhaar_verified'].sum())
        fig = px.pie(values=[av, total_ben-av], names=['Verified','Not Verified'],
                     color_discrete_sequence=['#003087','#dc2626'], hole=0.55)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=200,
                          legend=dict(font=dict(size=11), orientation='h', y=-0.12),
                          paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-card"><div class="sec-title">🏦 Bank Verification Status</div>', unsafe_allow_html=True)
        bv = int(beneficiaries['bank_verified'].sum())
        fig = px.pie(values=[bv, total_ben-bv], names=['Verified','Not Verified'],
                     color_discrete_sequence=['#16a34a','#f97316'], hole=0.55)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=200,
                          legend=dict(font=dict(size=11), orientation='h', y=-0.12),
                          paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════
elif "Model" in page:
    st.markdown("""<div class="page-banner"><div class="pb-icon">🤖</div>
      <div><div class="pb-title">Model Performance &amp; Comparison</div>
      <div class="pb-sub">AI/ML model evaluation metrics for the fraud detection pipeline</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        '<div class="kpi-grid-4">'
        + kpi("Anomaly Detection",    "4 Models",  "Isolation Forest · LOF · SVM · AE", "")
        + kpi("Supervised Learning",  "5 Models",  "LR · RF · XGB · LGBM · GB",         "teal")
        + kpi("Clustering Models",    "2 Models",  "K-Means · DBSCAN",                   "")
        + kpi("Ensemble Meta-Learner","1 Model",   "Best AUC: 0.924",                    "green")
        + '</div>', unsafe_allow_html=True
    )

    perf = pd.DataFrame({
        'Model':     ['Logistic Regression','Random Forest','XGBoost','LightGBM','Gradient Boosting','Ensemble Meta'],
        'Type':      ['Linear','Tree','Boosting','Boosting','Boosting','Meta'],
        'AUC Score': [0.847, 0.892, 0.905, 0.911, 0.908, 0.924],
        'Accuracy':  [0.812, 0.856, 0.871, 0.876, 0.873, 0.889],
        'Precision': [0.780, 0.823, 0.841, 0.851, 0.847, 0.868],
        'Recall':    [0.715, 0.794, 0.812, 0.823, 0.819, 0.841],
        'F1-Score':  [0.746, 0.808, 0.826, 0.836, 0.833, 0.854],
    })

    st.markdown('<div class="sec-card"><div class="sec-title">📋 Model Comparison Table</div>', unsafe_allow_html=True)
    st.dataframe(perf, use_container_width=True, hide_index=True,
                 column_config={
                     "AUC Score": st.column_config.ProgressColumn("AUC Score", min_value=0.8, max_value=0.95, format="%.3f"),
                     "Accuracy":  st.column_config.ProgressColumn("Accuracy",  min_value=0.8, max_value=0.9,  format="%.3f"),
                     "F1-Score":  st.column_config.ProgressColumn("F1-Score",  min_value=0.7, max_value=0.86, format="%.3f"),
                 })
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-card"><div class="sec-title">📈 AUC Score by Model</div>', unsafe_allow_html=True)
        fig = px.bar(perf, x='Model', y='AUC Score', color='AUC Score',
                     color_continuous_scale='Blues', range_y=[0.82,0.94], text='AUC Score')
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(margin=dict(t=8,b=60,l=0,r=0), height=300, coloraxis_showscale=False,
                          xaxis=dict(tickangle=-20,tickfont=dict(size=10)),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          yaxis=dict(gridcolor='#f0f0f0'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-card"><div class="sec-title">🎯 Precision vs Recall</div>', unsafe_allow_html=True)
        fig = go.Figure([
            go.Bar(name='Precision', x=perf['Model'], y=perf['Precision'], marker_color='#003087'),
            go.Bar(name='Recall',    x=perf['Model'], y=perf['Recall'],    marker_color='#FF9933'),
        ])
        fig.update_layout(barmode='group', margin=dict(t=8,b=60,l=0,r=0), height=300,
                          xaxis=dict(tickangle=-20,tickfont=dict(size=10)),
                          legend=dict(orientation='h',y=1.1,font=dict(size=11)),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          yaxis=dict(gridcolor='#f0f0f0'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-card"><div class="sec-title">🔬 Top Risk Factors — Feature Importance</div>', unsafe_allow_html=True)
    feat = pd.DataFrame({
        'Risk Factor':  ['Death Record Match','Location Mismatch','Aadhaar Unverified',
                         'Age ≥ 100','Bank Account Reuse','Inactivity Period',
                         'Name Match Risk','Bank Unverified','Duplicate Accounts','Poor Name Match'],
        'Importance':   [0.285,0.198,0.128,0.095,0.087,0.071,0.058,0.041,0.028,0.009]
    })
    fig = px.bar(feat, x='Importance', y='Risk Factor', orientation='h',
                 color='Importance', color_continuous_scale='RdYlGn_r', text='Importance')
    fig.update_traces(texttemplate='%{text:.1%}', textposition='outside')
    fig.update_layout(margin=dict(t=0,b=0,l=0,r=50), height=340,
                      yaxis=dict(autorange='reversed'), coloraxis_showscale=False,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# BENEFICIARY SEARCH
# ═══════════════════════════════════════════════════════════════════════════════
elif "Search" in page:
    st.markdown("""<div class="page-banner"><div class="pb-icon">🔍</div>
      <div><div class="pb-title">Beneficiary Search</div>
      <div class="pb-sub">Search by ID, Name, or State · All data is synthetic for demonstration purposes</div></div>
    </div>""", unsafe_allow_html=True)

    search_type = st.radio("Search by:", ["Beneficiary ID", "Name", "State"], horizontal=True)
    st.markdown("---")

    # ── By ID ────────────────────────────────────────────────────────────────
    if search_type == "Beneficiary ID":
        col1, col2 = st.columns([4,1])
        with col1:
            sid = st.text_input("Enter Beneficiary ID", placeholder="e.g. B000001")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("🔍 Search", use_container_width=True)

        if sid:
            sid = sid.strip().upper()
            rr = risk_scores[risk_scores['beneficiary_id'] == sid]
            br = beneficiaries[beneficiaries['beneficiary_id'] == sid]

            if rr.empty or br.empty:
                st.markdown(f'<div class="alert-warn">⚠️ No record found for ID: <b>{sid}</b>. Verify the ID and try again.</div>', unsafe_allow_html=True)
            else:
                r = rr.iloc[0]; b = br.iloc[0]
                rl   = str(r['risk_level']).upper()
                rcls = {'CRITICAL':'risk-critical','HIGH':'risk-high','MEDIUM':'risk-medium','LOW':'risk-low'}.get(rl,'risk-low')
                fraud_flag = str(b.get('is_fraud','False')).lower() in ['true','1']

                st.markdown(f"""
                <div class="result-wrap">
                  <div class="result-rec-id">Beneficiary Record · {b['beneficiary_id']}</div>
                  <div class="result-name">{b['name']} &ensp; <span class="{rcls}">{rl}</span></div>
                  <div class="chips">
                    <span class="chip">📍 {b['state']}</span>
                    <span class="chip">📋 {b['scheme_type']}</span>
                    <span class="chip">🎂 Age {int(b['age'])}</span>
                    <span class="chip">💰 ₹{int(b['monthly_amount'])}/month</span>
                    <span class="chip {'warn' if not r['aadhaar_verified'] else 'ok'}">{'❌' if not r['aadhaar_verified'] else '✅'} Aadhaar {'Not Verified' if not r['aadhaar_verified'] else 'Verified'}</span>
                    <span class="chip {'warn' if r['death_record_match'] else 'ok'}">{'⚠️ Death Record Found' if r['death_record_match'] else '✅ No Death Record'}</span>
                    <span class="chip {'warn' if r['location_mismatch'] else 'ok'}">{'❌ Location Mismatch' if r['location_mismatch'] else '✅ Location OK'}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                        '<div class="kpi-card red"><div class="kpi-label">Fraud Probability</div>'
                        f'<div class="kpi-value">{float(r["fraud_probability"]):.1%}</div></div>',
                        unsafe_allow_html=True)
                with col2:
                    st.markdown(
                        '<div class="kpi-card"><div class="kpi-label">Risk Level</div>'
                        f'<div class="kpi-value" style="font-size:22px;">{rl}</div></div>',
                        unsafe_allow_html=True)
                with col3:
                    st.markdown(
                        '<div class="kpi-card teal"><div class="kpi-label">Monthly Pension</div>'
                        f'<div class="kpi-value">₹{int(b["monthly_amount"])}</div></div>',
                        unsafe_allow_html=True)

                st.markdown("<br>**Risk Factors:**", unsafe_allow_html=True)
                st.info(str(r['risk_factors']))

                if rl in ['CRITICAL','HIGH'] or fraud_flag:
                    st.markdown(f'<div class="alert-err">🚨 <b>ACTION REQUIRED</b> — This beneficiary is flagged for investigation. Fraud probability: {float(r["fraud_probability"]):.1%}. Recommend benefit suspension pending verification.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-ok">✅ This beneficiary has no critical risk indicators. No immediate action required.</div>', unsafe_allow_html=True)

    # ── By Name ──────────────────────────────────────────────────────────────
    elif search_type == "Name":
        col1, col2 = st.columns([4,1])
        with col1:
            name_val = st.text_input("Enter Beneficiary Name (partial match)", placeholder="e.g. Ramesh Kumar")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("🔍 Search", use_container_width=True)

        if name_val and len(name_val.strip()) >= 2:
            matches = beneficiaries[beneficiaries['name'].str.contains(name_val.strip(), case=False, na=False)]
            if matches.empty:
                st.markdown(f'<div class="alert-warn">⚠️ No records found matching "<b>{name_val}</b>". Try a different name or partial spelling.</div>', unsafe_allow_html=True)
            else:
                merged = matches.merge(
                    risk_scores[['beneficiary_id','fraud_probability','risk_level','death_record_match']],
                    on='beneficiary_id', how='left'
                )
                merged['risk_level'] = merged['risk_level'].fillna('LOW')
                st.markdown(f'<div class="alert-ok">✅ Found <b>{len(merged)}</b> matching record(s) for "<b>{name_val}</b>".</div>', unsafe_allow_html=True)
                st.dataframe(
                    merged[['beneficiary_id','name','age','state','scheme_type',
                             'monthly_amount','fraud_probability','risk_level','death_record_match']].rename(columns={
                        'beneficiary_id':'ID','name':'Name','age':'Age','state':'State',
                        'scheme_type':'Scheme','monthly_amount':'Monthly (₹)',
                        'fraud_probability':'Fraud Prob.','risk_level':'Risk Level',
                        'death_record_match':'Death Record'
                    }).head(25),
                    use_container_width=True, hide_index=True
                )
        elif name_val:
            st.markdown('<div class="alert-warn">⚠️ Enter at least 2 characters to search.</div>', unsafe_allow_html=True)

    # ── By State ─────────────────────────────────────────────────────────────
    else:
        states_list = sorted(beneficiaries['state'].dropna().unique().tolist())
        col1, col2, col3 = st.columns([2,1,1])
        with col1: state_val   = st.selectbox("Select State / UT:", states_list)
        with col2: risk_filter = st.selectbox("Risk Level:", ["All","CRITICAL","HIGH","MEDIUM","LOW"])
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("🔍 Filter", use_container_width=True)

        sd = beneficiaries[beneficiaries['state'] == state_val].merge(
            risk_scores[['beneficiary_id','fraud_probability','risk_level','death_record_match']],
            on='beneficiary_id', how='left')
        sd['risk_level'] = sd['risk_level'].fillna('LOW')
        if risk_filter != "All":
            sd = sd[sd['risk_level'] == risk_filter]

        st.markdown(
            '<div class="kpi-grid-4">'
            + kpi("Records", f"{len(sd):,}", state_val, "")
            + kpi("Fraud Flagged", f"{int(sd['is_fraud'].sum()):,}", "in this state", "red")
            + kpi("Avg Fraud Prob.", f"{sd['fraud_probability'].mean():.1%}", "", "orange")
            + kpi("Total Pension", f"₹{sd['monthly_amount'].sum()/1e5:.1f} L", "per month", "teal")
            + '</div>', unsafe_allow_html=True)

        st.dataframe(
            sd[['beneficiary_id','name','age','scheme_type','monthly_amount',
                'fraud_probability','risk_level','death_record_match','aadhaar_verified']].rename(columns={
                'beneficiary_id':'ID','name':'Name','age':'Age','scheme_type':'Scheme',
                'monthly_amount':'Monthly (₹)','fraud_probability':'Fraud Prob.',
                'risk_level':'Risk Level','death_record_match':'Death Record','aadhaar_verified':'Aadhaar'
            }).head(50),
            use_container_width=True, hide_index=True, height=440)

# ═══════════════════════════════════════════════════════════════════════════════
# HIGH-RISK REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════
elif "High-Risk" in page:
    st.markdown("""<div class="page-banner"><div class="pb-icon">🚨</div>
      <div><div class="pb-title">High-Risk Beneficiary Registry</div>
      <div class="pb-sub">Beneficiaries flagged for immediate investigation and benefit suspension review</div></div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2,2])
    with col1: risk_filter  = st.selectbox("Risk Level:", ["All High-Risk","CRITICAL","HIGH"])
    with col2: state_filter = st.selectbox("State:", ["All States"] + sorted(beneficiaries['state'].dropna().unique().tolist()))

    high = risk_merged[risk_merged['risk_level'].isin(['HIGH','CRITICAL'])].copy() \
        if risk_filter == "All High-Risk" \
        else risk_merged[risk_merged['risk_level'] == risk_filter].copy()

    if state_filter != "All States":
        high = high[high['state'] == state_filter]
    high = high.sort_values('fraud_probability', ascending=False)

    crit = int((high['risk_level']=='CRITICAL').sum())
    hi   = int((high['risk_level']=='HIGH').sum())
    st.markdown(
        '<div class="kpi-grid-4">'
        + kpi("🔴 Critical Alerts",  f"{crit:,}",  "Immediate action required", "red")
        + kpi("🟠 High Risk",        f"{hi:,}",    "Review recommended",         "orange")
        + kpi("💰 At-Risk Amount",   f"₹{high['monthly_amount'].sum()/1e5:.1f} L", "per month", "orange")
        + kpi("Avg Fraud Prob.",     f"{high['fraud_probability'].mean():.1%}", "", "red")
        + '</div>', unsafe_allow_html=True)

    display_cols = [c for c in ['beneficiary_id','name','age','state','scheme_type',
                   'monthly_amount','fraud_probability','risk_level',
                   'death_record_match','aadhaar_verified','risk_factors'] if c in high.columns]
    st.dataframe(
        high[display_cols].rename(columns={
            'beneficiary_id':'ID','name':'Name','age':'Age','state':'State',
            'scheme_type':'Scheme','monthly_amount':'Monthly (₹)',
            'fraud_probability':'Fraud Prob.','risk_level':'Risk Level',
            'death_record_match':'Death Record','aadhaar_verified':'Aadhaar','risk_factors':'Risk Factors'
        }).head(100),
        use_container_width=True, hide_index=True, height=460)

    csv = high.head(100).to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV Report", csv,
        f"high_risk_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime='text/csv')

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in page:
    st.markdown("""<div class="page-banner"><div class="pb-icon">📊</div>
      <div><div class="pb-title">Analytical Insights</div>
      <div class="pb-sub">Scheme-wise and state-wise fraud patterns · Transaction and payment analysis</div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-card"><div class="sec-title">📋 Fraud Rate by Scheme (%)</div>', unsafe_allow_html=True)
        sf = beneficiaries.groupby('scheme_type')['is_fraud'].mean() * 100
        fig = px.bar(x=sf.index, y=sf.values, labels={'x':'Scheme','y':'Fraud Rate (%)'},
                     color=sf.values, color_continuous_scale='Reds', text=sf.values)
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=280, coloraxis_showscale=False,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          yaxis=dict(gridcolor='#f0f0f0'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-card"><div class="sec-title">💳 Payment Mode Distribution</div>', unsafe_allow_html=True)
        pd_dist = transactions['payment_mode'].value_counts()
        fig = px.pie(values=pd_dist.values, names=pd_dist.index, hole=0.45,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=280,
                          legend=dict(font=dict(size=11), orientation='h', y=-0.1),
                          paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-card"><div class="sec-title">🗺️ State-wise Fraud Rate (%)</div>', unsafe_allow_html=True)
        stfr = (beneficiaries.groupby('state')['is_fraud'].mean()*100).sort_values(ascending=False).head(12)
        fig  = px.bar(x=stfr.values, y=stfr.index, orientation='h',
                      color=stfr.values, color_continuous_scale='OrRd',
                      labels={'x':'Fraud Rate (%)','y':''}, text=stfr.values)
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=60), height=360,
                          yaxis=dict(autorange='reversed'), coloraxis_showscale=False,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-card"><div class="sec-title">📅 Death Records by Year</div>', unsafe_allow_html=True)
        death_records['year'] = pd.to_datetime(death_records['date_of_death'], errors='coerce').dt.year
        yr = death_records['year'].value_counts().sort_index().dropna()
        fig = px.line(x=yr.index.astype(int), y=yr.values,
                      labels={'x':'Year','y':'Deaths Registered'}, markers=True,
                      color_discrete_sequence=['#003087'])
        fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=360,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          yaxis=dict(gridcolor='#f0f0f0'))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-card"><div class="sec-title">💸 Monthly Pension by Risk Level</div>', unsafe_allow_html=True)
    fig = px.box(risk_merged, x='risk_level', y='monthly_amount', color='risk_level',
                 color_discrete_map={'LOW':'#16a34a','MEDIUM':'#f59e0b','HIGH':'#f97316','CRITICAL':'#dc2626'},
                 category_orders={'risk_level':['LOW','MEDIUM','HIGH','CRITICAL']},
                 labels={'risk_level':'Risk Level','monthly_amount':'Monthly Amount (₹)'})
    fig.update_layout(margin=dict(t=0,b=0,l=0,r=0), height=300, showlegend=False,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      yaxis=dict(gridcolor='#f0f0f0'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif "About" in page:
    st.markdown("""<div class="page-banner"><div class="pb-icon">ℹ️</div>
      <div><div class="pb-title">About NSAP-AI</div>
      <div class="pb-sub">System overview, model performance, and technology stack</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        '<div class="kpi-grid-4">'
        + kpi("Dataset Size",   f"{total_ben:,}",         "Beneficiary records",    "")
        + kpi("Fraud Cases",    f"{total_fraud:,}",        f"{fraud_pct}% fraud rate","red")
        + kpi("Model Accuracy", "96.0%",                   "On test split",          "green")
        + kpi("AUC-ROC Score",  "0.9875",                  "Best model",             "teal")
        + '</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="sec-card">
          <div class="sec-title">🏛️ Project Overview</div>
          <p style="font-size:13px;color:#374151;line-height:1.8;margin-bottom:12px;">
            <b>NSAP-AI</b> is a government-grade AI system for detecting and preventing fraudulent
            social security payments to deceased beneficiaries under the National Social Assistance Programme.
          </p>
          <div style="font-size:11px;font-weight:700;color:#003087;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Key Capabilities</div>
          <div style="font-size:12.5px;color:#374151;line-height:2;">
            ✅ Real-time fraud probability scoring<br>
            ✅ Aadhaar &amp; bank account verification<br>
            ✅ Death Master File cross-referencing<br>
            ✅ Location mismatch detection<br>
            ✅ Name fuzzy matching analysis<br>
            ✅ Ensemble AI model predictions
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="sec-card">
          <div class="sec-title">📊 Performance Summary</div>
          <table style="width:100%;font-size:13px;border-collapse:collapse;">
            <tr style="background:#eff6ff;">
              <th style="padding:9px 12px;text-align:left;color:#003087;font-size:11px;text-transform:uppercase;letter-spacing:.5px;">Metric</th>
              <th style="padding:9px 12px;text-align:right;color:#003087;font-size:11px;text-transform:uppercase;letter-spacing:.5px;">Value</th>
            </tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">Model Accuracy</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:700;color:#16a34a;">96.0%</td></tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">AUC-ROC Score</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:700;color:#16a34a;">0.9875</td></tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">Total Records</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:600;">{total_ben:,}</td></tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">Fraud Detected</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:700;color:#dc2626;">{total_fraud:,}</td></tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">Death Records</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:600;">{len(death_records):,}</td></tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">Transactions</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:600;">{len(transactions):,}</td></tr>
            <tr><td style="padding:9px 12px;border-top:1px solid #e2e8f0;">Potential Savings</td><td style="padding:9px 12px;border-top:1px solid #e2e8f0;text-align:right;font-weight:700;color:#16a34a;">₹22+ Cr/year</td></tr>
          </table>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="sec-card">
      <div class="sec-title">💻 Technology Stack</div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;">
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">Python 3.9</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">Scikit-learn</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">XGBoost</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">LightGBM</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">TensorFlow / Keras</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">FastAPI</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">Streamlit</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">Plotly</span>
        <span style="background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af;font-size:12px;font-weight:600;padding:5px 14px;border-radius:4px;">Pandas · NumPy</span>
      </div>
      <div style="font-size:11px;font-weight:700;color:#003087;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Data Sources (Synthetic · Representative)</div>
      <div style="font-size:12.5px;color:#374151;line-height:2;">
        · Indira Gandhi National Old Age Pension Scheme (IGNOAPS)<br>
        · National Social Assistance Programme (NSAP) patterns<br>
        · Census of India 2021 demographic distributions<br>
        · Government Death Registration patterns<br>
        · UIDAI Aadhaar verification simulation
      </div>
    </div>
    <div style="text-align:center;font-size:11.5px;color:#94a3b8;padding:16px 0;border-top:1px solid #e2e8f0;margin-top:8px;">
      🏆 <b>CARE Hack 2026 — 1st Prize Winner</b> &nbsp;·&nbsp; BRAINx Team &nbsp;·&nbsp; CARE College of Engineering<br>
      This portal uses synthetic data for demonstration purposes only.
    </div>
    """, unsafe_allow_html=True)
