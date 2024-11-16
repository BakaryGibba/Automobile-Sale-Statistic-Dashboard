 #!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown menu options and year list
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
year_list = [i for i in range(1980, 2024)]

# Layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'left', 'color': '#503D36', 'font-size': 24}),
    
    # Dropdowns for report type and year
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value='Select-year',
        placeholder='Select a year'
    )),
    
    # Container for displaying graphs
    html.Div(id='output-container', className='chart-grid')
])

# Callbacks
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(report_type, input_year):
    if report_type == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuation over recession period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales over Recession Period")
        )

        # Plot 2: Average vehicles sold by type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Type during Recessions")
        )

        # Plot 3: Expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title="Expenditure Share by Vehicle Type")
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Sales'},
                          title="Effect of Unemployment Rate on Sales by Vehicle Type")
        )

        return [
            html.Div([
                html.Div(children=R_chart1, style={'width': '50%', 'display': 'inline-block'}),
                html.Div(children=R_chart2, style={'width': '50%', 'display': 'inline-block'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div(children=R_chart3, style={'width': '50%', 'display': 'inline-block'}),
                html.Div(children=R_chart4, style={'width': '50%', 'display': 'inline-block'})
            ], style={'display': 'flex'})
        ]

    elif input_year and report_type == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile sales over the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales Over Time')
        )

        # Plot 2: Monthly Automobile sales within the year
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Monthly Automobile Sales')
        )

        # Plot 3: Average vehicles sold by type within the year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f'Average Vehicles Sold by Type in {input_year}')
        )

        # Plot 4: Advertisement expenditure by vehicle type within the year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title="Advertising Expenditure by Vehicle Type")
        )

        return [
            html.Div([
                html.Div(children=Y_chart1, style={'width': '50%', 'display': 'inline-block'}),
                html.Div(children=Y_chart2, style={'width': '50%', 'display': 'inline-block'})
            ], style={'display': 'flex'}),
            html.Div([
                html.Div(children=Y_chart3, style={'width': '50%', 'display': 'inline-block'}),
                html.Div(children=Y_chart4, style={'width': '50%', 'display': 'inline-block'})
            ], style={'display': 'flex'})
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
