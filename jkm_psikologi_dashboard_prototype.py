# ============================================================
# JKM Psychological & Counselling Service Effectiveness Dashboard
# Prototype for Tender Proposal: JKM.PK.600-13/1/7
# Author: UiTM / UiTM Technoventure Proposal Team
# Note: This prototype uses synthetic demo data for presentation purposes.
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="JKM Psychological Service Effectiveness Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #f6f8ff 0%, #eef6ff 45%, #fff8e7 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001845 0%, #023e8a 55%, #0077b6 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero-card {
        padding: 34px 38px;
        border-radius: 28px;
        background: linear-gradient(135deg, #001845 0%, #023e8a 55%, #0077b6 100%);
        color: white;
        box-shadow: 0 20px 45px rgba(0, 24, 69, 0.22);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .hero-card:after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        border-radius: 50%;
        background: rgba(244, 211, 94, 0.18);
        top: -100px;
        right: -70px;
    }

    .hero-title {
        font-size: 42px;
        line-height: 1.08;
        font-weight: 900;
        letter-spacing: -1.4px;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.92;
        max-width: 950px;
        line-height: 1.55;
    }

    .badge-row {
        margin-top: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .badge {
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.24);
        color: white;
        font-weight: 700;
        font-size: 13px;
    }

    .metric-card {
        padding: 22px 22px;
        border-radius: 22px;
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(2,62,138,0.08);
        box-shadow: 0 15px 35px rgba(0, 24, 69, 0.08);
        min-height: 146px;
    }

    .metric-label {
        font-size: 13px;
        color: #5c677d;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 34px;
        color: #001845;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .metric-note {
        font-size: 13px;
        color: #087f5b;
        font-weight: 700;
    }

    .section-title {
        font-size: 25px;
        font-weight: 900;
        color: #001845;
        margin: 10px 0 8px 0;
        letter-spacing: -0.5px;
    }

    .section-subtitle {
        color: #5c677d;
        font-size: 14px;
        margin-bottom: 16px;
    }

    .insight-box {
        border-radius: 22px;
        padding: 22px 24px;
        background: linear-gradient(135deg, rgba(244,211,94,0.25), rgba(255,255,255,0.9));
        border-left: 6px solid #c5a017;
        box-shadow: 0 10px 25px rgba(0,0,0,0.06);
        margin: 10px 0 18px 0;
    }

    .insight-title {
        color: #001845;
        font-weight: 900;
        font-size: 18px;
        margin-bottom: 6px;
    }

    .insight-text {
        color: #333333;
        line-height: 1.55;
        font-size: 14px;
    }

    .small-note {
        color: #6c757d;
        font-size: 12px;
        margin-top: 4px;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.75);
        border: 1px solid rgba(2,62,138,0.08);
        padding: 18px 18px;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(0, 24, 69, 0.06);
    }

    .footer {
        margin-top: 34px;
        padding: 18px 22px;
        border-radius: 18px;
        background: #001845;
        color: white;
        text-align: center;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# DEMO DATA GENERATOR
# -----------------------------
@st.cache_data
def generate_demo_data(seed: int = 2026):
    rng = np.random.default_rng(seed)

    states = [
        "Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan", "Pahang",
        "Pulau Pinang", "Perak", "Perlis", "Selangor", "Terengganu",
        "Sabah", "Sarawak", "W.P. Kuala Lumpur", "W.P. Labuan", "W.P. Putrajaya"
    ]

    services = [
        "Kaunseling Individu", "Kaunseling Keluarga", "Intervensi Krisis",
        "Sokongan Trauma", "Bimbingan Psikososial", "Kaunseling Kelompok"
    ]

    target_groups = [
        "Kanak-kanak", "Remaja", "Wanita", "Warga Emas", "OKU", "Keluarga Berisiko", "Komuniti Rentan"
    ]

    months = pd.date_range("2025-01-01", periods=18, freq="MS")

    rows = []
    for m in months:
        for state in states:
            for service in services:
                base = rng.integers(60, 230)
                demand_factor = 1.35 if state in ["Selangor", "W.P. Kuala Lumpur", "Johor", "Sabah", "Sarawak"] else 1.0
                cases = int(base * demand_factor + rng.normal(0, 18))
                cases = max(cases, 15)

                access = np.clip(rng.normal(76, 7), 48, 96)
                quality = np.clip(rng.normal(80, 6), 55, 98)
                satisfaction = np.clip(rng.normal(78, 7), 50, 98)
                outcome = np.clip(rng.normal(74, 8), 45, 96)
                continuity = np.clip(rng.normal(69, 9), 35, 94)
                workload_pressure = np.clip(rng.normal(64, 10), 30, 95)

                if service == "Intervensi Krisis":
                    outcome -= rng.uniform(1, 5)
                    workload_pressure += rng.uniform(4, 8)
                if service == "Kaunseling Keluarga":
                    satisfaction -= rng.uniform(0, 3)
                if state in ["Sabah", "Sarawak", "Kelantan", "Pahang"]:
                    access -= rng.uniform(2, 7)

                effectiveness = (
                    0.18 * access +
                    0.22 * quality +
                    0.18 * satisfaction +
                    0.25 * outcome +
                    0.12 * continuity +
                    0.05 * (100 - workload_pressure)
                )
                effectiveness = np.clip(effectiveness + rng.normal(0, 2.2), 35, 96)

                avg_wait = np.clip(rng.normal(11, 3.5) + (100-access)/11, 3, 28)
                completion = np.clip(rng.normal(82, 8), 45, 98)
                relapse_risk = np.clip(100 - outcome + rng.normal(0, 7), 6, 60)

                rows.append({
                    "month": m,
                    "state": state,
                    "service_type": service,
                    "cases": cases,
                    "access_score": round(access, 1),
                    "quality_score": round(quality, 1),
                    "satisfaction_score": round(satisfaction, 1),
                    "outcome_score": round(outcome, 1),
                    "continuity_score": round(continuity, 1),
                    "workload_pressure": round(workload_pressure, 1),
                    "effectiveness_index": round(effectiveness, 1),
                    "avg_wait_days": round(avg_wait, 1),
                    "completion_rate": round(completion, 1),
                    "relapse_risk": round(relapse_risk, 1),
                    "target_group": rng.choice(target_groups)
                })

    df = pd.DataFrame(rows)

    # Case-level examples for operational table
    case_rows = []
    risk_levels = ["Rendah", "Sederhana", "Tinggi"]
    statuses = ["Selesai", "Dalam Tindakan", "Susulan", "Dirujuk"]
    for i in range(320):
        created = datetime(2026, 1, 1) + timedelta(days=int(rng.integers(0, 135)))
        state = rng.choice(states)
        service = rng.choice(services)
        risk = rng.choice(risk_levels, p=[0.44, 0.38, 0.18])
        status = rng.choice(statuses, p=[0.48, 0.22, 0.21, 0.09])
        score = np.clip(rng.normal(76, 10), 38, 98)
        case_rows.append({
            "Case ID": f"JKM-{2026}-{i+1001}",
            "Tarikh": created.strftime("%d/%m/%Y"),
            "Negeri": state,
            "Jenis Perkhidmatan": service,
            "Kumpulan Sasar": rng.choice(target_groups),
            "Tahap Risiko": risk,
            "Status": status,
            "Skor Keberkesanan": round(score, 1),
            "Hari Menunggu": int(np.clip(rng.normal(9, 4), 1, 26)),
            "Catatan Ringkas": rng.choice([
                "Memerlukan susulan berkala",
                "Intervensi menunjukkan kemajuan",
                "Perlu rujukan sokongan komuniti",
                "Kes stabil selepas sesi",
                "Perlu pemantauan risiko"
            ])
        })
    case_df = pd.DataFrame(case_rows)

    return df, case_df


df, case_df = generate_demo_data()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.markdown("# 🧠 JKM Analytics")
st.sidebar.markdown("**Prototype Dashboard**  ")
st.sidebar.markdown("Kajian Penilaian Keberkesanan Perkhidmatan Psikologi dan Kaunseling")
st.sidebar.markdown("---")

selected_states = st.sidebar.multiselect(
    "Pilih Negeri",
    options=sorted(df["state"].unique()),
    default=["Selangor", "W.P. Kuala Lumpur", "Negeri Sembilan", "Johor", "Sabah", "Sarawak"]
)

selected_services = st.sidebar.multiselect(
    "Pilih Jenis Perkhidmatan",
    options=sorted(df["service_type"].unique()),
    default=sorted(df["service_type"].unique())
)

min_month, max_month = df["month"].min(), df["month"].max()
month_range = st.sidebar.slider(
    "Julat Bulan Analisis",
    min_value=min_month.to_pydatetime(),
    max_value=max_month.to_pydatetime(),
    value=(min_month.to_pydatetime(), max_month.to_pydatetime()),
    format="MMM YYYY"
)

st.sidebar.markdown("---")
st.sidebar.info("Data dalam sistem ini adalah data simulasi untuk tujuan prototype tender sahaja.")

filtered = df[
    (df["state"].isin(selected_states)) &
    (df["service_type"].isin(selected_services)) &
    (df["month"] >= pd.to_datetime(month_range[0])) &
    (df["month"] <= pd.to_datetime(month_range[1]))
].copy()

if filtered.empty:
    st.warning("Tiada data untuk pilihan semasa. Sila ubah filter.")
    st.stop()

# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Psychological Service Effectiveness Dashboard</div>
        <div class="hero-subtitle">
            Prototype analitik untuk menilai keberkesanan perkhidmatan psikologi dan kaunseling JKM melalui indeks keberkesanan, pemetaan jurang perkhidmatan, trend intervensi, pengalaman penerima dan cadangan tindakan strategik.
        </div>
        <div class="badge-row">
            <div class="badge">JKM.PK.600-13/1/7</div>
            <div class="badge">Mixed-Method Evaluation</div>
            <div class="badge">Effectiveness Index</div>
            <div class="badge">Policy Intelligence</div>
            <div class="badge">Synthetic Demo Data</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# KPI CARDS
# -----------------------------
total_cases = int(filtered["cases"].sum())
eff = filtered["effectiveness_index"].mean()
sat = filtered["satisfaction_score"].mean()
wait = filtered["avg_wait_days"].mean()
completion = filtered["completion_rate"].mean()
risk = filtered["relapse_risk"].mean()

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.metric("Jumlah Kes", f"{total_cases:,}", "+12.4%")
with c2:
    st.metric("Indeks Keberkesanan", f"{eff:.1f}/100", "+3.1")
with c3:
    st.metric("Kepuasan Penerima", f"{sat:.1f}%", "+2.6%")
with c4:
    st.metric("Purata Menunggu", f"{wait:.1f} hari", "-1.2 hari")
with c5:
    st.metric("Kadar Selesai", f"{completion:.1f}%", "+4.5%")
with c6:
    st.metric("Risiko Susulan", f"{risk:.1f}%", "-2.1%")

st.markdown(
    """
    <div class="insight-box">
        <div class="insight-title">Strategic Insight</div>
        <div class="insight-text">
            Prototype ini menunjukkan bagaimana JKM boleh memantau keberkesanan perkhidmatan secara berterusan melalui kombinasi indikator akses, kualiti intervensi, kepuasan penerima, hasil psikososial, kesinambungan perkhidmatan dan tekanan beban kerja pegawai.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Overview",
    "🗺️ Negeri & Perkhidmatan",
    "🧮 Effectiveness Index",
    "📋 Case Monitoring",
    "🎯 Policy Recommendation"
])

# -----------------------------
# TAB 1
# -----------------------------
with tab1:
    st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Ringkasan prestasi keseluruhan perkhidmatan psikologi dan kaunseling berdasarkan data simulasi.</div>', unsafe_allow_html=True)

    monthly = filtered.groupby("month", as_index=False).agg(
        cases=("cases", "sum"),
        effectiveness_index=("effectiveness_index", "mean"),
        satisfaction_score=("satisfaction_score", "mean"),
        outcome_score=("outcome_score", "mean")
    )

    col_a, col_b = st.columns([1.45, 1])
    with col_a:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["month"], y=monthly["effectiveness_index"],
            mode="lines+markers", name="Indeks Keberkesanan",
            line=dict(width=4)
        ))
        fig.add_trace(go.Scatter(
            x=monthly["month"], y=monthly["satisfaction_score"],
            mode="lines+markers", name="Kepuasan",
            line=dict(width=3, dash="dot")
        ))
        fig.update_layout(
            title="Trend Indeks Keberkesanan dan Kepuasan",
            template="plotly_white",
            height=420,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=70, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        service_share = filtered.groupby("service_type", as_index=False)["cases"].sum().sort_values("cases", ascending=False)
        fig = px.pie(
            service_share,
            names="service_type",
            values="cases",
            hole=0.48,
            title="Komposisi Kes Mengikut Perkhidmatan"
        )
        fig.update_layout(template="plotly_white", height=420, margin=dict(l=20, r=20, t=70, b=20))
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        fig = px.bar(
            monthly,
            x="month",
            y="cases",
            title="Jumlah Kes Bulanan",
            text_auto=True
        )
        fig.update_layout(template="plotly_white", height=380, margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        radar_values = [
            filtered["access_score"].mean(),
            filtered["quality_score"].mean(),
            filtered["satisfaction_score"].mean(),
            filtered["outcome_score"].mean(),
            filtered["continuity_score"].mean(),
        ]
        categories = ["Akses", "Kualiti", "Kepuasan", "Hasil", "Kesinambungan"]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_values + [radar_values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name="Dimensi Perkhidmatan"
        ))
        fig.update_layout(
            title="Radar Dimensi Keberkesanan",
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=380,
            template="plotly_white",
            margin=dict(l=20, r=20, t=60, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TAB 2
# -----------------------------
with tab2:
    st.markdown('<div class="section-title">Analisis Negeri dan Jenis Perkhidmatan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Mengenal pasti negeri, jenis perkhidmatan dan kumpulan sasar yang memerlukan perhatian strategik.</div>', unsafe_allow_html=True)

    state_summary = filtered.groupby("state", as_index=False).agg(
        cases=("cases", "sum"),
        effectiveness_index=("effectiveness_index", "mean"),
        avg_wait_days=("avg_wait_days", "mean"),
        workload_pressure=("workload_pressure", "mean")
    ).sort_values("effectiveness_index", ascending=False)

    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        fig = px.bar(
            state_summary,
            x="effectiveness_index",
            y="state",
            orientation="h",
            size="cases",
            title="Ranking Negeri Berdasarkan Indeks Keberkesanan",
            hover_data=["cases", "avg_wait_days", "workload_pressure"]
        )
        fig.update_layout(template="plotly_white", height=520, yaxis=dict(categoryorder="total ascending"), margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig = px.scatter(
            state_summary,
            x="avg_wait_days",
            y="effectiveness_index",
            size="cases",
            color="workload_pressure",
            hover_name="state",
            title="Matriks Akses vs Keberkesanan",
            labels={"avg_wait_days": "Purata Hari Menunggu", "effectiveness_index": "Indeks Keberkesanan"}
        )
        fig.update_layout(template="plotly_white", height=520, margin=dict(l=20, r=20, t=60, b=20))
        st.plotly_chart(fig, use_container_width=True)

    heat = filtered.pivot_table(
        index="state",
        columns="service_type",
        values="effectiveness_index",
        aggfunc="mean"
    ).round(1)
    fig = px.imshow(
        heat,
        text_auto=True,
        aspect="auto",
        title="Heatmap Keberkesanan Mengikut Negeri dan Jenis Perkhidmatan"
    )
    fig.update_layout(template="plotly_white", height=560, margin=dict(l=20, r=20, t=70, b=20))
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TAB 3
# -----------------------------
with tab3:
    st.markdown('<div class="section-title">Psychological Service Effectiveness Index</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Indeks demo yang menggabungkan beberapa dimensi keberkesanan untuk pemantauan strategik JKM.</div>', unsafe_allow_html=True)

    st.latex(r"PSEI = 0.18A + 0.22Q + 0.18S + 0.25O + 0.12C + 0.05(100-W)")

    st.markdown(
        """
        <div class="insight-box">
            <div class="insight-title">Interpretasi Indeks</div>
            <div class="insight-text">
            A = akses perkhidmatan, Q = kualiti intervensi, S = kepuasan penerima, O = hasil psikososial, C = kesinambungan perkhidmatan, W = tekanan beban kerja. Formula ini boleh disemak semula selepas kajian rintis dan pengesahan pakar.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    index_summary = filtered.groupby("service_type", as_index=False).agg(
        access_score=("access_score", "mean"),
        quality_score=("quality_score", "mean"),
        satisfaction_score=("satisfaction_score", "mean"),
        outcome_score=("outcome_score", "mean"),
        continuity_score=("continuity_score", "mean"),
        workload_pressure=("workload_pressure", "mean"),
        effectiveness_index=("effectiveness_index", "mean")
    ).round(1).sort_values("effectiveness_index", ascending=False)

    col_a, col_b = st.columns([1.25, 1])
    with col_a:
        fig = px.bar(
            index_summary,
            x="service_type",
            y="effectiveness_index",
            text="effectiveness_index",
            title="Indeks Keberkesanan Mengikut Jenis Perkhidmatan"
        )
        fig.update_layout(template="plotly_white", height=430, xaxis_tickangle=-25, margin=dict(l=20, r=20, t=60, b=80))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        top = index_summary.iloc[0]
        st.markdown("### 🏆 Perkhidmatan Prestasi Tertinggi")
        st.success(f"{top['service_type']} mencatat indeks tertinggi iaitu {top['effectiveness_index']:.1f}/100.")
        low = index_summary.iloc[-1]
        st.warning(f"{low['service_type']} memerlukan perhatian lanjut dengan indeks {low['effectiveness_index']:.1f}/100.")
        st.markdown("**Cadangan Tindakan:** Perkukuh SOP susulan, latihan intervensi khusus, dan pemantauan outcome selepas sesi.")

    st.dataframe(index_summary, use_container_width=True, hide_index=True)

# -----------------------------
# TAB 4
# -----------------------------
with tab4:
    st.markdown('<div class="section-title">Case Monitoring Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Contoh jadual pemantauan kes untuk menunjukkan potensi sistem apabila diintegrasi dengan data sebenar JKM.</div>', unsafe_allow_html=True)

    case_filtered = case_df[case_df["Negeri"].isin(selected_states) & case_df["Jenis Perkhidmatan"].isin(selected_services)].copy()

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        risk_filter = st.selectbox("Tahap Risiko", ["Semua"] + sorted(case_filtered["Tahap Risiko"].unique().tolist()))
    with col_b:
        status_filter = st.selectbox("Status Kes", ["Semua"] + sorted(case_filtered["Status"].unique().tolist()))
    with col_c:
        min_score = st.slider("Minimum Skor Keberkesanan", 0, 100, 50)
    with col_d:
        search = st.text_input("Cari Case ID / Catatan")

    if risk_filter != "Semua":
        case_filtered = case_filtered[case_filtered["Tahap Risiko"] == risk_filter]
    if status_filter != "Semua":
        case_filtered = case_filtered[case_filtered["Status"] == status_filter]
    case_filtered = case_filtered[case_filtered["Skor Keberkesanan"] >= min_score]
    if search:
        case_filtered = case_filtered[
            case_filtered["Case ID"].str.contains(search, case=False, na=False) |
            case_filtered["Catatan Ringkas"].str.contains(search, case=False, na=False)
        ]

    st.dataframe(case_filtered, use_container_width=True, hide_index=True, height=520)

    col_e, col_f = st.columns(2)
    with col_e:
        risk_counts = case_filtered["Tahap Risiko"].value_counts().reset_index()
        risk_counts.columns = ["Tahap Risiko", "Bilangan"]
        fig = px.bar(risk_counts, x="Tahap Risiko", y="Bilangan", text="Bilangan", title="Kes Mengikut Tahap Risiko")
        fig.update_layout(template="plotly_white", height=360)
        st.plotly_chart(fig, use_container_width=True)
    with col_f:
        status_counts = case_filtered["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Bilangan"]
        fig = px.pie(status_counts, names="Status", values="Bilangan", hole=0.45, title="Status Kes")
        fig.update_layout(template="plotly_white", height=360)
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TAB 5
# -----------------------------
with tab5:
    st.markdown('<div class="section-title">Policy Recommendation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Cadangan automatik berdasarkan indikator demo untuk menunjukkan konsep decision-support kepada pengurusan JKM.</div>', unsafe_allow_html=True)

    state_rec = filtered.groupby("state", as_index=False).agg(
        effectiveness_index=("effectiveness_index", "mean"),
        access_score=("access_score", "mean"),
        avg_wait_days=("avg_wait_days", "mean"),
        workload_pressure=("workload_pressure", "mean"),
        continuity_score=("continuity_score", "mean"),
        cases=("cases", "sum")
    ).round(1)

    def generate_priority(row):
        if row["effectiveness_index"] < 70 and row["avg_wait_days"] > 12:
            return "Tinggi", "Perkukuh akses perkhidmatan, tambah slot kaunseling dan semak proses temujanji."
        if row["workload_pressure"] > 70:
            return "Tinggi", "Laksanakan pengagihan beban kes, sokongan pegawai dan latihan pengurusan krisis."
        if row["continuity_score"] < 68:
            return "Sederhana", "Perkukuh sistem susulan, reminder digital dan protokol kesinambungan kes."
        if row["effectiveness_index"] >= 78:
            return "Rendah", "Kekalkan amalan baik dan jadikan sebagai lokasi benchmarking."
        return "Sederhana", "Pantau indikator utama dan laksanakan penambahbaikan berfasa."

    recs = state_rec.apply(lambda r: generate_priority(r), axis=1)
    state_rec["Keutamaan"] = [r[0] for r in recs]
    state_rec["Cadangan Strategik"] = [r[1] for r in recs]
    state_rec = state_rec.sort_values(["Keutamaan", "effectiveness_index"], ascending=[False, True])

    st.dataframe(state_rec, use_container_width=True, hide_index=True)

    high_priority = state_rec[state_rec["Keutamaan"] == "Tinggi"]
    st.markdown("### 🔴 Senarai Keutamaan Tindakan")
    if high_priority.empty:
        st.success("Tiada negeri berstatus keutamaan tinggi berdasarkan filter semasa.")
    else:
        for _, row in high_priority.iterrows():
            st.error(f"{row['state']}: {row['Cadangan Strategik']}")

    st.markdown("### Cadangan Output Kepada JKM")
    st.markdown(
        """
        1. **Indeks Keberkesanan Tahunan** untuk pemantauan prestasi perkhidmatan psikologi dan kaunseling.
        2. **Dashboard Pengurusan** bagi melihat trend, jurang akses, beban kerja dan outcome psikososial.
        3. **Matriks Keutamaan Intervensi** mengikut negeri, jenis perkhidmatan dan kumpulan sasar.
        4. **Policy Brief** ringkas untuk pengurusan tertinggi berdasarkan dapatan empirikal.
        5. **Sistem Amaran Awal** untuk kes berisiko tinggi atau lokasi dengan tekanan perkhidmatan tinggi.
        """
    )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    """
    <div class="footer">
        Prototype prepared for proposal demonstration only · Synthetic data · UiTM / UiTM Technoventure · JKM Psychological Service Evaluation
    </div>
    """,
    unsafe_allow_html=True
)
