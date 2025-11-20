# train.py
# You will add ML training code here
# train.py
import pandas as pd
import lightgbm as lgb
import pickle

def load_data():
    df = pd.read_csv("data/sales.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

def feature_engineering(df):
    df = df.sort_values('date')
    df['lag_1'] = df['sales'].shift(1)
    df['lag_7'] = df['sales'].shift(7)
    df['day_of_week'] = df['date'].dt.dayofweek
    df['rolling_7'] = df['sales'].rolling(7).mean()
    df = df.dropna()
    return df

def train_model():
    df = load_data()
    df = feature_engineering(df)
    
    X = df[['lag_1', 'lag_7', 'day_of_week', 'rolling_7']]
    y = df['sales']

    model = lgb.LGBMRegressor()
    model.fit(X, y)

    pickle.dump(model, open("models/model.pkl", "wb"))
    print("Model saved successfully!")

if __name__ == "__main__":
    train_model()
