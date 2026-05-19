# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get max and min payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[

    # Dashboard Title
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie Chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # Payload Range Text
    html.P("Payload range (Kg):"),

    # TASK 3: Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,

        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },

        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter Plot
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])


# TASK 2 CALLBACK
@app.callback(
    Output(component_id='success-pie-chart',
           component_property='figure'),

    Input(component_id='site-dropdown',
          component_property='value')
)

def get_pie_chart(entered_site):

    # CASE 1: ALL sites selected
    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

        return fig

    # CASE 2: Specific site selected
    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {entered_site}'
        )

        return fig


# TASK 4 CALLBACK
@app.callback(
    Output(component_id='success-payload-scatter-chart',
           component_property='figure'),

    [Input(component_id='site-dropdown',
           component_property='value'),

     Input(component_id='payload-slider',
           component_property='value')]
)

def update_scatter_chart(selected_site, payload_range):

    # Payload range
    low, high = payload_range

    # Filter dataframe based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # CASE 1: ALL sites selected
    if selected_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs Launch Success for All Sites'
        )

        return fig

    # CASE 2: Specific site selected
    else:

        site_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Launch Success for {selected_site}'
        )

        return fig


# Run the app
if __name__ == '__main__':
    app.run()