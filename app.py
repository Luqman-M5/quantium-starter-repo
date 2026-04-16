import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

# Initialize Dash application
app = dash.Dash(__name__)

# Load and process the data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'formatted_output.csv')

# Load the dataset
df = pd.read_csv(DATA_FILE)

# Sort by date
df = df.sort_values(by="date")

# Create a line chart of sales over time by region
fig = px.line(
    df, 
    x="date", 
    y="sales", 
    color="region",
    title="Pink Morsel Sales by Region",
    labels={
        "sales": "Sales (USD)",
        "date": "Date",
        "region": "Region"
    }
)

# Add a vertical line for the price increase on Jan 15, 2021
fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="red")

# Add a text annotation for the price increase
fig.add_annotation(
    x="2021-01-15", 
    y=df['sales'].max(), 
    text="Price Increase (Jan 15, 2021)",
    showarrow=True,
    arrowhead=1,
    ax=-100,
    ay=0
)

# Update layout for better aesthetics
fig.update_layout(
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="#ffffff",
    font=dict(family="Arial, sans-serif", size=12, color="#333333"),
    title_font=dict(size=20)
)

# Define the layout of the app
app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f4f8",
        "padding": "20px",
        "minHeight": "100vh"
    },
    children=[
        html.H1(
            "Soul Foods: Pink Morsel Sales Visualizer",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "10px"
            }
        ),
        html.P(
            "Visualizing the impact of the January 15, 2021 price increase on Pink Morsel sales.",
            style={
                "textAlign": "center",
                "color": "#7f8c8d",
                "fontSize": "16px",
                "marginBottom": "30px"
            }
        ),
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                "maxWidth": "1200px",
                "margin": "0 auto"
            },
            children=[
                dcc.Graph(
                    id="sales-line-chart",
                    figure=fig
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
