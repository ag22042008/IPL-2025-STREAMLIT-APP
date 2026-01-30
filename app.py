import pandas as pd
import numpy as np
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
            background: rgba(0, 0, 0, 0.6);
            z-index: -1;
        }}
        h1, h2, h3, h4, p {{
            color: #ffffff;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("assets/ipl_bg.png")

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
# TOP NAVIGATION BUTTONS
# =========================
c1, c2, c3, c4 = st.columns(4)
section = None

if c1.button("📊 Dataset Overview"):
    section = "dataset"
if c2.button("🔥 Runs Analysis"):
    section = "runs"
if c3.button("🎯 Bowling Analysis"):
    section = "bowling"
if c4.button("🧠 Advanced Insights"):
    section = "advanced"

# =========================
# DATASET OVERVIEW (TEXT ONLY)
# =========================
if section == "dataset":
    st.header("📊 Dataset Overview & Structural Analysis")

    st.markdown("""
### 📁 Match-Level Dataset Analysis

The IPL 2025 match-level dataset consists of **74 matches and 22 columns**, representing a complete season covering league and playoff stages. 
It integrates **numerical, categorical, and text-based attributes**, capturing match context such as teams, venues, stage, toss decisions, innings performance, and match outcomes.

Numerical fields including *innings scores, wickets lost, balls remaining,* and *highest individual score* enable quantitative performance analysis, while categorical variables such as *stage, toss decision,* and *match result* allow outcome-driven comparisons. 
Several columns contain missing values, primarily in *wide-ball statistics, match winner,* and *individual awards*, which naturally occur due to abandoned matches, no-results, or unavailable player attribution.
Overall, the dataset is well-structured and suitable for analyzing scoring patterns, match flow, toss impact, and result dynamics in IPL 2025.
    """)

    st.markdown("""
### 🎯 Bowling Dataset Analysis

The bowling dataset includes **108 bowlers across 13 attributes**, offering a comprehensive view of individual bowling performance throughout the tournament. 
It contains key numerical indicators such as *wickets, overs bowled, runs conceded, economy rate, strike rate,* and *bowling average*, enabling multi-dimensional evaluation of effectiveness.

Categorical markers like *four-wicket and five-wicket hauls* highlight match-defining spells, while descriptive fields such as *player name, team,* and *best bowling figures* provide contextual clarity. 
Importantly, the bowling dataset contains **no missing values**, ensuring high analytical reliability. 
This makes it well-suited for advanced insights such as identifying economical bowlers, death-over specialists, impact bowlers, and underrated performers.
    """)

# =========================
# RUNS ANALYSIS
# =========================
elif section == "runs":
    st.header("🔥 Runs & Match Analysis")

    ipl2025["total_score"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

    st.subheader("📊 Distribution of Total Runs per Match")

    fig = px.histogram(
        ipl2025,
        x="total_score",
        nbins=12,
        marginal="rug",
        color_discrete_sequence=["#3F51B5"],
        title="Distribution of Total Runs per Match"
    )

    mean_runs = ipl2025["total_score"].mean()

    fig.add_vline(
        x=mean_runs,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean ≈ {round(mean_runs,1)}",
        annotation_position="top"
    )

    fig.update_layout(
        xaxis_title="Total Runs per Match",
        yaxis_title="Number of Matches"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Analysis & Conclusion:**
- Most matches fall in the **300–420 total runs** range.
- The right-skewed distribution confirms a **batting-dominant IPL 2025**.
- High-scoring matches significantly influence the overall mean.
    """)

    # -------------------------
    # TOP 10 HIGH SCORING MATCHES
    # -------------------------
    st.subheader("🔥 Top 10 Highest Scoring Matches (IPL 2025)")

    top10_matches = (
        ipl2025
        .sort_values("total_score", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top10_matches,
        x="match_id",
        y="total_score",
        color="total_score",
        color_continuous_scale="Inferno",
        hover_data={
            "team1": True,
            "team2": True,
            "venue": True,
            "stage": True
        },
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
- These matches represent the extreme right tail of the run distribution.
- All exceed the tournament average total score, confirming aggressive batting trends.
- High scores occur across multiple venues and stages, not confined to a single condition.

**Conclusion:**
- A small set of ultra-high scoring matches disproportionately drives the overall scoring trend.
- Such matches increase pressure on bowling units, especially in the death overs.
- Controlling run flow in these games becomes a decisive tactical factor.
    """)

# =========================
# BOWLING ANALYSIS
# =========================
elif section == "bowling":
    st.header("🎯 Bowling Analysis")

    st.subheader("Top Economical Bowlers (Ascending Economy Rate)")

    eco = bowlers.sort_values("ECO").head(10)

    fig = px.bar(
        eco,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Top Economical Bowlers"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jaydev Unadkat and Jasprit Bumrah stand out for exceptional run control.
- Economy rate remains a critical metric for bowler selection.
    """)

    st.subheader("⚖️ Wickets vs Economy Rate")

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

    st.markdown("""
**Conclusion:**
- Bowlers trusted with higher workloads generally maintain controlled economy.
- Highly expensive bowlers are rarely used for extended spells.
    """)

# =========================
# ADVANCED INSIGHTS
# =========================
elif section == "advanced":
    st.header("🧠 Advanced Bowling Insights")

    st.subheader("Strike Rate vs Economy (Death Overs)")

    death = bowlers[bowlers["OVR"] > 15]

    fig = px.scatter(
        death,
        x="ECO",
        y="SR",
        color="Team",
        hover_name="Player Name",
        title="Strike Rate vs Economy Rate"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jasprit Bumrah emerges as the most reliable death-over bowler.
- Low economy combined with strong strike rate is extremely rare and valuable.
    """)

    st.subheader("💥 Impact Bowlers (Fewer Overs, More Wickets)")

    impact = bowlers[bowlers["OVR"] < 16].head(10)

    fig = px.bar(
        impact,
        x="Player Name",
        y="WKT",
        color="Team",
        title="Impact Bowlers"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Karn Sharma and Will Jacks deliver high impact despite limited overs.
- Such bowlers provide tactical flexibility in T20 formats.
    """)

    st.subheader("🧠 Underrated Bowlers")

    underrated = bowlers[(bowlers["MAT"] < 8) & (bowlers["MAT"] > 3)]
    underrated = underrated.sort_values("ECO").head(5)

    fig = px.bar(
        underrated,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Underrated Bowlers (Low Economy, Fewer Matches)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jaydev Unadkat stands out as the most underrated bowler of IPL 2025.
- Several rotational bowlers delivered strong efficiency when given opportunities.
    """)
