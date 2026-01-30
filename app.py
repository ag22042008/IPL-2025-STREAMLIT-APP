import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

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

The IPL 2025 match-level dataset consists of **74 matches and 22 columns**, representing a complete league season including both league-stage and playoff fixtures. 
The dataset integrates **categorical, numerical, and text-based attributes**, covering match context such as participating teams, venues, tournament stage, toss outcomes, innings performance, and result information.

Numerical variables including *first and second innings scores, wickets lost, balls remaining,* and *highest individual score* enable quantitative performance analysis, while categorical fields such as *stage, toss decision,* and *match result* support outcome-based comparisons. 
Several columns contain missing values—particularly *wide-ball statistics, match winner,* and *individual awards*—which naturally arise due to abandoned matches, no-result games, or unavailable player attribution. 
Overall, the dataset is structurally rich and well-suited for analyzing scoring patterns, match flow, toss impact, and result dynamics across IPL 2025.
    """)

    st.markdown("""
### 🎯 Bowling Dataset Analysis

The bowling dataset comprises **108 bowlers across 13 performance attributes**, providing a detailed representation of individual bowling contributions throughout the tournament. 
It includes key numerical metrics such as *wickets taken, matches played, innings bowled, overs delivered, runs conceded, bowling average, economy rate,* and *strike rate*, enabling multi-dimensional evaluation of bowler effectiveness.

Additional categorical indicators such as *four-wicket and five-wicket hauls* highlight match-winning spells, while descriptive fields including *player name, team,* and *best bowling figures* add contextual depth. 
Notably, the bowling dataset contains **no missing values**, ensuring high data completeness and analytical reliability. 
This makes it particularly suitable for advanced analysis aimed at identifying economical bowlers, death-over specialists, impact bowlers with limited overs, and underrated performers who deliver strong efficiency despite fewer opportunities.
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
**Conclusion:**
- Most matches fall within the **300–420 total runs** range.
- The mean confirms consistently **batting-friendly conditions** during IPL 2025.
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
- Economy rate remains a key metric for bowler selection and trust.
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
- Bowlers trusted with more overs generally maintain a balanced economy.
- Highly expensive bowlers are rarely given extended spells.
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
- Low economy combined with strong strike rate is extremely valuable.
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
- Karn Sharma and Will Jacks deliver high impact in short bowling spells.
- Such bowlers are valuable tactical assets in modern T20 cricket.
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
- Several part-time bowlers delivered strong economy when given opportunities.
    """)
