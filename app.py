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
# TOP NAVIGATION
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

The IPL 2025 match dataset consists of **74 matches and 22 columns**, capturing complete league and playoff information.
It integrates numerical, categorical, and text-based attributes describing teams, venues, toss decisions, innings performance, and match outcomes.

Numerical fields such as innings scores, wickets lost, balls remaining, and highest individual scores enable quantitative analysis.
Categorical features like stage, toss decision, and match result support outcome-based comparisons.
Missing values appear mainly in wide-ball statistics and award-based columns, reflecting real match conditions such as abandoned or no-result games.
Overall, the dataset is structurally rich and suitable for advanced match-flow and scoring analysis.
    """)

    st.markdown("""
### 🎯 Bowling Dataset Analysis

The bowling dataset contains **108 bowlers across 13 attributes**, with no missing values.
It includes wickets, overs, economy rate, strike rate, bowling average, and match appearances, enabling multi-dimensional performance evaluation.

Indicators like four- and five-wicket hauls highlight match-winning spells, while player and team identifiers provide contextual clarity.
The dataset is ideal for identifying economical bowlers, death-over specialists, impact bowlers, and underrated performers.
    """)

# =========================
# RUNS ANALYSIS
# =========================
elif section == "runs":
    st.header("🔥 Runs & Match Analysis")

    ipl2025["total_score"] = (
        ipl2025["first_ings_score"] + ipl2025["second_ings_score"]
    )

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

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Most matches fall in the **300–420 run range**, indicating batting-friendly conditions.
- High-scoring matches strongly influence the overall average.
    """)

    st.subheader("🔥 Top 10 Highest Scoring Matches")

    top10 = ipl2025.sort_values("total_score", ascending=False).head(10)

    fig = px.bar(
        top10,
        x="match_id",
        y="total_score",
        color="total_score",
        color_continuous_scale="Inferno",
        hover_data=["team1", "team2", "venue", "stage"],
        title="Top 10 Highest Scoring Matches – IPL 2025"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- These matches form the extreme right tail of the scoring distribution.
- They occurred across different venues and stages, not limited to one condition.
- Such games place extreme pressure on bowling units, especially at the death.
    """)

# =========================
# BOWLING ANALYSIS
# =========================
elif section == "bowling":
    st.header("🎯 Bowling Analysis")

    eco = bowlers.sort_values("ECO").head(10)

    fig = px.bar(
        eco,
        y="Player Name",
        x="ECO",
        color="Team",
        title="Top Economical Bowlers (Ascending Economy Rate)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Conclusion:**
- Jaydev Unadkat and Jasprit Bumrah stand out for exceptional run control.
- Economy rate remains a key selection metric.
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
- Bowlers trusted with more overs tend to maintain controlled economy.
- Highly expensive bowlers are rarely used for extended spells.
    """)

# ===============
