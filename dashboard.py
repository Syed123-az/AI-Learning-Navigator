import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="AI Learning Navigator", layout="wide")

# ---------------------------
# CLEAN CSS (NO BREAKING UI)
# ---------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
}

/* Center title properly */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 20px;
    background: linear-gradient(90deg,#22c55e,#38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Glass cards */
.glass {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* FIX TAB TEXT COLOR */
button[data-baseweb="tab"] {
    color: #e2e8f0 !important;   /* light text */
    font-weight: 500;
}

/* ACTIVE TAB COLOR */
button[aria-selected="true"] {
    color: #22c55e !important;   /* green highlight */
    border-bottom: 2px solid #22c55e;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# THEME
# ---------------------------
PLOTLY_THEME = dict(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font=dict(color="#e2e8f0")
)

COLORS = {
    "High Performer": "#22c55e",
    "Average (At Risk)": "#f59e0b",
    "Low Performer": "#ef4444"
}

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("student_learning_dataset.xlsx")

    df["avg_score"] = (df["math_score"] + df["reading_score"] + df["writing_score"]) / 3

    features = df[["study_time_weekly","absences","math_score","reading_score","writing_score"]]
    scaled = StandardScaler().fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled)

    cluster_means = df.groupby("cluster")["avg_score"].mean().sort_values()
    labels = {
        cluster_means.index[0]: "Low Performer",
        cluster_means.index[1]: "Average (At Risk)",
        cluster_means.index[2]: "High Performer"
    }

    df["performance_level"] = df["cluster"].map(labels)

    df["skill_gap"] = df["math_score"].apply(
        lambda x: "Weak Fundamentals" if x < 50 else ("Needs Improvement" if x < 75 else "Strong")
    )

    return df

df = load_data()

# ---------------------------
# FILTERS
# ---------------------------
st.sidebar.title("Filters")

perf = st.sidebar.selectbox("Performance", ["All"] + list(df["performance_level"].unique()))
score = st.sidebar.slider("Score", 0, 100, (0, 100))
abs_range = st.sidebar.slider("Absences", 0, int(df["absences"].max()), (0, int(df["absences"].max())))

df_f = df.copy()

if perf != "All":
    df_f = df_f[df_f["performance_level"] == perf]

df_f = df_f[
    (df_f["math_score"] >= score[0]) &
    (df_f["math_score"] <= score[1]) &
    (df_f["absences"] >= abs_range[0]) &
    (df_f["absences"] <= abs_range[1])
]

# ---------------------------
# AI FUNCTIONS
# ---------------------------
def ai_group(df):
    if df.empty:
        return "No data available"

    avg = df["math_score"].mean()

    if avg > 85:
        return "🚀 High performance group — focus on advanced learning"
    elif avg > 70:
        return "📈 Improve consistency and practice"
    elif avg > 50:
        return "⚠️ Strengthen fundamentals"
    else:
        return "❌ Immediate intervention required"

def ai_student(row):
    if row["math_score"] < 50:
        return "Focus on basics"
    if row["absences"] > 8:
        return "Reduce absences"
    if row["math_score"] > 85:
        return "Try advanced problems"
    return "Maintain consistency"

# ---------------------------
# TABS
# ---------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Home","Analysis","Insights","Students"])

# ===========================
# HOME
# ===========================
with tab1:

    st.markdown('<div class="title"> AI Learning Navigator</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.markdown(f'<div class="glass"><h3>Students</h3><h2>{len(df_f)}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="glass"><h3>Avg Score</h3><h2>{round(df_f["math_score"].mean(),2)}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="glass"><h3>Absences</h3><h2>{round(df_f["absences"].mean(),2)}</h2></div>', unsafe_allow_html=True)

    # AI PANEL
    st.subheader("🤖 AI Recommendation")
    st.markdown(f'<div class="glass">{ai_group(df_f)}</div>', unsafe_allow_html=True)

    # CHARTS
    perf_counts = df_f["performance_level"].value_counts().reset_index()
    perf_counts.columns = ["performance_level","count"]

    col4, col5 = st.columns(2)

    fig = px.pie(perf_counts, names="performance_level", values="count", color="performance_level", color_discrete_map=COLORS)
    fig.update_layout(**PLOTLY_THEME)
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>")
    col4.plotly_chart(fig, use_container_width=True)

    fig = px.bar(perf_counts, x="performance_level", y="count", color="performance_level", color_discrete_map=COLORS)
    fig.update_layout(**PLOTLY_THEME)
    fig.update_traces(hovertemplate="Category: %{x}<br>Count: %{y}<extra></extra>")
    col5.plotly_chart(fig, use_container_width=True)

# ===========================
# ANALYSIS
# ===========================
with tab2:

    col1, col2 = st.columns(2)

    fig = px.scatter(df_f, x="study_time_weekly", y="math_score", color="performance_level", color_discrete_map=COLORS)
    fig.update_layout(**PLOTLY_THEME)
    col1.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df_f, x="absences", y="math_score", color="performance_level", color_discrete_map=COLORS)
    fig.update_layout(**PLOTLY_THEME)
    col2.plotly_chart(fig, use_container_width=True)

# ===========================
# INSIGHTS
# ===========================
with tab3:

    skill_counts = df_f["skill_gap"].value_counts().reset_index()
    skill_counts.columns = ["skill_gap","count"]

    fig = px.bar(skill_counts, x="skill_gap", y="count", color="skill_gap")
    fig.update_layout(**PLOTLY_THEME)
    fig.update_traces(hovertemplate="Skill: %{x}<br>Count: %{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)

# ===========================
# STUDENTS
# ===========================
with tab4:

    temp = df_f.copy()
    temp["AI_Recommendation"] = temp.apply(ai_student, axis=1)

    st.dataframe(temp)

    st.subheader("Top Performers")
    st.dataframe(temp.sort_values("math_score", ascending=False).head(10))