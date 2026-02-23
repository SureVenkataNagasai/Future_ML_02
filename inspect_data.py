import pandas as pd

# Load the dataset
try:
    df = pd.read_csv(r'c:\Users\Admin\OneDrive\Desktop\Task3\Resume\Resume.csv')
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:\n", df.head())
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
except Exception as e:
    print(f"Error loading CSV: {e}")
