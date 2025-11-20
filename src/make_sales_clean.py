import pandas as pd

# Load your renamed file
df = pd.read_csv("data/sales.csv")

# Keep only Date and Sales
df = df[['Date', 'Sales']]

# Rename columns
df.columns = ['date', 'sales']

# Remove rows with sales = 0 (stores closed)
df = df[df['sales'] > 0]

# Save cleaned file
df.to_csv("data/sales_clean.csv", index=False)

print("✔ Clean file created: data/sales_clean.csv")
