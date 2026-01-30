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
# DATASET OVERVIEW
# =========================
if section == "dataset":
    st.header("📊 Dataset Overview")

    total_matches = ipl2025["match_id"].nunique()
    teams = pd.unique(ipl2025[["team1", "team2"]].values.ravel())
    venues = ipl2025["venue"].unique()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Matches", total_matches)
    m2.metric("Total Teams", len(teams))
    m3.metric("Total Venues", len(venues))

    st.subheader("📈 Tournament Progression (Matches Over Time)")

    prog = ipl2025.sort_values("match_id").reset_index(drop=True)
    prog["match_number"] = range(1, len(prog) + 1)

    fig = px.line(
        prog,
        x="match_number",
        y="match_number",
        markers=True,
        title="IPL 2025 Tournament Progression"
    )

    fig.update_traces(line=dict(color="#00E5FF", width=4))
    fig.update_layout(
        xaxis_title="Match Sequence",
        yaxis_title="Cumulative Matches"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- IPL 2025 followed a smooth and evenly paced schedule.
- No abnormal clustering or gaps in match scheduling were observed.
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
- Majority of matches fall in high scoring range 
- The mean confirms batting-friendly conditions throughout IPL 2025.
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
-  Jasprit Bumrah stand out for exceptional run control.
- Economy rate remains a key selection metric for bowlers.
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
- Highly expensive bowlers are rarely used for long spells.
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
- Karn Sharma and Will Jacks provide high impact in short spells.
- Such bowlers are valuable tactical assets.
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
- Jaydev Unadkat stands out as the most underrated bowler.
- Several part-time bowlers delivered strong economy when given opportunities.
    """)
