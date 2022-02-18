
import csv
import codecs
import urllib.request
import urllib.error
import sys
import os

import dash                     # pip install dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import plotly.express as px     # pip install plotly==5.2.2
import plotly.graph_objects as go

import pandas as pd             # pip install pandas

"""
API use: visual crossing weather
"""

def concatenate(city):

    StartDate = '2020-12-01'
    EndDate = '2020-12-31'

    ContentType = "csv"

    Include = "days"

    print('')
    print(' - Requesting weather : ')

    ApiQuery = BaseURL + city

    if (len(StartDate)):
        ApiQuery += "/" + StartDate
        if (len(EndDate)):
            ApiQuery += "/" + EndDate

    ApiQuery += "?"

    if (len(UnitGroup)):
        ApiQuery += "&unitGroup=" + UnitGroup

    if (len(ContentType)):
        ApiQuery += "&contentType=" + ContentType

    if (len(Include)):
        ApiQuery += "&include=" + Include

    ApiQuery += "&key=" + ApiKey
    return ApiQuery

def print_():
    print(' - Running query URL: ', ApiQuery)
    print()

    try:
        CSVBytes = urllib.request.urlopen(ApiQuery)
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()

    # Parse the results as CSV
    CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))

    RowIndex = 0

    for Row in CSVText:
        if RowIndex == 0:
            FirstRow = Row
        else:
            print('Weather in ', Row[0], ' on ', Row[1])
            temp=[Row[0]]
            temp.append(Row[1])

            ColIndex = 0
            for Col in Row:
                if ColIndex >= 4:
                    if 'feels' in FirstRow[ColIndex]:
                        #print('   ', FirstRow[ColIndex], ' = ', Row[ColIndex])
                        temp.append(Row[ColIndex])
                ColIndex += 1
            TemperaturesOfCities.append(temp)
        RowIndex += 1

    if RowIndex == 0:
        print('Sorry, but it appears that there was an error connecting to the weather server.')
        print('Please check your network connection and try again..')

    # If there is only one CSV  row then we likely got an error from the server
    if RowIndex == 1:
        print('Sorry, but it appears that there was an error retrieving the weather data.')
        print('Error: ', FirstRow)

    print()


def dashboard():
    app.layout = html.Div(children=[
        html.H1(children="Analytics Dashboard of Cities Temperature (Dash Plotly)", style={"textAlign": "center"}),
        html.Hr(),
        html.P("Choose city of interest:"),
        # html.Div(#html.Div([
        dcc.Dropdown(id='dropdown', clearable=False,

                     options=[{'label': 'Bogotá', 'value': 'Bogotá, D.C., Colombia'},
                              {'label': 'Medellín', 'value': 'Medellín, Colombia'},
                              {'label': 'Barranquilla', 'value': 'Barranquilla, Colombia'},
                              {'label': 'Cartagena', 'value': 'Cartagena, Colombia'},
                              {'label': 'Bucaramanga', 'value': 'Bucaramanga, Colombia'}
                              ], value="Bogotá"),


        dcc.Graph(id='output-div')

    ])

    @app.callback(Output(component_id='output-div', component_property='figure'),
                  Input(component_id='dropdown', component_property='value'))
    def update_graph(city_chosen):
        dff = df[df["Ciudad"] == city_chosen]

        print(dff)
        fig = px.line(dff, x="Fecha", y="Temperatura_maxima", color='Ciudad')
        fig.add_scatter(x=dff["Fecha"], y=dff["Temperatura_minima"], name="Temp_min")
        fig.add_scatter(x=dff["Fecha"], y=dff["Temperatura_promedio"], name="Temp_prom")
        fig.update_layout(yaxis={"title": "Temperatura(C°)"},
                          xaxis={"title": "Día"})
        
        return fig


if not os.path.isfile('TemperaturasCiudadesColombia.csv'):
    # This is the core of our weather query URL
    BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

    ApiKey='8RYFYFN8XDHFVWQQD855F2CD4'#'PR5EXHJK5579L98NV9LLHD5D2'
    #UnitGroup sets the units of the output - us or metric
    UnitGroup='metric'

    #Locations for the weather data

    Cities=['Bogota,DC', 'Medellin','Barranquilla', 'Cartagena', 'Bucaramanga']
    TemperaturesOfCities=[]
    for i in Cities:
        ApiQuery=concatenate(i)
        print_()

    # Create and export csv
    headers=["Ciudad", "Fecha", "Tempertura_maxima", "Temperatura_minima", "Temperatura_promedio"]

    with open("TemperaturasCiudadesColombia.csv","w") as temp:
        Temp = csv.writer(temp)
        Temp.writerow(headers)
        Temp.writerows(TemperaturesOfCities)
    df = pd.read_csv("TemperaturasCiudadesColombia.csv")
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    dashboard()
else:
    df = pd.read_csv("TemperaturasCiudadesColombia.csv")
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    dashboard()

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8000)