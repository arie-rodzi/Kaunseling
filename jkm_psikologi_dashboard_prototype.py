
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# JKM PSYCHOLOGICAL SERVICE INTELLIGENCE PLATFORM - PREMIUM V2
# Early Analytical Prototype with Simulated Data
# ============================================================

st.set_page_config(
    page_title="JKM Psychological Service Intelligence Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM CSS
# ============================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(255,75,75,0.12), transparent 30%),
        radial-gradient(circle at top right, rgba(0,86,179,0.12), transparent 30%),
        linear-gradient(135deg, #f7fbff 0%, #eef5ff 45%, #fff8ec 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071b33 0%, #0b2c55 55%, #031020 100%);
}

[data-testid="stSidebar"] * {
    color: white;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(135deg, #071b33, #003566, #ff4b4b);
    padding: 32px;
    border-radius: 30px;
    color: white;
    box-shadow: 0 20px 45px rgba(0,0,0,0.18);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 17px;
    opacity: 0.92;
    max-width: 1100px;
}

.pill {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    padding: 7px 14px;
    border-radius: 999px;
    margin-right: 8px;
    font-size: 13px;
}

.kpi-card {
    background: rgba(255,255,255,0.96);
    padding: 22px;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.4);
    min-height: 155px;
}

.kpi-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 650;
}

.kpi-value {
    font-size: 34px;
    font-weight: 900;
    color: #071b33;
    margin-top: 4px;
}

.kpi-note-green {
    font-size: 13px;
    color: #15803d;
    font-weight: 700;
}

.kpi-note-red {
    font-size: 13px;
    color: #b91c1c;
    font-weight: 700;
}

.kpi-note-blue {
    font-size: 13px;
    color: #1d4ed8;
    font-weight: 700;
}

.card {
    background: rgba(255,255,255,0.96);
    padding: 24px;
    border-radius: 26px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.075);
    margin-bottom: 18px;
    border: 1px solid rgba(0,0,0,0.03);
}

.dark-card {
    background: linear-gradient(135deg, #071b33, #003566);
    color: white;
    padding: 26px;
    border-radius: 26px;
    box-shadow: 0 14px 35px rgba(0,0,0,0.16);
    margin-bottom: 18px;
}

.red-card {
    background: linear-gradient(135deg, #b91c1c, #ff4b4b);
    color: white;
    padding: 24px;
    border-radius: 26px;
    box-shadow: 0 14px 35px rgba(185,28,28,0.20);
    margin-bottom: 18px;
}

.gold-card {
    background: linear-gradient(135deg, #fff7d6, #ffffff);
    padding: 22px;
    border-radius: 24px;
    border-left: 7px solid #f0b429;
    box-shadow: 0 10px 28px rgba(0,0,0,0.07);
    margin-bottom: 18px;
}

.green-card {
    background: linear-gradient(135deg, #dcfce7, #ffffff);
    padding: 22px;
    border-radius: 24px;
    border-left: 7px solid #22c55e;
    box-shadow: 0 10px 28px rgba(0,0,0,0.07);
    margin-bottom: 18px;
}

.section-title {
    font-size: 26px;
    font-weight: 900;
    color: #071b33;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 15px;
}

.mini-title {
    font-size: 18px;
    font-weight: 850;
    color: #071b33;
}

.small-muted {
    color: #6b7280;
    font-size: 13px;
}

.status-high {
    color: #b91c1c;
    font-weight: 800;
}

.status-mid {
    color: #b45309;
    font-weight: 800;
}

.status-low {
    color: #15803d;
    font-weight: 800;
}

.footer-note {
    text-align: center;
    color: #6b7280;
    padding: 25px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA GENERATION
# ============================================================
@st.cache_data
def generate_data(seed=2026):
    rng = np.random.default_rng(seed)

    states = [
        "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
        "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah",
        "Sarawak", "Selangor", "Terengganu", "W.P. Kuala Lumpur"
    ]

    regions = {
        "Johor": "Selatan", "Kedah": "Utara", "Kelantan": "Pantai Timur",
        "Melaka": "Selatan", "Negeri Sembilan": "Selatan", "Pahang": "Pantai Timur",
        "Perak": "Utara", "Perlis": "Utara", "Pulau Pinang": "Utara",
        "Sabah": "Borneo", "Sarawak": "Borneo", "Selangor": "Tengah",
        "Terengganu": "Pantai Timur", "W.P. Kuala Lumpur": "Tengah"
    }

    services = [
        "Kaunseling Individu",
        "Kaunseling Keluarga",
        "Intervensi Krisis",
        "Sokongan Trauma",
        "Bimbingan Psikososial",
        "Program Pemulihan",
        "Intervensi Kanak-Kanak",
        "Sokongan Warga Emas"
    ]

    client_groups = [
        "Kanak-kanak", "Remaja", "Dewasa", "Warga Emas",
        "Keluarga", "Mangsa Krisis", "Penjaga", "OKU"
    ]

    months = pd.date_range("2025-01-01", periods=18, freq="M")
    month_labels = months.strftime("%b %Y")

    state_rows = []
    for s in states:
        base_case = rng.integers(360, 1650)
        access = rng.uniform(68, 94)
        responsiveness = rng.uniform(66, 95)
        intervention = rng.uniform(70, 96)
        emotional = rng.uniform(64, 92)
        followup = rng.uniform(55, 90)
        satisfaction = rng.uniform(70, 96)
        psei = 0.18*access + 0.18*responsiveness + 0.20*intervention + 0.20*emotional + 0.12*followup + 0.12*satisfaction
        state_rows.append({
            "Negeri": s,
            "Zon": regions[s],
            "Jumlah Kes": int(base_case),
            "Akses": round(access, 1),
            "Responsif": round(responsiveness, 1),
            "Kualiti Intervensi": round(intervention, 1),
            "Hasil Emosi": round(emotional, 1),
            "Susulan": round(followup, 1),
            "Kepuasan": round(satisfaction, 1),
            "PSEI": round(psei, 1),
            "Kes Risiko Tinggi": int(base_case * rng.uniform(0.08, 0.22)),
            "Purata Masa Menunggu (hari)": round(rng.uniform(3, 18), 1),
            "Kadar Penyelesaian (%)": round(rng.uniform(62, 92), 1),
            "Pegawai Aktif": int(rng.integers(8, 55)),
            "Sesi Susulan": int(rng.integers(160, 2100))
        })
    df_state = pd.DataFrame(state_rows)

    service_rows = []
    for svc in services:
        case = rng.integers(550, 2800)
        service_rows.append({
            "Jenis Perkhidmatan": svc,
            "Kes Dikendalikan": int(case),
            "Keberkesanan (%)": round(rng.uniform(68, 95), 1),
            "Kepuasan (%)": round(rng.uniform(70, 97), 1),
            "Kadar Penyelesaian (%)": round(rng.uniform(60, 92), 1),
            "Kes Risiko Tinggi": int(case * rng.uniform(0.07, 0.24)),
            "Kos Anggaran per Kes (RM)": int(rng.integers(120, 520)),
            "Sesi Purata": round(rng.uniform(2.1, 7.8), 1)
        })
    df_service = pd.DataFrame(service_rows)

    trend_rows = []
    for i, m in enumerate(month_labels):
        seasonal = 90*np.sin(i/2.5)
        new_cases = int(1150 + seasonal + rng.normal(0, 130))
        solved = int(new_cases * rng.uniform(0.72, 0.93))
        high_risk = int(new_cases * rng.uniform(0.09, 0.20))
        trend_rows.append({
            "Bulan": m,
            "Kes Baharu": max(650, new_cases),
            "Kes Selesai": max(500, solved),
            "Kes Risiko Tinggi": high_risk,
            "PSEI": round(rng.uniform(73, 88) + i*0.18, 1),
            "Kepuasan": round(rng.uniform(74, 91), 1),
            "Masa Menunggu": round(rng.uniform(5, 15), 1)
        })
    df_trend = pd.DataFrame(trend_rows)

    case_rows = []
    risk_levels = ["Rendah", "Sederhana", "Tinggi", "Kritikal"]
    statuses = ["Baru", "Saringan", "Dalam Intervensi", "Perlu Susulan", "Rujukan Lanjut", "Selesai"]
    for i in range(1, 251):
        risk = rng.choice(risk_levels, p=[0.38, 0.34, 0.20, 0.08])
        progress = int(rng.integers(10, 100))
        if risk == "Kritikal":
            risk_score = int(rng.integers(82, 99))
        elif risk == "Tinggi":
            risk_score = int(rng.integers(65, 86))
        elif risk == "Sederhana":
            risk_score = int(rng.integers(40, 68))
        else:
            risk_score = int(rng.integers(10, 42))
        case_rows.append({
            "ID Kes": f"JKM-{2026}-{i:04d}",
            "Negeri": rng.choice(states),
            "Zon": None,
            "Jenis Perkhidmatan": rng.choice(services),
            "Kumpulan Sasar": rng.choice(client_groups),
            "Tahap Risiko": risk,
            "Risk Score": risk_score,
            "Status": rng.choice(statuses),
            "Progress (%)": progress,
            "Hari Dalam Proses": int(rng.integers(1, 120)),
            "Keutamaan": "Segera" if risk in ["Tinggi", "Kritikal"] else "Normal",
            "Pegawai Kes": f"Pegawai {rng.integers(1, 38)}"
        })
    df_case = pd.DataFrame(case_rows)
    df_case["Zon"] = df_case["Negeri"].map(regions)

    survey_rows = []
    constructs = ["Akses", "Responsif", "Kualiti Intervensi", "Hasil Emosi", "Susulan", "Kepuasan"]
    for construct in constructs:
        for item in range(1, 7):
            survey_rows.append({
                "Konstruk": construct,
                "Item": f"{construct[:3].upper()}-{item}",
                "Min": round(rng.uniform(3.55, 4.55), 2),
                "SD": round(rng.uniform(0.45, 0.95), 2),
                "Loading": round(rng.uniform(0.62, 0.91), 2),
                "Alpha if Deleted": round(rng.uniform(0.78, 0.93), 2)
            })
    df_survey = pd.DataFrame(survey_rows)

    qual_rows = pd.DataFrame({
        "Tema": [
            "Akses kepada perkhidmatan",
            "Keperluan susulan selepas sesi",
            "Beban tugas pegawai",
            "Sokongan digital",
            "Intervensi krisis",
            "Keperluan latihan berterusan",
            "Standardisasi modul",
            "Rujukan antara agensi"
        ],
        "Bilangan Petikan": rng.integers(18, 86, 8),
        "Sentimen Positif (%)": rng.uniform(45, 88, 8).round(1),
        "Keutamaan": rng.choice(["Sangat Tinggi", "Tinggi", "Sederhana"], 8, p=[0.35,0.45,0.20])
    })

    return df_state, df_service, df_trend, df_case, df_survey, qual_rows, states, services, client_groups

df_state, df_service, df_trend, df_case, df_survey, df_qual, states, services, client_groups = generate_data()

# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def kpi_card(label, value, note, note_type="green"):
    cls = {"green": "kpi-note-green", "red": "kpi-note-red", "blue": "kpi-note-blue"}.get(note_type, "kpi-note-green")
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="{cls}">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def interpret_score(score):
    if score >= 85:
        return "Cemerlang"
    if score >= 75:
        return "Baik"
    if score >= 65:
        return "Sederhana"
    return "Perlu Penambahbaikan"

def risk_color(score):
    if score >= 80:
        return "Kritikal"
    if score >= 60:
        return "Tinggi"
    if score >= 40:
        return "Sederhana"
    return "Rendah"

def generate_ai_insights(state_df, service_df, case_df):
    insights = []
    low_follow = state_df.sort_values("Susulan").head(3)
    high_wait = state_df.sort_values("Purata Masa Menunggu (hari)", ascending=False).head(3)
    high_risk_states = state_df.sort_values("Kes Risiko Tinggi", ascending=False).head(3)
    best_service = service_df.sort_values("Keberkesanan (%)", ascending=False).iloc[0]
    weak_service = service_df.sort_values("Keberkesanan (%)").iloc[0]
    critical_count = len(case_df[case_df["Tahap Risiko"] == "Kritikal"])

    insights.append(f"Negeri dengan kesinambungan susulan paling rendah ialah {', '.join(low_follow['Negeri'].tolist())}. Cadangan: tambah sistem reminder dan jadual follow-up digital.")
    insights.append(f"Masa menunggu tertinggi dikesan di {', '.join(high_wait['Negeri'].tolist())}. Cadangan: tetapkan service-level benchmark dan mekanisme redistribusi kes.")
    insights.append(f"Kes risiko tinggi tertumpu di {', '.join(high_risk_states['Negeri'].tolist())}. Cadangan: wujudkan triage psikososial dan panel rujukan pantas.")
    insights.append(f"Perkhidmatan paling berkesan dalam simulasi ialah {best_service['Jenis Perkhidmatan']} ({best_service['Keberkesanan (%)']}%). Ini boleh dijadikan model amalan terbaik.")
    insights.append(f"Perkhidmatan yang memerlukan penambahbaikan ialah {weak_service['Jenis Perkhidmatan']} ({weak_service['Keberkesanan (%)']}%). Cadangan: semak modul, latihan dan SOP intervensi.")
    insights.append(f"Terdapat {critical_count} kes kritikal dalam paparan semasa. Kes ini memerlukan pemantauan intensif dan escalation workflow.")
    return insights

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🧠 JKM Intelligence")
    st.caption("Psychological Service Effectiveness Analytics")
    st.markdown("---")

    selected_states = st.multiselect("Negeri", states, default=states)
    selected_services = st.multiselect("Jenis Perkhidmatan", services, default=services)
    selected_groups = st.multiselect("Kumpulan Sasar", client_groups, default=client_groups)

    st.markdown("---")
    target_psei = st.slider("Sasaran PSEI Nasional", 60, 95, 82)
    alert_threshold = st.slider("Ambang Risk Score Kritikal", 60, 95, 80)

    st.markdown("---")
    st.markdown("### Prototype Status")
    st.success("Simulated Data Active")
    st.info("Version: Premium V2")
    st.caption(f"Last refresh: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

# Apply filters
df_state_f = df_state[df_state["Negeri"].isin(selected_states)]
df_service_f = df_service[df_service["Jenis Perkhidmatan"].isin(selected_services)]
df_case_f = df_case[
    df_case["Negeri"].isin(selected_states)
    & df_case["Jenis Perkhidmatan"].isin(selected_services)
    & df_case["Kumpulan Sasar"].isin(selected_groups)
]

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">Integrated Psychological Service Intelligence Platform</div>
    <div class="hero-subtitle">
        Premium analytical prototype for evaluating effectiveness, monitoring risks, generating policy intelligence,
        and supporting evidence-based improvement of JKM psychological and counselling services.
    </div>
    <br>
    <span class="pill">National Monitoring</span>
    <span class="pill">Effectiveness Index</span>
    <span class="pill">Risk Triage</span>
    <span class="pill">Policy Intelligence</span>
    <span class="pill">Survey Analytics</span>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([
    "📊 Executive Command Centre",
    "🗺️ State & Service Analytics",
    "🧮 Effectiveness Index",
    "🚨 Risk & Case Monitoring",
    "📋 Survey & Instrument Analytics",
    "🔮 Forecasting & Simulation",
    "🎯 Policy Recommendation Engine",
    "📦 Deliverables"
])

# ============================================================
# TAB 1: EXECUTIVE COMMAND CENTRE
# ============================================================
with tabs[0]:
    section_header("Executive Command Centre", "National-level simulated overview of service performance, risk and intervention outcomes.")

    total_cases = int(df_state_f["Jumlah Kes"].sum())
    avg_psei = df_state_f["PSEI"].mean()
    avg_satisfaction = df_state_f["Kepuasan"].mean()
    high_risk = int(df_state_f["Kes Risiko Tinggi"].sum())
    waiting = df_state_f["Purata Masa Menunggu (hari)"].mean()
    completion = df_state_f["Kadar Penyelesaian (%)"].mean()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        kpi_card("Total Cases", f"{total_cases:,}", "+12.4% simulated growth", "green")
    with c2:
        kpi_card("National PSEI", f"{avg_psei:.1f}%", interpret_score(avg_psei), "blue")
    with c3:
        kpi_card("Satisfaction", f"{avg_satisfaction:.1f}%", "Positive service experience", "green")
    with c4:
        kpi_card("High Risk Cases", f"{high_risk:,}", "Requires triage monitoring", "red")
    with c5:
        kpi_card("Avg Waiting", f"{waiting:.1f} days", "Service access indicator", "blue")
    with c6:
        kpi_card("Completion", f"{completion:.1f}%", "Case closure performance", "green")

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="mini-title">Monthly National Trend</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_trend["Bulan"], y=df_trend["Kes Baharu"], name="Kes Baharu"))
        fig.add_trace(go.Bar(x=df_trend["Bulan"], y=df_trend["Kes Selesai"], name="Kes Selesai"))
        fig.add_trace(go.Scatter(x=df_trend["Bulan"], y=df_trend["PSEI"], name="PSEI", yaxis="y2", mode="lines+markers"))
        fig.update_layout(
            height=440,
            barmode="group",
            yaxis=dict(title="Cases"),
            yaxis2=dict(title="PSEI", overlaying="y", side="right", range=[60, 100]),
            legend=dict(orientation="h"),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("### 🧠 AI-style Executive Insight")
        insights = generate_ai_insights(df_state_f, df_service_f, df_case_f)
        for i, insight in enumerate(insights[:4], start=1):
            st.markdown(f"**{i}.** {insight}")
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(
            df_state_f.sort_values("PSEI", ascending=False).head(10),
            x="Negeri",
            y="PSEI",
            color="PSEI",
            title="Top State Performance by PSEI"
        )
        fig.update_layout(height=390, xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.scatter(
            df_state_f,
            x="Purata Masa Menunggu (hari)",
            y="PSEI",
            size="Jumlah Kes",
            color="Kes Risiko Tinggi",
            hover_name="Negeri",
            title="Waiting Time vs PSEI vs High-Risk Burden"
        )
        fig.add_hline(y=target_psei, line_dash="dash", annotation_text="Target PSEI")
        fig.update_layout(height=390)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 2: STATE AND SERVICE ANALYTICS
# ============================================================
with tabs[1]:
    section_header("State & Service Analytics", "Comparison across states, service types, zones and operational indicators.")

    c1, c2 = st.columns([1.25, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(
            df_state_f.sort_values("PSEI"),
            x="PSEI",
            y="Negeri",
            orientation="h",
            color="Zon",
            title="State Ranking by Psychological Service Effectiveness Index"
        )
        fig.add_vline(x=target_psei, line_dash="dash")
        fig.update_layout(height=560)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        zone_summary = df_state_f.groupby("Zon", as_index=False).agg({
            "PSEI": "mean",
            "Jumlah Kes": "sum",
            "Kes Risiko Tinggi": "sum",
            "Kepuasan": "mean"
        })
        fig = px.treemap(
            zone_summary,
            path=["Zon"],
            values="Jumlah Kes",
            color="PSEI",
            title="Regional Case Volume and PSEI"
        )
        fig.update_layout(height=560)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(
            df_service_f.sort_values("Keberkesanan (%)", ascending=False),
            x="Jenis Perkhidmatan",
            y="Keberkesanan (%)",
            color="Kadar Penyelesaian (%)",
            title="Service Effectiveness by Intervention Type"
        )
        fig.update_layout(height=420, xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.pie(
            df_service_f,
            values="Kes Dikendalikan",
            names="Jenis Perkhidmatan",
            hole=0.42,
            title="Service Case Composition"
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("View State Data Table"):
        st.dataframe(df_state_f, use_container_width=True)

    with st.expander("View Service Data Table"):
        st.dataframe(df_service_f, use_container_width=True)

# ============================================================
# TAB 3: EFFECTIVENESS INDEX
# ============================================================
with tabs[2]:
    section_header("Effectiveness Index Engine", "Simulated weighted scoring model for national service effectiveness evaluation.")

    weights = {
        "Akses": 0.18,
        "Responsif": 0.18,
        "Kualiti Intervensi": 0.20,
        "Hasil Emosi": 0.20,
        "Susulan": 0.12,
        "Kepuasan": 0.12
    }

    dimension_table = pd.DataFrame({
        "Dimension": list(weights.keys()),
        "Weight": list(weights.values()),
        "National Score": [df_state_f[d].mean() for d in weights.keys()]
    })
    dimension_table["Weighted Contribution"] = dimension_table["Weight"] * dimension_table["National Score"]
    national_psei = dimension_table["Weighted Contribution"].sum()

    c1, c2, c3 = st.columns([0.9, 1.1, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=national_psei,
            delta={"reference": target_psei},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#ff4b4b"},
                "steps": [
                    {"range": [0, 55], "color": "#fee2e2"},
                    {"range": [55, 75], "color": "#fef3c7"},
                    {"range": [75, 100], "color": "#dcfce7"},
                ],
            },
            title={"text": "National PSEI"}
        ))
        fig.update_layout(height=410, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.line_polar(
            dimension_table,
            r="National Score",
            theta="Dimension",
            line_close=True,
            title="Dimension Radar"
        )
        fig.update_traces(fill="toself")
        fig.update_layout(height=410)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="gold-card">', unsafe_allow_html=True)
        st.markdown("### Index Formula")
        st.latex(r"""
        PSEI = \sum_{i=1}^{6} w_i S_i
        """)
        st.write("Where:")
        st.write("- w = dimension weight")
        st.write("- S = dimension score")
        st.write("- PSEI = Psychological Service Effectiveness Index")
        st.markdown(f"### Current Score: **{national_psei:.1f}%**")
        st.markdown(f"### Status: **{interpret_score(national_psei)}**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-title">Weighted Dimension Contribution</div>', unsafe_allow_html=True)
    fig = px.bar(
        dimension_table,
        x="Dimension",
        y="Weighted Contribution",
        color="National Score",
        text="Weighted Contribution",
        title="Contribution to National PSEI"
    )
    fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(dimension_table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 4: RISK AND CASE MONITORING
# ============================================================
with tabs[3]:
    section_header("Risk & Case Monitoring", "Operational view of case flow, risk triage, escalation and follow-up monitoring.")

    risk_filter = st.multiselect(
        "Tahap Risiko",
        ["Rendah", "Sederhana", "Tinggi", "Kritikal"],
        default=["Rendah", "Sederhana", "Tinggi", "Kritikal"]
    )

    status_filter = st.multiselect(
        "Status Kes",
        sorted(df_case_f["Status"].unique()),
        default=sorted(df_case_f["Status"].unique())
    )

    df_case_view = df_case_f[
        df_case_f["Tahap Risiko"].isin(risk_filter)
        & df_case_f["Status"].isin(status_filter)
    ].copy()

    urgent = len(df_case_view[df_case_view["Risk Score"] >= alert_threshold])
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Displayed Cases", f"{len(df_case_view):,}", "Filtered case view", "blue")
    with c2:
        kpi_card("Urgent Cases", f"{urgent:,}", "Above selected threshold", "red")
    with c3:
        kpi_card("Avg Risk Score", f"{df_case_view['Risk Score'].mean():.1f}", "Risk triage score", "blue")
    with c4:
        kpi_card("Avg Progress", f"{df_case_view['Progress (%)'].mean():.1f}%", "Intervention progress", "green")

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.histogram(
            df_case_view,
            x="Tahap Risiko",
            color="Status",
            barmode="group",
            title="Case Status by Risk Level"
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.box(
            df_case_view,
            x="Tahap Risiko",
            y="Hari Dalam Proses",
            color="Tahap Risiko",
            title="Case Duration by Risk Level"
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="red-card">', unsafe_allow_html=True)
    st.markdown("### 🚨 Escalation Watchlist")
    watchlist = df_case_view.sort_values("Risk Score", ascending=False).head(12)
    st.dataframe(watchlist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 5: SURVEY AND INSTRUMENT ANALYTICS
# ============================================================
with tabs[4]:
    section_header("Survey & Instrument Analytics", "Prototype module for questionnaire validation, construct reliability and respondent insight.")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Questionnaire Sets", "3", "Client, officer, management", "blue")
    with c2:
        kpi_card("Constructs", "6", "PSEI core dimensions", "green")
    with c3:
        kpi_card("Items", f"{len(df_survey)}", "Simulated instrument items", "blue")
    with c4:
        kpi_card("Avg Loading", f"{df_survey['Loading'].mean():.2f}", "Acceptable range", "green")

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        construct_summary = df_survey.groupby("Konstruk", as_index=False).agg({
            "Min": "mean",
            "Loading": "mean",
            "Alpha if Deleted": "mean"
        })
        fig = px.bar(
            construct_summary,
            x="Konstruk",
            y="Min",
            color="Loading",
            title="Average Construct Mean and Factor Loading"
        )
        fig.update_layout(height=420, xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.scatter(
            df_survey,
            x="Loading",
            y="Min",
            color="Konstruk",
            size="Alpha if Deleted",
            hover_name="Item",
            title="Item Quality Matrix"
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.markdown("### Suggested Questionnaire Architecture")
    st.write("""
    **Set A: Penerima Perkhidmatan** — 40 hingga 50 item.  
    **Set B: Pegawai Pelaksana** — 30 hingga 40 item.  
    **Set C: Pengurusan / Stakeholder** — 15 hingga 25 item.
    """)
    st.write("Focus: access, responsiveness, intervention quality, psychosocial outcome, follow-up continuity and satisfaction.")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("View Simulated Survey Item Table"):
        st.dataframe(df_survey, use_container_width=True)

# ============================================================
# TAB 6: FORECASTING AND SIMULATION
# ============================================================
with tabs[5]:
    section_header("Forecasting & Simulation", "Simple scenario engine to estimate future case pressure and performance gap.")

    growth_rate = st.slider("Projected Monthly Case Growth (%)", -10, 30, 8)
    intervention_boost = st.slider("Expected Intervention Improvement (%)", 0, 20, 6)
    staff_increase = st.slider("Additional Staff Capacity (%)", 0, 50, 10)

    forecast = df_trend.copy()
    last_cases = forecast["Kes Baharu"].iloc[-1]
    future_months = pd.date_range("2026-07-01", periods=6, freq="M").strftime("%b %Y")
    future_rows = []
    for i, m in enumerate(future_months, start=1):
        projected_cases = int(last_cases * ((1 + growth_rate/100) ** i))
        capacity_effect = 1 + staff_increase/150
        projected_solved = int(projected_cases * min(0.95, (0.78 + intervention_boost/100) * capacity_effect))
        projected_psei = min(96, forecast["PSEI"].iloc[-1] + intervention_boost * 0.35 + i*0.3)
        future_rows.append({
            "Bulan": m,
            "Kes Baharu": projected_cases,
            "Kes Selesai": projected_solved,
            "Kes Risiko Tinggi": int(projected_cases * 0.15),
            "PSEI": round(projected_psei, 1),
            "Kepuasan": round(min(96, forecast["Kepuasan"].iloc[-1] + intervention_boost*0.25), 1),
            "Masa Menunggu": round(max(2, forecast["Masa Menunggu"].iloc[-1] - staff_increase*0.08), 1)
        })
    df_future = pd.DataFrame(future_rows)
    df_forecast_all = pd.concat([forecast, df_future], ignore_index=True)
    df_forecast_all["Type"] = ["Historical"]*len(forecast) + ["Forecast"]*len(df_future)

    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.line(
            df_forecast_all,
            x="Bulan",
            y=["Kes Baharu", "Kes Selesai"],
            color_discrete_sequence=None,
            markers=True,
            title="Projected Case Pressure and Resolution"
        )
        fig.update_layout(height=430)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.line(
            df_forecast_all,
            x="Bulan",
            y="PSEI",
            color="Type",
            markers=True,
            title="Projected PSEI Improvement"
        )
        fig.add_hline(y=target_psei, line_dash="dash", annotation_text="Target")
        fig.update_layout(height=430)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="green-card">', unsafe_allow_html=True)
    st.markdown("### Simulation Insight")
    projected_gap = int(df_future["Kes Baharu"].sum() - df_future["Kes Selesai"].sum())
    st.write(f"Projected six-month unresolved case gap: **{projected_gap:,} cases**.")
    st.write("This module can be extended into a policy simulation tool using real historical case data, officer workload and service capacity.")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 7: POLICY RECOMMENDATION ENGINE
# ============================================================
with tabs[6]:
    section_header("Policy Recommendation Engine", "Converts analytical signals into structured action recommendations.")

    recommendations = pd.DataFrame({
        "Analytical Signal": [
            "Low follow-up continuity",
            "High waiting time in selected states",
            "Concentration of high-risk cases",
            "Variation in service effectiveness",
            "Need for national effectiveness indicator",
            "Need for officer workload monitoring",
            "Need for digital case escalation workflow",
            "Need for annual benchmarking"
        ],
        "Recommended Action": [
            "Develop digital follow-up reminder and post-session tracking system.",
            "Introduce service-level benchmark for maximum waiting time.",
            "Implement psychological risk triage and rapid referral protocol.",
            "Standardise intervention modules by service category.",
            "Adopt Psychological Service Effectiveness Index as annual KPI.",
            "Monitor officer caseload, case complexity and intervention duration.",
            "Create escalation workflow for critical and prolonged cases.",
            "Publish internal annual state and service benchmark report."
        ],
        "Priority": [
            "High", "High", "Very High", "Medium", "Very High", "High", "Very High", "Medium"
        ],
        "Timeframe": [
            "3-6 months", "6 months", "3 months", "6-12 months", "6 months", "6 months", "3-6 months", "12 months"
        ],
        "Policy Value": [5, 4, 5, 3, 5, 4, 5, 3]
    })

    c1, c2 = st.columns([1.1, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(recommendations, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = px.bar(
            recommendations,
            x="Policy Value",
            y="Analytical Signal",
            orientation="h",
            color="Priority",
            title="Policy Priority Mapping"
        )
        fig.update_layout(height=520)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown("### Strategic Narrative for Tender")
    st.write("""
    This prototype demonstrates that the proposed study can go beyond a conventional survey report.
    The findings can be translated into a continuous service intelligence platform that supports
    monitoring, prioritisation, intervention improvement and evidence-based policy decisions.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# TAB 8: DELIVERABLES
# ============================================================
with tabs[7]:
    section_header("Project Deliverables", "Proposed outputs for the JKM effectiveness evaluation study.")

    deliverables = pd.DataFrame({
        "Deliverable": [
            "Inception Report",
            "Validated Questionnaire Instruments",
            "Interview and FGD Protocol",
            "Progress Report",
            "Quantitative Analysis Report",
            "Qualitative Thematic Report",
            "Psychological Service Effectiveness Index",
            "Interactive Dashboard Prototype",
            "Final Technical Report",
            "Executive Summary for Policymakers",
            "Policy Recommendation Matrix",
            "Presentation Deck"
        ],
        "Purpose": [
            "Confirm methodology, workplan and sampling strategy.",
            "Support survey data collection and construct measurement.",
            "Guide qualitative data collection.",
            "Update JKM on project implementation status.",
            "Present survey findings and statistical analysis.",
            "Present themes, issues and narratives.",
            "Provide national effectiveness scoring model.",
            "Visualise performance, risks and policy insights.",
            "Full documentation of study findings.",
            "Short strategic document for decision makers.",
            "Translate findings into actionable recommendations.",
            "Support final briefing and stakeholder engagement."
        ],
        "Format": [
            "PDF", "DOCX/PDF", "DOCX/PDF", "PDF", "PDF", "PDF", "XLSX/PDF",
            "Streamlit/Web", "PDF", "PDF", "XLSX/PDF", "PPTX"
        ],
        "Value": [
            "Project governance", "Data quality", "Fieldwork consistency", "Monitoring",
            "Evidence base", "Deep insight", "KPI monitoring", "Decision support",
            "Official record", "Policy communication", "Implementation planning", "Stakeholder presentation"
        ]
    })

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(deliverables, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="gold-card">', unsafe_allow_html=True)
        st.markdown("### Phase 1")
        st.write("Inception, instrument development, pilot test and sampling finalisation.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="green-card">', unsafe_allow_html=True)
        st.markdown("### Phase 2")
        st.write("Nationwide data collection, interviews, FGD and document review.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="dark-card">', unsafe_allow_html=True)
        st.markdown("### Phase 3")
        st.write("Analytics, framework, dashboard, policy recommendations and reporting.")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer-note">
    JKM Psychological Service Intelligence Platform — Early Analytical Prototype.
    All data shown are simulated for proposal demonstration only.
</div>
""", unsafe_allow_html=True)
