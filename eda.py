# AI Learning Navigator - Student Performance Analysis

# ---------------------------
# 1. Import Libraries
# ---------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ---------------------------
# 2. Load Dataset
# ---------------------------
df = pd.read_excel("student_learning_dataset.xlsx")

# ---------------------------
# 3. Data Cleaning
# ---------------------------
df["test_preparation"] = df["test_preparation"].fillna("Not Completed")
df["test_preparation"] = df["test_preparation"].str.lower()

# ---------------------------
# 4. Feature Engineering
# ---------------------------
df["high_absence"] = df["absences"] > 5

# ---------------------------
# 5. Exploratory Data Analysis (EDA)
# ---------------------------

# Learning Style Distribution
sns.countplot(x="learning_style", data=df)
plt.title("Learning Style Distribution")
plt.show()

# Study Time vs Math Score
sns.scatterplot(x="study_time_weekly", y="math_score", data=df)
plt.title("Study Time vs Math Score")
plt.show()

# Absences vs Math Score
sns.scatterplot(
    x="absences",
    y="math_score",
    hue="high_absence",
    data=df,
    alpha=0.6
)
plt.title("Absences vs Math Score (High vs Low Absence)")
plt.show()

# Test Preparation vs Math Score
sns.boxplot(x="test_preparation", y="math_score", data=df)
plt.title("Test Preparation vs Math Score")
plt.show()

# Correlation Heatmap
numeric_df = df.select_dtypes(include=["number"])
plt.figure(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# ---------------------------
# 6. Recommendation System
# ---------------------------
def recommend(student):

    test_prep = student["test_preparation"]

    if student["math_score"] < 50 and student["absences"] > 10:
        return "High Risk: Improve attendance and review fundamentals"

    elif student["math_score"] < 50:
        return "Revise the basics and practice more questions"

    elif student["absences"] > 10:
        return "Reduce absences and maintain consistency"

    elif test_prep != "completed":
        return "Complete test preparation to improve performance"

    else:
        return "Keep up the good work and try advanced problems"


df["recommendation"] = df.apply(recommend, axis=1)

# ---------------------------
# 7. Clustering (KMeans)
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
# 8. Label Clusters
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
# 9. AI-Based Action Plan
# ---------------------------
def final_action(row):

    if row["performance_level"] == "Low Performer":
        return "High Priority: Provide basic support and increase study time"

    elif row["performance_level"] == "Average (At Risk)":
        return "Medium Priority: Improve consistency and reduce absences"

    else:
        return "Low Priority: Encourage advanced learning"


df["action_plan"] = df.apply(final_action, axis=1)

# ---------------------------
# 10. Final Output
# ---------------------------
print("\n===== FINAL STUDENT ANALYSIS OUTPUT =====\n")

print(df[[
    "math_score",
    "study_time_weekly",
    "performance_level",
    "recommendation",
    "action_plan"
]].head(10))