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
if c3.button("🔥 High Scoring Matches"):
    section = "runs"
if c4.button("📈 Points & Batting"):
    section = "batting"
if c5.button("🎯 Bowling & Insights"):
    section = "bowling"

# =========================
# DATASET OVERVIEW (TEXT ONLY)
# =========================
if section == "dataset":
    st.header("📊 Dataset Overview & Structural Analysis")

    st.markdown("""
### 📁 Match-Level Dataset Analysis

The IPL 2025 match dataset consists of **74 matches and 22 columns**, covering league and playoff fixtures.
It integrates numerical, categorical, and text-based attributes capturing teams, venues, toss decisions,
innings performance, and match outcomes.

Numerical variables such as innings scores, wickets lost, balls remaining, and highest individual scores
enable quantitative evaluation, while categorical features like stage, toss decision, and match result
support outcome-based comparisons. Missing values occur primarily in wide-ball statistics and
award-related columns, reflecting abandoned or no-result matches.

Overall, the dataset is structurally rich and suitable for match-flow, scoring, and strategic analysis.
    """)

    st.markdown("""
### 🎯 Bowling Dataset Analysis

The bowling dataset includes **108 bowlers across 13 attributes** with **no missing values**.
It captures wickets, overs, economy rate, strike rate, bowling average, and match appearances.

This dataset enables reliable identification of economical bowlers, death-over specialists,
impact bowlers, and underrated performers across IPL 2025.
    """)

# =========================
# TOSS & RESULTS
# =========================
elif section == "toss":
    st.header("🪙 Toss & Match Results Analysis")

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

    toss_win = ipl2025[ipl2025["toss_winner"] == ipl2025["match_winner"]]
    win_rate = round(len(toss_win) / len(ipl2025) * 100, 2)

    st.markdown(f"""
**Conclusion:**
- Toss decisions reflect evolving T20 strategies.
- Teams winning the toss also won the match **{win_rate}%** of the time, indicating a moderate toss advantage.
    """)

# =========================
# HIGH SCORING MATCHES (KEPT)
# =========================
elif section == "runs":
    st.header("🔥 Top 10 Highest Scoring Matches (IPL 2025)")

    ipl2025["total_score"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

    top10 = (
        ipl2025
        .sort_values("total_score", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top10,
        x="match_id",
        y="total_score",
        color="total_score",
        color_continuous_scale="Inferno",
        hover_data=["team1", "team2", "venue", "stage"],
        title="Top 10 Highest Scoring Matches of IPL 2025"
    )

    fig.update_layout(
        xaxis_title="Match ID",
        yaxis_title="Total Runs (1st + 2nd Innings)",
        coloraxis_colorbar=dict(title="Total Runs")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Analysis:**
- These matches form the extreme right tail of the scoring distribution.
- All significantly exceed the tournament average total score.
- High totals occur across multiple venues and stages, not limited to a single condition.

**Conclusion:**
- A small number of ultra-high scoring matches disproportionately shape IPL 2025’s scoring narrative.
- Such games expose bowling vulnerabilities, particularly during middle and death overs.
- Controlling run flow in these scenarios becomes a decisive tactical factor.
    """)

# =========================
# POINTS TABLE + BATTING
# =========================
elif section == "batting":
    st.header("📈 Points Table & Batting Analysis")

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
# BOWLING + ADVANCED INSIGHTS
# =========================
elif section == "bowling":
    st.header("🎯 Bowling Analysis & Advanced Insights")

    eco = bowlers.sort_values("ECO").head(10)
    fig = px.bar(
        eco,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Top Economical Bowlers"
    )
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

    death = bowlers[bowlers["OVR"] > 15]
    fig = px.scatter(
        death,
        x="ECO",
        y="SR",
        color="Team",
        hover_name="Player Name",
        title="Death Overs: Strike Rate vs Economy"
    )
    st.plotly_chart(fig, use_container_width=True)

    impact = bowlers[bowlers["OVR"] < 16].head(10)
    fig = px.bar(
        impact,
        x="Player Name",
        y="WKT",
        color="Team",
        title="Impact Bowlers"
    )
    st.plotly_chart(fig, use_container_width=True)

    underrated = (
        bowlers[(bowlers["MAT"] < 8) & (bowlers["MAT"] > 3)]
        .sort_values("ECO")
        .head(5)
    )

    fig = px.bar(
        underrated,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Underrated Bowlers"
    )
    st.plotly_chart(fig, use_container_width=True)
