import plotly.express as px
import pandas as pd

def create_trend_chart(df, region):
    """Generate a line chart for COVID-19 cases trend in the selected region."""
    filtered_df = df[df['region'] == region]
    fig = px.line(filtered_df, x='date', y='cases', 
                  title=f'COVID-19 Cases Trend in {region}',
                  labels={'cases': 'Number of Cases', 'date': 'Date'})
    return fig

def create_forecast_chart(forecast_df, region, method="Prophet"):
    """
    Generate a chart to visualize forecasted cases.
    
    Parameters:
      forecast_df (DataFrame): Forecasted data with dates and predicted values.
      region (str): The region being forecasted.
      method (str): The forecasting method used (for title annotation).
    """
    if method == "Prophet":
        # Prophet forecast uses 'ds' and 'yhat'
        x_col, y_col = 'ds', 'yhat'
    else:
        # ARIMA forecast uses our custom columns
        x_col, y_col = 'ds', 'yhat'
    fig = px.line(forecast_df, x=x_col, y=y_col, 
                  title=f'30-Day Forecast of COVID-19 Cases in {region} ({method})',
                  labels={y_col: 'Predicted Cases', x_col: 'Date'})
    return fig

def create_summary_stats(df, region):
    """
    Create summary statistics for the selected region.
    Returns a dictionary with total cases, average cases, and max daily cases.
    """
    filtered_df = df[df['region'] == region]
    total = filtered_df['cases'].sum()
    average = filtered_df['cases'].mean()
    max_daily = filtered_df['cases'].max()
    return {"Total Cases": total, "Average Daily Cases": round(average, 2), "Max Daily Cases": max_daily}

def summary_card(stats):
    """
    Create an HTML card to display summary statistics using Dash Bootstrap Components.
    """
    import dash_bootstrap_components as dbc
    card_items = [dbc.ListGroupItem(f"{key}: {value}") for key, value in stats.items()]
    card = dbc.Card([
        dbc.CardHeader("Summary Statistics"),
        dbc.ListGroup(card_items, flush=True)
    ], style={"width": "18rem"})
    return card
