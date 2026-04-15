AI Learning Navigator - Student Performance Analysis System

--------------------------------------------------

📌 Project Description

AI Learning Navigator is a data-driven system designed to analyze student performance and provide personalized learning recommendations.

The system uses machine learning, clustering, and rule-based logic to:
- Segment students into performance groups
- Identify skill gaps
- Generate personalized learning paths
- Suggest career alignment
- Provide actionable improvement plans

--------------------------------------------------

👥 Team Members

- Syed Azmath
- Mohammed Afnan S

--------------------------------------------------

⚙️ Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn (KMeans Clustering)
- Streamlit (Dashboard)
- Jupyter Notebook (EDA)

--------------------------------------------------

📂 Project Files

- eda.ipynb → Exploratory Data Analysis (EDA) with visual insights
- learning_navigator.py → Core logic and analysis system
- dashboard.py → Interactive Streamlit dashboard
- student_learning_dataset.xlsx → Dataset
- learning_navigator_report.pdf → Project report
- README.md → Documentation
- README.md → Project documentation

--------------------------------------------------

📊 EDA (Exploratory Data Analysis)

The EDA notebook (`eda.ipynb`) is used to understand data patterns and relationships.

It includes:
- Distribution analysis of test preparation
- Study time vs performance analysis
- Absence impact analysis
- Correlation heatmap
- Pairplot for multi-variable relationships

These insights form the foundation for clustering and recommendation logic.

--------------------------------------------------

📊 Dashboard Features

An interactive dashboard was built using Streamlit to visualize and explore student data in real-time.

Key Features:
- Performance-based filtering (Low, Average, High)
- Filters for gender, course, score range, and absences
- Student search by ID
- Dynamic charts and visualizations
- Correlation heatmap
- Identification of top-performing and at-risk students
- Downloadable dataset

--------------------------------------------------

▶️ How to Run the Project

1. Install required libraries:

   pip install pandas matplotlib seaborn scikit-learn streamlit openpyxl

2. Run the dashboard:

   python -m streamlit run dashboard.py

3. Open EDA notebook:

   jupyter notebook eda.ipynb

4. (Optional) Run script:

   python learning_navigator.py

--------------------------------------------------

📊 Output

The system provides:

- Student segmentation (Low Performer, Average, High Performer)
- Skill gap analysis
- Personalized learning paths
- Career alignment recommendations
- Action plans
- Interactive dashboard visualization

--------------------------------------------------

💡 Key Insight

Student performance is multi-dimensional and influenced by study habits, attendance, and preparation.

Consistency plays a more important role than raw scores, and the "Average (At Risk)" group represents the highest opportunity for improvement.

--------------------------------------------------

🎯 Conclusion

This project demonstrates how AI-driven analysis combined with interactive visualization can transform raw educational data into actionable insights.

The integration of EDA, clustering, personalization, and dashboard systems makes the solution scalable, practical, and suitable for real-world applications.

--------------------------------------------------
