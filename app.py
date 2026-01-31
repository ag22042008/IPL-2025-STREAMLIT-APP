import pandas as pd
import plotly.express as px
import streamlit as st
import base64

# =========================
# BACKGROUND IMAGE
# =========================
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: -1;
        }}
        h1, h2, h3, h4, p {{
            color: #ffffff;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("Screenshot 2026-01-30 234139.png")

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="IPL 2025 Analysis", layout="wide")
st.title("🏏 IPL 2025 Interactive Data Analysis Dashboard")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    bowlers = pd.read_csv("IPL2025Bowlers.csv")
    matches.fillna(0, inplace=True)
    return matches, bowlers

ipl2025, bowlers = load_data()

# =========================
# TOP NAVIGATION
# =========================
c1, c2, c3, c4, c5 = st.columns(5)
section = None

if c1.button("📊 Dataset Overview"):
    section = "dataset"
if c2.button("🪙 Toss & Results"):
    section = "toss"
if c3.button("📈 Points & Batting"):
    section = "batting"
if c4.button("🎯 Bowling Analysis"):
    section = "bowling"
if c5.button("🧠 Advanced Insights"):
    section = "advanced"

# =========================
# DATASET OVERVIEW (TEXT ONLY)
# =========================
if section == "dataset":
    st.header("📊 Dataset Overview & Structural Analysis")

    st.markdown("""
The IPL 2025 match dataset consists of **74 matches and 22 columns**, integrating numerical, categorical, and text features.
It captures match context such as teams, venues, stages, toss outcomes, innings scores, and match results.

Several columns contain missing values (e.g., wide-ball data, awards, match winner), which naturally arise due to abandoned or no-result matches.
Overall, the dataset is structurally sound and suitable for match-flow, scoring, and strategic analysis.
    """)

    st.markdown("""
The bowling dataset contains **108 bowlers with 13 performance metrics** and **no missing values**.
This ensures high analytical reliability for identifying economical bowlers, impact players, death-over specialists, and underrated performers.
    """)

# =========================
# TOSS & RESULTS ANALYSIS
# =========================
elif section == "toss":
    st.header("🪙 Toss & Match Results")

    toss_choice = ipl2025["toss_decision"].value_counts().reset_index()
    toss_choice.columns = ["Decision", "Count"]

    fig = px.bar(
        toss_choice,
        x="Decision",
        y="Count",
        color="Decision",
        title="Toss Decision: Bat vs Field"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Teams showed a clear preference based on pitch and chasing trends.
- Toss decisions reflect evolving T20 strategies.
    """)

    toss_win = ipl2025[ipl2025["toss_winner"] == ipl2025["match_winner"]]
    win_rate = round(len(toss_win) / len(ipl2025) * 100, 2)

    st.markdown(f"""
**Insight:**  
Teams winning the toss also won the match **{win_rate}%** of the time, indicating a moderate toss advantage.
    """)

# =========================
# POINTS TABLE + BATTING
# =========================
elif section == "batting":
    st.header("📈 Points Table & Batting Analysis")

    # Points Table
    pts = ipl2025[ipl2025["match_winner"] != 0]["match_winner"].value_counts() * 2
    ties = ipl2025[ipl2025["match_winner"] == 0]

    for _, r in ties.iterrows():
        pts[r["team1"]] = pts.get(r["team1"], 0) + 1
        pts[r["team2"]] = pts.get(r["team2"], 0) + 1

    pts = pts.sort_values(ascending=False).reset_index()
    pts.columns = ["Team", "Points"]

    fig = px.bar(
        pts,
        x="Team",
        y="Points",
        color="Points",
        title="IPL 2025 Points Table"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Batting
    bat = (
        ipl2025[ipl2025["top_scorer"] != 0]
        .groupby("top_scorer")["highscore"]
        .max()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        bat,
        y="top_scorer",
        x="highscore",
        color="highscore",
        title="Top Individual Scores (IPL 2025)"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# BOWLING ANALYSIS
# =========================
elif section == "bowling":
    st.header("🎯 Bowling Analysis")

    eco = bowlers.sort_values("ECO").head(10)
    fig = px.bar(eco, y="Player Name", x="ECO", color="Team",
                 title="Top Economical Bowlers")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(
        bowlers,
        x="WKT",
        y="ECO",
        size="OVR",
        color="Team",
        hover_name="Player Name",
        title="Wickets vs Economy Rate"
    )
    st.plotly_chart(fig, use_container_width=True)

    team_eco = bowlers.groupby("Team")["ECO"].mean().reset_index()
    fig = px.bar(
        team_eco,
        x="Team",
        y="ECO",
        color="ECO",
        title="Team-wise Average Economy Rate"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# ADVANCED INSIGHTS
# =========================
elif section == "advanced":
    st.header("🧠 Advanced Bowling Insights")

    death = bowlers[bowlers["OVR"] > 15]
    fig = px.scatter(death, x="ECO", y="SR", color="Team",
                     hover_name="Player Name",
                     title="Death Overs: Strike Rate vs Economy")
    st.plotly_chart(fig, use_container_width=True)

    impact = bowlers[bowlers["OVR"] < 16].head(10)
    fig = px.bar(impact, x="Player Name", y="WKT", color="Team",
                 title="Impact Bowlers")
    st.plotly_chart(fig, use_container_width=True)

    underrated = bowlers[(bowlers["MAT"] < 8) & (bowlers["MAT"] > 3)].sort_values("ECO").head(5)
    fig = px.bar(underrated, y="Player Name", x="ECO", color="Team",
                 title="Underrated Bowlers")
    st.plotly_chart(fig, use_container_width=True)
