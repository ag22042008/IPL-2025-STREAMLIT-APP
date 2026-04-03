import pandas as pd
import plotly.express as px
import streamlit as st
import base64

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="IPL 2025 Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

set_bg("ChatGPT Image Feb 1, 2026, 10_26_21 AM.png")

# =========================
# LOAD DATA (FIXED)
# =========================
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    bowlers = pd.read_csv("IPL2025Bowlers.csv")

    # SAFE fillna (important fix)
    num_cols = matches.select_dtypes(include=['number']).columns
    str_cols = matches.select_dtypes(include=['object', 'string']).columns

    matches[num_cols] = matches[num_cols].fillna(0)
    matches[str_cols] = matches[str_cols].fillna("Unknown")

    return matches, bowlers

ipl2025, bowlers = load_data()

# =========================
# TITLE
# =========================
st.title("🏏 IPL 2025 Interactive Data Analysis Dashboard")

# =========================
# NAVIGATION
# =========================
st.markdown("### 📍 Navigation")

section = st.radio(
    "Go to",
    ["Dataset", "Toss", "Runs", "Batting", "Bowling"],
    horizontal=True
)

# =========================
# DATASET
# =========================
if section == "Dataset":
    st.header("📊 Dataset Overview & Structural Analysis")

    st.markdown("""
**Match Dataset**
- 74 matches, 22 columns  
- Numerical, categorical & text features  
- Missing values due to no-result matches  

**Bowling Dataset**
- 108 bowlers, 13 attributes  
- Clean dataset with strong reliability  
    """)

# =========================
# TOSS
# =========================
elif section == "Toss":
    st.header("🪙 Toss & Match Results")

    toss = ipl2025["toss_decision"].value_counts().reset_index()
    toss.columns = ["Decision", "Count"]

    fig = px.bar(toss, x="Decision", y="Count", color="Decision")
    st.plotly_chart(fig, use_container_width=True)

    valid = ipl2025[ipl2025["match_winner"] != "Unknown"]

    toss_win = valid[valid["toss_winner"] == valid["match_winner"]]
    win_rate = round(len(toss_win) / len(valid) * 100, 2)

    st.markdown(f"""
**Conclusion**
- Toss advantage exists but is not decisive  
- Toss winners won **{win_rate}%** matches  
    """)

# =========================
# RUNS
# =========================
elif section == "Runs":
    st.header("🔥 Top 10 Highest Scoring Matches")

    ipl2025["total_score"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

    top10 = ipl2025.sort_values("total_score", ascending=False).head(10)

    fig = px.bar(
        top10,
        x="match_id",
        y="total_score",
        color="total_score",
        color_continuous_scale="Inferno",
        hover_data=["team1", "team2", "venue", "stage"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Analysis**
- Extreme high-scoring matches dominate  
- Far above tournament average  

**Conclusion**
- Death over bowling is the key differentiator  
    """)

# =========================
# BATTING
# =========================
elif section == "Batting":
    st.header("📈 Points & Batting Analysis")

    valid = ipl2025[ipl2025["match_winner"] != "Unknown"]

    pts = valid["match_winner"].value_counts() * 2
    pts = pts.reset_index()
    pts.columns = ["Team", "Points"]

    fig = px.bar(pts, x="Team", y="Points", color="Points")
    st.plotly_chart(fig, use_container_width=True)

    bat = (
        ipl2025[ipl2025["top_scorer"] != "Unknown"]
        .groupby("top_scorer")["highscore"]
        .max()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(bat, y="top_scorer", x="highscore", color="highscore")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# BOWLING
# =========================
elif section == "Bowling":
    st.header("🎯 Bowling Analysis & Insights")

    eco = bowlers.sort_values("ECO").head(10)

    fig = px.bar(eco, y="Player Name", x="ECO", color="Team")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Conclusion:** Bumrah & Unadkat dominate run control")

    fig = px.scatter(
        bowlers,
        x="WKT",
        y="ECO",
        size="OVR",
        color="Team",
        hover_name="Player Name"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Conclusion:** Expensive bowlers rarely sustain spells")

    team_eco = bowlers.groupby("Team")["ECO"].mean().reset_index()

    fig = px.bar(team_eco, x="Team", y="ECO", color="ECO")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Conclusion:** MI & RCB show strong bowling balance")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("### 🚀 Built by Aditya Gupta")
