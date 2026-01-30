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

# 🔴 Image name EXACTLY as you specified
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
# TOP NAVIGATION BUTTONS
# =========================
c1, c2, c3 = st.columns(3)
section = None

if c1.button("📊 Dataset Overview"):
    section = "dataset"
if c2.button("🎯 Bowling Analysis"):
    section = "bowling"
if c3.button("🧠 Advanced Insights"):
    section = "advanced"

# =========================
# DATASET OVERVIEW (TEXT ONLY)
# =========================
if section == "dataset":
    st.header("📊 Dataset Overview & Structural Analysis")

    st.markdown("""
### 📁 Match-Level Dataset Analysis

The IPL 2025 match dataset consists of **74 matches and 22 columns**, covering league and playoff fixtures.
It integrates numerical, categorical, and text-based attributes capturing teams, venues, toss decisions, innings performance, and match outcomes.

Numerical fields such as innings scores, wickets lost, balls remaining, and highest individual scores enable quantitative evaluation.
Categorical features like stage, toss decision, and match result support outcome-based comparisons.
Missing values appear mainly in wide-ball statistics and award-related columns, reflecting real match conditions such as abandoned or no-result games.
Overall, the dataset is structurally rich and suitable for match-flow and strategic analysis.
    """)

    st.markdown("""
### 🎯 Bowling Dataset Analysis

The bowling dataset includes **108 bowlers across 13 attributes**, with no missing values.
It contains wickets, overs, economy rate, strike rate, bowling average, and match appearances.

Indicators like four- and five-wicket hauls highlight match-defining spells, while player and team identifiers add contextual depth.
The dataset is well-suited for identifying economical bowlers, death-over specialists, impact bowlers, and underrated performers.
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
- Economy rate remains a critical selection metric for bowlers.
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
- Karn Sharma and Will Jacks deliver high impact despite limited overs.
- Such bowlers provide tactical flexibility in T20 cricket.
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
