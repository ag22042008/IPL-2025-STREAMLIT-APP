import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="IPL 2025 Analysis", layout="wide")
st.title("🏏 IPL 2025 Interactive Data Analysis Dashboard")

@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    bowlers = pd.read_csv("IPL2025Bowlers.csv")
    matches.fillna(0, inplace=True)
    return matches, bowlers

ipl2025, bowlers = load_data()

# =====================================================
# TOP NAVIGATION (BUTTONS, NOT SIDEBAR)
# =====================================================
col1, col2, col3, col4, col5 = st.columns(5)

section = None
if col1.button("📊 Dataset Overview"):
    section = "dataset"
if col2.button("🏟️ Venue & Team"):
    section = "venue"
if col3.button("🔥 Runs Analysis"):
    section = "runs"
if col4.button("🎯 Bowling Analysis"):
    section = "bowling"
if col5.button("🧠 Advanced Insights"):
    section = "advanced"

# =====================================================
# DATASET OVERVIEW
# =====================================================
if section == "dataset":
    st.header("📊 Dataset Overview")

    total_matches = ipl2025["match_id"].nunique()
    teams = pd.unique(ipl2025[["team1","team2"]].values.ravel())
    venues = ipl2025["venue"].unique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Matches", total_matches)
    c2.metric("Total Teams", len(teams))
    c3.metric("Total Venues", len(venues))

    fig = px.histogram(
        ipl2025,
        x="match_id",
        nbins=15,
        color_discrete_sequence=["#00E5FF"],
        title="Matches per Season (ID Frequency)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- IPL 2025 consisted of 74 matches with a balanced league structure.
- Match IDs are evenly distributed, confirming a standard tournament format.
    """)

# =====================================================
# VENUE & TEAM ANALYSIS
# =====================================================
elif section == "venue":
    st.header("🏟️ Venue & Team Analysis")

    venue_counts = ipl2025["venue"].value_counts().reset_index()
    venue_counts.columns = ["Venue","Matches"]

    fig = px.bar(
        venue_counts,
        y="Venue",
        x="Matches",
        color="Matches",
        color_continuous_scale="Turbo",
        title="Matches Played per Venue"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Certain venues hosted significantly more matches, indicating preferred stadiums.
- Scheduling reflects infrastructure capacity and audience demand.
    """)

    team_counts = (
        ipl2025["team1"].value_counts() +
        ipl2025["team2"].value_counts()
    ).reset_index()
    team_counts.columns = ["Team","Matches"]

    fig = px.bar(
        team_counts,
        x="Team",
        y="Matches",
        color="Team",
        title="Matches Played per Team"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- All teams played a similar number of matches.
- Confirms fairness of the league format.
    """)

# =====================================================
# RUNS ANALYSIS
# =====================================================
elif section == "runs":
    st.header("🔥 Runs & Match Analysis")

    ipl2025["total_score"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

    fig = px.histogram(
        ipl2025,
        x="total_score",
        nbins=20,
        color_discrete_sequence=["#3F51B5"],
        title="Distribution of Total Runs per Match"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Majority of matches fall between 300–420 total runs.
- Indicates batting-friendly conditions in IPL 2025.
    """)

    high = ipl2025[ipl2025["total_score"] >= 200]
    fig = px.scatter(
        high,
        x="match_id",
        y="total_score",
        size="total_score",
        color="total_score",
        color_continuous_scale="Inferno",
        hover_data=["team1","team2"],
        title="High Scoring Matches (200+ Runs)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- A significant number of matches crossed 200+ runs.
- High-scoring games became the norm rather than exception.
    """)

# =====================================================
# BOWLING ANALYSIS
# =====================================================
elif section == "bowling":
    st.header("🎯 Bowling Analysis")

    eco = bowlers.sort_values("ECO").head(10)

    fig = px.bar(
        eco,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Top Economical Bowlers (Ascending ECO)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jaydev Unadkat and Jasprit Bumrah stand out for exceptional run control.
- Economy rate remains a critical selection metric for bowlers.
    """)

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
- Bowlers with lower economy generally maintain steady wicket-taking.
- High wicket-takers with poor economy are rarely trusted with more overs.
    """)

# =====================================================
# ADVANCED INSIGHTS
# =====================================================
elif section == "advanced":
    st.header("🧠 Advanced Bowling Insights")

    death = bowlers[bowlers["OVR"] > 15]
    fig = px.scatter(
        death,
        x="ECO",
        y="SR",
        color="Team",
        hover_name="Player Name",
        title="Strike Rate vs Economy (Death Overs)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jasprit Bumrah emerges as the most reliable death-over bowler.
- Low economy combined with strong strike rate is rare and valuable.
    """)

    impact = bowlers[bowlers["OVR"] < 16].head(10)
    fig = px.bar(
        impact,
        x="Player Name",
        y="WKT",
        color="Team",
        title="Impact Bowlers (Fewer Overs, More Wickets)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Karn Sharma and Will Jacks deliver high impact despite limited overs.
- These bowlers provide strong value in short spells.
    """)

    underrated = bowlers[(bowlers["MAT"] < 8) & (bowlers["MAT"] > 3)]
    underrated = underrated.sort_values("ECO").head(5)

    fig = px.bar(
        underrated,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Underrated Bowlers (Low ECO, Fewer Matches)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jaydev Unadkat is the most underrated bowler of IPL 2025.
- Several part-time bowlers maintained excellent economy when given chances.
    """)
