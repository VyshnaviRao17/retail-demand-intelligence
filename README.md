# retail-demand-intelligence
AI Retail Demand Intelligence System
Sales Forecasting | Anomaly Detection | Inventory Optimization
1. Overview

The AI Retail Demand Intelligence System is an end-to-end machine learning solution designed to support retail businesses in demand forecasting, anomaly detection, and inventory planning.
It uses a LightGBM regression model, feature-engineered time-series data, and an interactive Streamlit dashboard to provide actionable insights.

The system forecasts daily sales for the next 14 days, identifies unusual behavior in historical sales patterns, and recommends optimal stock levels based on predicted demand.

2. Key Features
• 14-Day Sales Forecasting

A trained LightGBM model predicts future sales using lag features, rolling averages, and day-of-week patterns.

• Anomaly Detection

Automated detection of abnormal sales activity using rolling window deviation. Identifies unexpected spikes or drops in sales.

• Inventory (Stock) Recommendation

Calculates:

Predicted demand for the next 7 days

Safety stock (15%)

Total recommended inventory

• Business Insights

Provides:

Highest and lowest sales days

Monthly average sales trends

Overall demand direction

• Interactive Dashboard

Developed with Streamlit for clear visualization of forecasts, anomalies, and insights.

3. Dataset

The model is trained using a cleaned subset of the Rossmann Store Sales Dataset (Kaggle), containing:

date, sales


The dataset is preprocessed to remove closed-store days and ensure chronological order.

4. Machine Learning Approach
4.1 Data Preprocessing

Conversion of date fields into datetime format

Sorting chronologically

Removal of sales=0 days

Cleaning missing values

4.2 Feature Engineering

Final features used for the model:

lag_1: Sales from the previous day

lag_7: Sales from the same weekday of the previous week

rolling_7: 7-day moving average

day_of_week: Encoded weekday (0–6)

These features capture short-term trends, weekly seasonality, and general time-series behavior.

4.3 Model

Algorithm: LightGBM Regressor
Chosen for:

High performance on tabular data

Fast training speed

Low memory usage

Strong results in forecasting competitions

4.4 Forecasting Method

A recursive, multi-step prediction method is used:

Predict next day’s sales

Feed prediction as input to next step

Repeat for 14 days

This method ensures continuity and realistic forecasting patterns.

5. Project Structure
retail-demand-intelligence/
│
├── app/
│   └── streamlit_app.py        # Streamlit dashboard
│
├── src/
│   ├── train.py                # Model training script
│   ├── predict.py              # 14-day forecasting logic
│   └── anomalies.py            # Anomaly detection logic
│
├── data/
│   └── sales.csv               # Cleaned dataset
│
├── models/
│   └── model.pkl               # Trained LightGBM model
│
├── README.md
└── requirements.txt

6. Installation & Setup
Step 1: Clone the Repository
git clone https://github.com/VyshnaviRao17/retail-demand-intelligence.git
cd retail-demand-intelligence

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Run the Dashboard
streamlit run app/streamlit_app.py

7. Dashboard Overview
7.1 Forecast

Displays a 14-day future sales prediction graph.

7.2 Anomalies

Shows abnormal days detected through deviation analysis.

7.3 Stock Advisor

Provides:

Forecasted demand for next week

Recommended safety stock

Total inventory requirement

7.4 Insights

Provides key business patterns:

Highest and lowest sales days

Monthly averages

Overall demand trend

8. Future Enhancements

Per-store forecasting support

Product-level forecasting

CSV upload for external datasets

REST API for model inference

Deployment on cloud platforms

Automated retraining pipeline

9. Contributors
Role	Member
Machine Learning Engineer	Vyshnavi Rao
Frontend / Dashboard Developer	Om Panhale

10. License

This project is intended for educational and hackathon purposes.
