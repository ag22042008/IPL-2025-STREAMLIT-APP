import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="IPL 2025 Analysis", layout="wide")
st.title("🏏 IPL 2025 Interactive Analysis Dashboard")

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
st.sidebar.header("📊 Choose Analysis")

analysis_type = st.sidebar.selectbox(
    "Select Analysis Category",
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
if analysis_type == "Dataset Overview":
    st.header("📊 Dataset Overview")

    total_matches = ipl2025["match_id"].nunique()
    teams = pd.unique(ipl2025[["team1", "team2"]].values.ravel())
    venues = ipl2025["venue"].unique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Matches", total_matches)
    c2.metric("Teams", len(teams))
    c3.metric("Venues", len(venues))

    st.write("Teams:", teams)
    st.write("Venues:", venues)

# =====================================================
# VENUE & TEAM ANALYSIS
# =====================================================
elif analysis_type == "Venue & Team Analysis":
    plot_choice = st.sidebar.radio(
        "Select Plot",
        ["Matches per Venue", "Matches per Team"]
    )

    if plot_choice == "Matches per Venue":
        st.subheader("🏟️ Matches Played per Venue")
        venue_counts = ipl2025["venue"].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(y=venue_counts.index, x=venue_counts.values, ax=ax)
        st.pyplot(fig)

    else:
        st.subheader("👥 Matches Played per Team")
        team_counts = ipl2025["team1"].value_counts() + ipl2025["team2"].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=team_counts.index, y=team_counts.values, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

# =====================================================
# RUNS & MATCH ANALYSIS
# =====================================================
elif analysis_type == "Runs & Match Analysis":
    plot_choice = st.sidebar.radio(
        "Select Plot",
        [
            "Runs Distribution",
            "High Scoring Matches (200+)"
        ]
    )

    ipl2025["total_score_per_match"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

    if plot_choice == "Runs Distribution":
        st.subheader("🔥 Distribution of Total Runs per Match")
        fig, ax = plt.subplots()
        sns.histplot(ipl2025["total_score_per_match"], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

    else:
        st.subheader("🔥 High Scoring Matches (200+ Runs)")
        high = ipl2025[ipl2025["total_score_per_match"] >= 200]
        st.metric("Number of High Scoring Matches", len(high))
        st.dataframe(high[["match_id", "team1", "team2", "total_score_per_match"]])

# =====================================================
# POINTS TABLE
# =====================================================
elif analysis_type == "Points Table":
    st.header("📈 IPL 2025 Points Table")

    ipl5 = ipl2025.drop(ipl2025.tail(4).index)
    points = ipl5[ipl5["match_winner"] != 0]["match_winner"].value_counts() * 2

    ties = ipl5[ipl5["match_winner"] == 0]
    for _, row in ties.iterrows():
        points[row["team1"]] = points.get(row["team1"], 0) + 1
        points[row["team2"]] = points.get(row["team2"], 0) + 1

    points = points.sort_values(ascending=False)
    st.dataframe(points)

    fig, ax = plt.subplots()
    sns.barplot(x=points.index, y=points.values, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =====================================================
# BATTING ANALYSIS
# =====================================================
elif analysis_type == "Batting Analysis":
    st.header("🏏 Batting Analysis")

    bat = ipl2025[ipl2025["top_scorer"] != 0][["top_scorer", "highscore"]]
    bat = bat.groupby("top_scorer").max().sort_values("highscore", ascending=False).head(10)

    fig, ax = plt.subplots()
    sns.barplot(y=bat.index, x=bat["highscore"], ax=ax)
    st.pyplot(fig)

# =====================================================
# BOWLING ANALYSIS
# =====================================================
elif analysis_type == "Bowling Analysis":
    plot_choice = st.sidebar.radio(
        "Select Plot",
        [
            "Top Economical Bowlers",
            "Wickets vs Economy"
        ]
    )

    if plot_choice == "Top Economical Bowlers":
        best_eco = bowlers[["Player Name", "ECO", "Team"]].sort_values("ECO").head(10)
        fig = px.bar(best_eco, y="Player Name", x="ECO", color="ECO")
        st.plotly_chart(fig, use_container_width=True)

    else:
        bowlers2 = bowlers[["Player Name","OVR","ECO","WKT","Team","SR"]]
        fig = px.scatter(
            bowlers2,
            x="WKT",
            y="ECO",
            size="OVR",
            color="Team",
            hover_name="Player Name"
        )
        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ADVANCED BOWLING INSIGHTS
# =====================================================
elif analysis_type == "Advanced Bowling Insights":
    plot_choice = st.sidebar.radio(
        "Select Plot",
        [
            "Strike Rate vs Economy",
            "Impact Bowlers",
            "Underrated Bowlers"
        ]
    )

    if plot_choice == "Strike Rate vs Economy":
        b = bowlers[bowlers["OVR"] > 15]
        fig = px.scatter(b, x="ECO", y="SR", color="Team", hover_name="Player Name")
        st.plotly_chart(fig, use_container_width=True)

    elif plot_choice == "Impact Bowlers":
        impact = bowlers[bowlers["OVR"] < 16][["Player Name","WKT","Team"]].head(10)
        fig = px.bar(impact, x="Player Name", y="WKT", color="Team")
        st.plotly_chart(fig, use_container_width=True)

    else:
        under = bowlers[(bowlers["MAT"] < 8) & (bowlers["MAT"] > 3)]
        under = under.sort_values("ECO").head(5)
        fig, ax = plt.subplots()
        sns.barplot(y=under["Player Name"], x=under["ECO"], ax=ax)
        st.pyplot(fig)
