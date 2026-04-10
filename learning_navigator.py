import pandas as pd

def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

def main():
    df = load_data("student_learning_dataset.xlsx")
    
    print("📊 Dataset Preview:")
    print(df.head())
    
    print("\n📌 Dataset Info:")
    print(df.info())
    
    print("\n📈 Summary Statistics:")
    print(df.describe())

if __name__ == "__main__":
    main()