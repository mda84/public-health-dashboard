# Public Health Data Analysis Dashboard – Enhanced Edition

## Overview
This project provides an interactive dashboard for analyzing and forecasting public health data (using COVID-19 case data as an example). It demonstrates advanced data cleaning, exploratory analysis, and forecasting using two techniques (Prophet and ARIMA). The dashboard also includes a simple login mechanism for access control, supports dynamic data sources, and is ready for containerized deployment with CI/CD integration.

## Features
- **Data Ingestion & Cleaning:**  
  - Load data from a local CSV or from an external API.
  - Handle missing values, outlier removal, and type conversions.
- **Exploratory Data Analysis:**  
  - Interactive visualizations (line charts, bar charts, and summary statistics).
- **Forecasting:**  
  - Forecast using Prophet (with uncertainty bounds).
  - Alternate forecast using ARIMA.
- **User Authentication:**  
  - Simple login form (demo credentials: admin/password) to restrict access.
- **Enhanced UI/UX:**  
  - Multi-tab layout with separate views for analysis and forecasting.
  - Summary statistics cards with key metrics.
- **Deployment & CI/CD:**  
  - Dockerfile for containerized deployment.
  - GitHub Actions workflow for automated testing and build.

## Project Structure
```
public-health-dashboard/
├── README.md
├── requirements.txt
├── Dockerfile
├── .github/
│    └── workflows/
│        └── ci.yml # CI/CD pipeline configuration
├── data/
│    └── covid_data.csv # Sample dataset
├── notebooks/
│    ├── EDA_Notebook.ipynb # Exploratory analysis and data cleaning
│    └── Forecasting_Notebook.ipynb # Experimentation with forecasting methods
└── src/
     ├── data_loader.py # Data ingestion and cleaning with multiple sources
     ├── visualization.py # Visualization functions and summary stats
     ├── forecast.py # Forecasting modules (Prophet and ARIMA)
     └── app.py # Main Dash app with login, multi-tab layout, and callbacks
```
## Installation
**Clone the Repository:**
```
   git clone https://github.com/yourusername/public-health-dashboard.git
   cd public-health-dashboard
```
Set Up Virtual Environment and Install Dependencies:
```
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
```
Run the Dashboard:
```   
   python src/app.py
   Open your browser at http://127.0.0.1:8050.
```
## Docker Deployment
Build and run the Docker container with:
```   
   docker build -t public-health-dashboard .
   docker run -p 8050:8050 public-health-dashboard
```
## Notebooks
EDA_Notebook.ipynb: Walks through data loading, cleaning, and exploratory analysis with visualizations.
Forecasting_Notebook.ipynb: Demonstrates forecasting using Prophet, parameter tuning, and visualizes forecast outputs.

## License
This project is licensed under the MIT License.

## Contact
For questions, collaboration, or contributions, please contact dorkhah9@gmail.com
