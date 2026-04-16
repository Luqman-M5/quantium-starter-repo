import dash
from dash import dcc, html, Input, Output
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
df = df.sort_values(by="date")

# Define the layout of the app
app.layout = html.Div(
    className="app-container",
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Soul Foods Analytics", className="title"),
                html.P("Analyzing the impact of the January 15, 2021 Pink Morsel price increase.", className="subtitle")
            ]
        ),
        html.Div(
            className="control-panel",
            children=[
                html.Label("Filter by Region:", className="control-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All Regions", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inputClassName="radio-input",
                    labelClassName="radio-label",
                    className="radio-group"
                )
            ]
        ),
        html.Div(
            className="graph-container",
            children=[
                dcc.Graph(id="sales-chart")
            ]
        )
    ]
)

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    # Create a line chart of sales over time by region
    fig = px.line(
        filtered_df, 
        x="date", 
        y="sales", 
        color="region" if selected_region == "all" else None,
        title="Pink Morsel Sales by Region" if selected_region == "all" else f"Pink Morsel Sales in {selected_region.capitalize()} Region",
        labels={
            "sales": "Sales (USD)",
            "date": "Date",
            "region": "Region"
        }
    )

    # Add a vertical line for the price increase on Jan 15, 2021
    fig.add_vline(x="2021-01-15", line_width=2, line_dash="dash", line_color="#ff4b4b")

    # Add a text annotation for the price increase
    fig.add_annotation(
        x="2021-01-15", 
        y=filtered_df['sales'].max() if not filtered_df.empty else 2000, 
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        ax=-60,
        ay=-30,
        font=dict(color="#ff4b4b", size=13, family="'Outfit', sans-serif")
    )

    # Update layout for better aesthetics inside the dark theme
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Inter', sans-serif", size=13, color="#e2e8f0"),
        title_font=dict(size=22, family="'Outfit', sans-serif", color="#ffffff"),
        xaxis=dict(showgrid=False, linecolor="#4a5568", title_font=dict(size=14)),
        yaxis=dict(gridcolor="#2d3748", linecolor="#4a5568", title_font=dict(size=14)),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=""
        )
    )

    # If displaying a single line (region selected), style it with an accent color
    if selected_region != "all":
        fig.update_traces(line=dict(color="#00d2ff", width=3))

    return fig

if __name__ == '__main__':
    app.run(debug=True)
