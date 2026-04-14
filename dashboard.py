import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Learning Navigator",
    page_icon="🎯",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_excel("student_learning_dataset.xlsx")

# ---------------------------
# PREPROCESSING
# ---------------------------
df["test_preparation"] = df["test_preparation"].fillna("Not Completed")
df["test_preparation"] = df["test_preparation"].str.lower()

# ---------------------------
# CLUSTERING
# ---------------------------
features = df[[
    "study_time_weekly",
    "absences",
    "math_score",
    "reading_score",
    "writing_score"
]]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(scaled_features)

# ---------------------------
# LABEL CLUSTER
# ---------------------------
def label_cluster(cluster):
    if cluster == 0:
        return "Low Performer"
    elif cluster == 1:
        return "High Performer"
    else:
        return "Average (At Risk)"

df["performance_level"] = df["cluster"].apply(label_cluster)

# ---------------------------
# SKILL GAP
# ---------------------------
def skill_gap(row):
    if row["math_score"] < 50:
        return "Weak Fundamentals"
    elif row["math_score"] < 75:
        return "Needs Improvement"
    else:
        return "Strong"

df["skill_gap"] = df.apply(skill_gap, axis=1)

# ---------------------------
# LEARNING PATH
# ---------------------------
def learning_path(row):
    if row["performance_level"] == "Low Performer":
        return "Start with basics"
    elif row["performance_level"] == "Average (At Risk)":
        return "Improve consistency"
    else:
        return "Advanced learning"

df["learning_path"] = df.apply(learning_path, axis=1)

# ---------------------------
# CAREER ALIGNMENT
# ---------------------------
def career_alignment(row):
    if row["performance_level"] == "High Performer" and row["math_score"] > 85:
        return "Data Science / Engineering"
    elif row["performance_level"] == "Average (At Risk)":
        return "Needs consistency"
    elif row["math_score"] > 70:
        return "Analytical roles"
    else:
        return "Focus on basics"

df["career_path"] = df.apply(career_alignment, axis=1)

# ---------------------------
# ACTION PLAN
# ---------------------------
def action_plan(row):
    if row["performance_level"] == "Low Performer":
        return "High Priority"
    elif row["performance_level"] == "Average (At Risk)":
        return "Medium Priority"
    else:
        return "Low Priority"

df["action_plan"] = df.apply(action_plan, axis=1)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
# 🎯 AI Learning Navigator Dashboard
### AI-Based Student Performance & Personalization System
---
""")

# ---------------------------
# KPI CARDS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(df))
col2.metric("Avg Score", round(df["math_score"].mean(), 2))
col3.metric("High Performers", (df["performance_level"] == "High Performer").sum())
col4.metric("At Risk Students", (df["performance_level"] == "Average (At Risk)").sum())

# ---------------------------
# SIDEBAR FILTERS (ADVANCED)
# ---------------------------
st.sidebar.title("🔍 Filter Options")

performance_filter = st.sidebar.selectbox(
    "Performance Level",
    ["All", "Low Performer", "Average (At Risk)", "High Performer"]
)

gender_filter = st.sidebar.selectbox(
    "Gender",
    ["All"] + list(df["gender"].unique())
)

course_filter = st.sidebar.selectbox(
    "Course",
    ["All"] + list(df["course_id"].unique())
)

score_range = st.sidebar.slider("Score Range", 0, 100, (0, 100))
absence_range = st.sidebar.slider("Absence Range", 0, 20, (0, 20))

search_id = st.sidebar.text_input("Search Student ID")

# ---------------------------
# FILTER LOGIC
# ---------------------------
df_filtered = df.copy()

if performance_filter != "All":
    df_filtered = df_filtered[df_filtered["performance_level"] == performance_filter]

if gender_filter != "All":
    df_filtered = df_filtered[df_filtered["gender"] == gender_filter]

if course_filter != "All":
    df_filtered = df_filtered[df_filtered["course_id"] == course_filter]

df_filtered = df_filtered[
    (df_filtered["math_score"] >= score_range[0]) &
    (df_filtered["math_score"] <= score_range[1]) &
    (df_filtered["absences"] >= absence_range[0]) &
    (df_filtered["absences"] <= absence_range[1])
]

if search_id:
    df_filtered = df_filtered[df_filtered["student_id"].astype(str) == search_id]

# ---------------------------
# SMART INSIGHT
# ---------------------------
st.subheader("🧠 Smart Insight")

avg_score = df_filtered["math_score"].mean()

if avg_score > 80:
    st.success("Overall performance is strong 🚀")
elif avg_score > 60:
    st.warning("Moderate performance ⚠️")
else:
    st.error("Low performance ❌ Intervention needed")

# ---------------------------
# GRAPH STYLE
# ---------------------------
sns.set_style("whitegrid")

# ---------------------------
# CHART ROW 1
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Student Distribution")
    fig1, ax1 = plt.subplots()
    sns.countplot(x="performance_level", data=df_filtered, palette="Set2", ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Category Breakdown")
    fig2, ax2 = plt.subplots()
    df_filtered["performance_level"].value_counts().plot(
        kind="bar",
        color=["#4CAF50", "#FFC107", "#F44336"],
        ax=ax2
    )
    st.pyplot(fig2)

# ---------------------------
# CHART ROW 2
# ---------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Study Time vs Score")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(
        x="study_time_weekly",
        y="math_score",
        hue="performance_level",
        palette="Set1",
        data=df_filtered,
        ax=ax3
    )
    st.pyplot(fig3)

with col4:
    st.subheader("Absences vs Score")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(
        x="absences",
        y="math_score",
        hue="performance_level",
        palette="coolwarm",
        data=df_filtered,
        ax=ax4
    )
    st.pyplot(fig4)

# ---------------------------
# CHART ROW 3
# ---------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("Test Preparation Impact")
    fig5, ax5 = plt.subplots()
    sns.boxplot(
        x="test_preparation",
        y="math_score",
        palette="pastel",
        data=df_filtered,
        ax=ax5
    )
    st.pyplot(fig5)

with col6:
    st.subheader("Correlation Heatmap")
    fig6, ax6 = plt.subplots()
    sns.heatmap(
        df_filtered.select_dtypes(include="number").corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax6
    )
    st.pyplot(fig6)

# ---------------------------
# TABLES
# ---------------------------
st.subheader("🏆 Top Performers")
st.dataframe(df_filtered.sort_values(by="math_score", ascending=False).head(10))

st.subheader("⚠️ At Risk Students")
st.dataframe(df_filtered[df_filtered["performance_level"] == "Average (At Risk)"].head(10))

# ---------------------------
# MAIN TABLE
# ---------------------------
st.subheader("📋 Student Insights")
st.dataframe(df_filtered[[
    "math_score",
    "performance_level",
    "skill_gap",
    "learning_path",
    "career_path",
    "action_plan"
]])

# ---------------------------
# DOWNLOAD
# ---------------------------
csv = df_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    "student_analysis.csv",
    "text/csv"
)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
---
👨‍💻 Developed by **Syed Azmath & Mohammed Afnan S**  
AI Learning Navigator Project
""")