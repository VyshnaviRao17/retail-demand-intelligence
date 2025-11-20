# src/predict.py

import pandas as pd
import pickle
from datetime import timedelta

def load_model():
    return pickle.load(open("models/model.pkl", "rb"))

def predict_next_14_days():
    df = pd.read_csv("data/sales.csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    model = load_model()

    last_row = df.iloc[-1]
    predictions = []
    dates = []

    lag_1 = last_row['sales']
    lag_7 = df.iloc[-7]['sales']
    rolling_7 = df['sales'].tail(7).mean()

    for i in range(14):
        future_date = last_row['date'] + timedelta(days=i+1)
        dow = future_date.dayofweek

        X = [[lag_1, lag_7, rolling_7, dow]]
        pred = float(model.predict(X)[0])

        predictions.append(pred)
        dates.append(future_date.strftime("%Y-%m-%d"))

        lag_7 = lag_1
        lag_1 = pred
        rolling_7 = (rolling_7 * 6 + pred) / 7

    return dates, predictions
