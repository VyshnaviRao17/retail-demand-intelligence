# src/anomalies.py

import pandas as pd

def detect_anomalies():
    df = pd.read_csv("data/sales.csv")
    df['rolling_7'] = df['sales'].rolling(7).mean()
    df['anomaly'] = abs(df['sales'] - df['rolling_7']) > (0.30 * df['rolling_7'])

    # Remove NaN from first 7 rows
    df = df.dropna()

    return df[df['anomaly'] == True]
