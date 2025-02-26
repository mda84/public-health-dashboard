import os
import pandas as pd
import requests

def load_data(source="csv", file_path="../data/covid_data.csv"):
    """
    Load and clean public health data.
    
    Parameters:
      source (str): 'csv' to load from file or 'api' to fetch from a remote API.
      file_path (str): File path for CSV data.
    
    Returns:
      DataFrame: Cleaned data with date as datetime and outliers removed.
    """
    if source == "csv":
        df = pd.read_csv(file_path)
    elif source == "api":
        df = fetch_data_from_api()
    else:
        raise ValueError("Unsupported data source.")

    # Convert date column to datetime and sort data
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.sort_values('date')
    df.fillna(method='ffill', inplace=True)
    
    # Remove outliers in 'cases'
    threshold = df['cases'].quantile(0.99)
    df = df[df['cases'] <= threshold]
    return df

def fetch_data_from_api(save_file=False, file_path="../data/covid_data.csv"):
    """
    Fetch public health data from an external API.
    
    For demonstration, this function uses a sample COVID-19 historical data API.
    """
    url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
    response = requests.get(url)
    data = response.json()
    # Transform the API response into a DataFrame.
    df = pd.DataFrame({
        'date': list(data['cases'].keys()),
        'cases': list(data['cases'].values()),
        'deaths': list(data['deaths'].values()),
        'recovered': list(data['recovered'].values())
    })
    # For uniformity with our project, add a dummy 'region' column.
    df['region'] = "Global"

    # Save the DataFrame to CSV if requested.
    if save_file:
        # Ensure the directory exists.
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

    return df
