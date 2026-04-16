AI Learning Navigator - Student Performance Analysis System

📌 Project Overview

This project is an AI-driven system designed to analyze student performance and provide personalized learning recommendations.

The system uses data analysis, machine learning (K-Means clustering), and rule-based AI logic to identify performance levels, detect skill gaps, and generate personalized learning paths and actionable insights.

An interactive dashboard is developed using Streamlit to visualize data and support real-time decision-making.

👥 Team Members

Syed Azmath
Mohammed Afnan S

📂 Project Files

learning_navigator_report.pdf
→ Final project report containing methodology, analysis, and conclusions
dashboard.py
→ Streamlit-based interactive dashboard with AI recommendations and visualizations
eda.ipynb
→ Exploratory Data Analysis notebook for understanding data patterns and relationships
README.md
→ Project documentation and execution guide
student_learning_dataset.xlsx
→ Dataset used for analysis and model building

📊 Key Features

Student performance segmentation using K-Means clustering
(Low Performer, Average (At Risk), High Performer)
Skill gap identification
(Weak Fundamentals, Needs Improvement, Strong)
AI-based recommendation system
Cohort-level insights
Student-level suggestions
Personalized learning path guidance
Interactive dashboard with filters:
Performance level
Score range
Absences
Data visualizations:
Performance distribution (Pie chart)
Category breakdown (Bar chart)
Scatter plots (Study time vs performance, Absences vs performance)
Skill gap analysis
Identification of top-performing and at-risk students

▶️ How to Run

Install dependencies:

pip install pandas numpy scikit-learn plotly streamlit openpyxl

Run dashboard:

python -m streamlit run dashboard.py

Open EDA notebook:

jupyter notebook eda.ipynb

💡 Key Insights

Student performance is influenced by multiple factors such as study time, attendance, and consistency.

Study time shows a positive correlation with performance, while absences impact consistency rather than directly affecting scores.

The “Average (At Risk)” group is the most critical segment, as these students have potential but lack consistency.

🤖 AI-Based Approach

The system integrates clustering, rule-based logic, and data visualization to create a complete decision-support system.

Instead of only analyzing data, it generates actionable insights and recommendations that can help improve student outcomes.

🎯 Conclusion

This project demonstrates how AI and data analytics can be used to transform raw student data into meaningful insights.

By combining machine learning, visualization, and recommendation logic, the system provides a scalable and practical solution for personalized learning and academic improvement.