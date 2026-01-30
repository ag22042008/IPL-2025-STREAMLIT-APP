import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="IPL 2025 Interactive Analysis",
    layout="wide"
)

st.title("🏏 IPL 2025 Interactive Data Analysis Dashboard")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    bowlers = pd.read_csv("IPL2025Bowlers.csv")
    matches.fillna(0, inplace=True)
    return matches, bowlers

ipl2025, bowlers = load_data()

# =====================================================
# SIDEBAR CONTROLS
# =====================================================
st.sidebar.header("📊 Select Analysis")

analysis = st.sidebar.selectbox(
    "Choose Analysis Category",
    [
        "Dataset Overview",
        "Venue & Team Analysis",
        "Runs & Match Analysis",
        "Points Table",
        "Batting Analysis",
        "Bowling Analysis",
        "Advanced Bowling Insights"
    ]
)

# =====================================================
# DATASET OVERVIEW
# =====================================================
if analysis == "Dataset Overview":
    st.header("📊 Dataset Overview")

    total_matches = ipl2025["match_id"].nunique()
    teams = pd.unique(ipl2025[["team1","team2"]].values.ravel())
    venues = ipl2025["venue"].unique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Matches", total_matches)
    c2.metric("Total Teams", len(teams))
    c3.metric("Total Venues", len(venues))

    st.subheader("Matches per Season (ID Frequency)")
    fig = px.histogram(
        ipl2025,
        x="match_id",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# VENUE & TEAM ANALYSIS
# =====================================================
elif analysis == "Venue & Team Analysis":

    plot = st.sidebar.radio(
        "Choose Plot",
        ["Matches per Venue", "Matches per Team"]
    )

    if plot == "Matches per Venue":
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

    else:
        team_counts = (
            ipl2025["team1"].value_counts()
            + ipl2025["team2"].value_counts()
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

# =====================================================
# RUNS & MATCH ANALYSIS
# =====================================================
elif analysis == "Runs & Match Analysis":

    plot = st.sidebar.radio(
        "Choose Plot",
        ["Runs Distribution", "High Scoring Matches"]
    )

    ipl2025["total_score"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

    if plot == "Runs Distribution":
        fig = px.histogram(
            ipl2025,
            x="total_score",
            nbins=25,
            color_discrete_sequence=px.colors.sequential.Plasma,
            title="Distribution of Total Runs per Match"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
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

# =====================================================
# POINTS TABLE
# =====================================================
elif analysis == "Points Table":

    ipl5 = ipl2025.drop(ipl2025.tail(4).index)
    points = ipl5[ipl5["match_winner"] != 0]["match_winner"].value_counts() * 2

    ties = ipl5[ipl5["match_winner"] == 0]
    for _, row in ties.iterrows():
        points[row["team1"]] = points.get(row["team1"],0) + 1
        points[row["team2"]] = points.get(row["team2"],0) + 1

    points = points.sort_values(ascending=False).reset_index()
    points.columns = ["Team","Points"]

    fig = px.bar(
        points,
        x="Team",
        y="Points",
        color="Points",
        color_continuous_scale="Viridis",
        title="IPL 2025 Points Table"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# BATTING ANALYSIS
# =====================================================
elif analysis == "Batting Analysis":

    bat = ipl2025[ipl2025["top_scorer"] != 0][["top_scorer","highscore"]]
    bat = bat.groupby("top_scorer").max().sort_values("highscore", ascending=False).head(10)
    bat = bat.reset_index()

    fig = px.bar(
        bat,
        y="top_scorer",
        x="highscore",
        color="highscore",
        color_continuous_scale="Rainbow",
        title="Top Individual Scores (IPL 2025)"
    )
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# BOWLING ANALYSIS
# =====================================================
elif analysis == "Bowling Analysis":

    plot = st.sidebar.radio(
        "Choose Plot",
        ["Top Economical Bowlers", "Wickets vs Economy"]
    )

    if plot == "Top Economical Bowlers":
        eco = bowlers.sort_values("ECO").head(10)

        fig = px.bar(
            eco,
            y="Player Name",
            x="ECO",
            color="Team",
            title="Top Economical Bowlers"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
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

# =====================================================
# ADVANCED BOWLING INSIGHTS
# =====================================================
elif analysis == "Advanced Bowling Insights":

    plot = st.sidebar.radio(
        "Choose Plot",
        [
            "Strike Rate vs Economy",
            "Impact Bowlers",
            "Underrated Bowlers"
        ]
    )

    if plot == "Strike Rate vs Economy":
        b = bowlers[bowlers["OVR"] > 15]

        fig = px.scatter(
            b,
            x="ECO",
            y="SR",
            color="Team",
            hover_name="Player Name",
            title="Strike Rate vs Economy Rate"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif plot == "Impact Bowlers":
        impact = bowlers[bowlers["OVR"] < 16].head(10)

        fig = px.bar(
            impact,
            x="Player Name",
            y="WKT",
            color="Team",
            title="Impact Bowlers (Fewer Overs, More Wickets)"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        under = bowlers[(bowlers["MAT"] < 8) & (bowlers["MAT"] > 3)]
        under = under.sort_values("ECO").head(5)

        fig = px.bar(
            under,
            y="Player Name",
            x="ECO",
            color="Team",
            title="Underrated Bowlers (Low ECO, Fewer Matches)"
        )
        st.plotly_chart(fig, use_container_width=True)
