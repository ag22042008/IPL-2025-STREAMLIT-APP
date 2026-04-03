import pandas as pd
import plotly.express as px
import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="IPL 2025 Analytics Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA (CLEAN + SAFE)
# =========================
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    bowlers = pd.read_csv("IPL2025Bowlers.csv")

    # Handle missing values safely
    num_cols = matches.select_dtypes(include=['number']).columns
    str_cols = matches.select_dtypes(include=['object', 'string']).columns

    matches[num_cols] = matches[num_cols].fillna(0)
    matches[str_cols] = matches[str_cols].fillna("Unknown")

    return matches, bowlers

ipl, bowlers = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.title("🔍 Filters")

teams = sorted(set(ipl["team1"]).union(set(ipl["team2"])))
selected_team = st.sidebar.selectbox("Select Team", ["All"] + teams)

venues = ["All"] + sorted(ipl["venue"].unique())
selected_venue = st.sidebar.selectbox("Select Venue", venues)

# Apply filters
filtered = ipl.copy()

if selected_team != "All":
    filtered = filtered[
        (filtered["team1"] == selected_team) |
        (filtered["team2"] == selected_team)
    ]

if selected_venue != "All":
    filtered = filtered[filtered["venue"] == selected_venue]

# =========================
# TITLE
# =========================
st.title("🏏 IPL 2025 Data Analytics Dashboard")

st.markdown("""
### 📌 Project Overview
- End-to-end IPL 2025 data analysis
- Includes EDA, insights & performance metrics
- Built using Streamlit + Plotly
""")

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", len(filtered))
col2.metric("Total Teams", len(teams))
col3.metric("Venues", filtered["venue"].nunique())

# =========================
# TOSS ANALYSIS
# =========================
st.subheader("🪙 Toss Decision Analysis")

toss = filtered["toss_decision"].value_counts().reset_index()
toss.columns = ["Decision", "Count"]

fig = px.pie(toss, names="Decision", values="Count", hole=0.4)
st.plotly_chart(fig, use_container_width=True)

# Toss impact
valid_matches = filtered[filtered["match_winner"] != "Unknown"]
toss_win = valid_matches[
    valid_matches["toss_winner"] == valid_matches["match_winner"]
]

if len(valid_matches) > 0:
    win_rate = round(len(toss_win) / len(valid_matches) * 100, 2)
else:
    win_rate = 0

st.info(f"Toss winners win **{win_rate}%** of matches.")

# =========================
# HIGH SCORING MATCHES
# =========================
st.subheader("🔥 High Scoring Matches")

filtered["total_score"] = (
    filtered["first_ings_score"] + filtered["second_ings_score"]
)

top_matches = filtered.sort_values("total_score", ascending=False).head(10)

fig = px.bar(
    top_matches,
    x="match_id",
    y="total_score",
    color="total_score",
    hover_data=["team1", "team2", "venue"],
    title="Top 10 Matches by Total Score"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# POINTS TABLE
# =========================
st.subheader("📈 Points Table")

valid = filtered[filtered["match_winner"] != "Unknown"]

points = valid["match_winner"].value_counts() * 2
points = points.reset_index()
points.columns = ["Team", "Points"]

fig = px.bar(points, x="Team", y="Points", color="Points")
st.plotly_chart(fig, use_container_width=True)

# =========================
# TOP BATSMEN
# =========================
st.subheader("🏏 Top Batting Performances")

bat = (
    filtered[filtered["top_scorer"] != "Unknown"]
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
    title="Top Individual Scores"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# BOWLING ANALYSIS
# =========================
st.subheader("🎯 Bowling Analysis")

eco = bowlers.sort_values("ECO").head(10)

fig = px.bar(
    eco,
    y="Player Name",
    x="ECO",
    color="Team",
    title="Best Economy Bowlers"
)
st.plotly_chart(fig, use_container_width=True)

# Scatter
fig = px.scatter(
    bowlers,
    x="WKT",
    y="ECO",
    size="OVR",
    color="Team",
    hover_name="Player Name",
    title="Wickets vs Economy"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# ADVANCED INSIGHTS
# =========================
st.subheader("📊 Advanced Insights")

team_eco = bowlers.groupby("Team")["ECO"].mean().reset_index()

fig = px.bar(
    team_eco,
    x="Team",
    y="ECO",
    color="ECO",
    title="Team-wise Bowling Economy"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("### 🚀 Built by Aditya Gupta")
st.markdown("Streamlit • Plotly • Data Analytics • Machine Learning Ready")
