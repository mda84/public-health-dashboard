import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from data_loader import load_data
from visualization import create_trend_chart, create_forecast_chart, create_summary_stats, summary_card
from forecast import forecast_cases_prophet, forecast_cases_arima

# Pre-load data (using CSV by default; change source as needed)
df = load_data(source="csv")
regions = sorted(df['region'].unique())

# Demo credentials (for production, use a secure authentication system)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # For deployment

# Layouts for Login and Dashboard
login_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Please Log In"), width=12)
    ], justify="center", className="mt-5"),
    dbc.Row([
        dbc.Col(
            dbc.FormGroup([
                dbc.Label("Username"),
                dbc.Input(id="login-username", placeholder="Enter username", type="text"),
            ]), width=4
        )
    ], justify="center", className="mb-3"),
    dbc.Row([
        dbc.Col(
            dbc.FormGroup([
                dbc.Label("Password"),
                dbc.Input(id="login-password", placeholder="Enter password", type="password"),
            ]), width=4
        )
    ], justify="center", className="mb-3"),
    dbc.Row([
        dbc.Col(
            dbc.Button("Login", id="login-button", color="primary", block=True),
            width=4
        )
    ], justify="center"),
    html.Div(id="login-message", className="text-danger mt-3"),
    dcc.Store(id="login-status", data=False)
], fluid=True)

dashboard_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Interactive Public Health Dashboard"), className="mb-3")
    ]),
    dbc.Tabs(id="tabs", active_tab="tab-eda", children=[
        dbc.Tab(label="Exploratory Analysis", tab_id="tab-eda"),
        dbc.Tab(label="Forecasting", tab_id="tab-forecast")
    ], className="mb-4"),
    html.Div(id="tab-content")
], fluid=True)

# Main app layout: login first, then conditionally show dashboard
app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Store(id="stored-login", storage_type="session"),
    html.Div(id="page-content")
])

# Callback to show login or dashboard based on login state
@app.callback(
    Output("page-content", "children"),
    Input("stored-login", "data")
)
def display_page(is_logged_in):
    if is_logged_in:
        return dashboard_layout
    return login_layout

# Callback for login button
@app.callback(
    [Output("stored-login", "data"),
     Output("login-message", "children")],
    Input("login-button", "n_clicks"),
    [State("login-username", "value"),
     State("login-password", "value")],
    prevent_initial_call=True
)
def verify_login(n_clicks, username, password):
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return True, ""
    return False, "Invalid credentials. Please try again."

# Callback to render content based on selected tab
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "tab-eda":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id='region-dropdown-eda',
                    options=[{'label': r, 'value': r} for r in regions],
                    value=regions[0],
                    clearable=False
                ), width=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(id='summary-stats', width=3),
                dbc.Col(dcc.Graph(id='trend-chart'), width=9)
            ])
        ])
    elif active_tab == "tab-forecast":
        return dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id='region-dropdown-forecast',
                    options=[{'label': r, 'value': r} for r in regions],
                    value=regions[0],
                    clearable=False
                ), width=4),
                dbc.Col(dcc.RadioItems(
                    id='forecast-method',
                    options=[
                        {'label': 'Prophet', 'value': 'Prophet'},
                        {'label': 'ARIMA', 'value': 'ARIMA'}
                    ],
                    value='Prophet',
                    inline=True
                ), width=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col(dcc.Graph(id='forecast-chart'), width=12)
            ])
        ])
    return "No content available for this tab."

# Callback for Exploratory Analysis: update trend chart and summary stats
@app.callback(
    [Output('trend-chart', 'figure'),
     Output('summary-stats', 'children')],
    Input('region-dropdown-eda', 'value')
)
def update_trend_chart(selected_region):
    fig = create_trend_chart(df, selected_region)
    stats = create_summary_stats(df, selected_region)
    card = summary_card(stats)
    return fig, card

# Callback for Forecasting: update forecast chart based on method selected
@app.callback(
    Output('forecast-chart', 'figure'),
    [Input('region-dropdown-forecast', 'value'),
     Input('forecast-method', 'value')]
)
def update_forecast_chart(selected_region, method):
    if method == "Prophet":
        forecast_df = forecast_cases_prophet(df, selected_region)
    else:
        forecast_df = forecast_cases_arima(df, selected_region)
    return create_forecast_chart(forecast_df, selected_region, method)

if __name__ == '__main__':
    app.run_server(debug=True)
