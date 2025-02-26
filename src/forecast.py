from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

def forecast_cases_prophet(df, region, periods=30):
    """
    Forecast COVID-19 cases for a selected region using Prophet.
    Returns a DataFrame with 'ds', 'yhat', and confidence intervals.
    """
    region_df = df[df['region'] == region].copy()
    region_df = region_df.rename(columns={'date': 'ds', 'cases': 'y'})
    
    model = Prophet(daily_seasonality=True)
    model.fit(region_df[['ds', 'y']])
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

def forecast_cases_arima(df, region, periods=30):
    """
    Forecast COVID-19 cases for a selected region using an ARIMA model.
    Returns a DataFrame with 'ds', 'yhat', and confidence intervals.
    """
    region_df = df[df['region'] == region].copy()
    region_df = region_df.set_index('date')
    ts = region_df['cases']
    
    model = ARIMA(ts, order=(1, 1, 1))
    model_fit = model.fit()
    forecast_obj = model_fit.get_forecast(steps=periods)
    forecast_df = forecast_obj.summary_frame()
    # Create a date range for forecasted values
    forecast_df['ds'] = pd.date_range(start=ts.index[-1] + pd.Timedelta(days=1), periods=periods, freq='D')
    forecast_df.rename(columns={'mean': 'yhat', 'mean_ci_lower': 'yhat_lower', 'mean_ci_upper': 'yhat_upper'}, inplace=True)
    return forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
