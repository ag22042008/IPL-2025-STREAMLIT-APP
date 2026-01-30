
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="IPL 2025 Analysis", layout="wide")
st.title("🏏 IPL 2025 Full Analysis Dashboard")

@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    bowlers = pd.read_csv("IPL2025Bowlers.csv")
    matches.fillna(0, inplace=True)
    return matches, bowlers

ipl2025, bowlers = load_data()

st.header("📊 Dataset Understanding")

total_matches = ipl2025["match_id"].nunique()
teams = pd.unique(ipl2025[["team1", "team2"]].values.ravel())
venues = ipl2025["venue"].unique()

c1, c2, c3 = st.columns(3)
c1.metric("Total Matches", total_matches)
c2.metric("Total Teams", len(teams))
c3.metric("Total Venues", len(venues))

st.subheader("Teams")
st.write(teams)

st.subheader("Venues")
st.write(venues)

st.header("🏟️ Matches Played per Venue")
iplvenue = ipl2025["venue"].value_counts()
fig, ax = plt.subplots()
sns.barplot(y=iplvenue.index, x=iplvenue.values, ax=ax)
st.pyplot(fig)

st.header("👥 Matches Played per Team")
iplteam = ipl2025["team1"].value_counts() + ipl2025["team2"].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=iplteam.index, y=iplteam.values, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.header("🔥 Runs & Match Overview")
ipl2025["total_score_per_match"] = ipl2025["first_ings_score"] + ipl2025["second_ings_score"]

st.metric("Total Runs Scored", int(ipl2025["total_score_per_match"].sum()))
st.metric("Average Runs per Match", round(ipl2025["total_score_per_match"].mean(), 2))

fig, ax = plt.subplots()
sns.histplot(ipl2025["total_score_per_match"], bins=20, kde=True, ax=ax)
st.pyplot(fig)

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

st.header("🎯 Bowling Analysis")
best_eco = bowlers[["Player Name", "ECO", "Team"]].sort_values("ECO").head(10)
st.dataframe(best_eco)

fig = px.bar(best_eco, y="Player Name", x="ECO", color="ECO")
st.plotly_chart(fig, use_container_width=True)

st.header("⚖️ Wickets vs Economy Rate")
bowlers2 = bowlers[["Player Name","OVR","ECO","WKT","Team","SR"]]
fig = px.scatter(bowlers2, x="WKT", y="ECO", size="OVR", color="Team", hover_name="Player Name")
st.plotly_chart(fig, use_container_width=True)
