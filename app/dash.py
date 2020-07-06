from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import os
import psycopg2 as pg
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd
# Connect to PostgreSQL database
host = "ec2-18-144-86-70.us-west-1.compute.amazonaws.com"
# host = "127.0.0.1"
port = "5432"
database = "testdb"
user = "testuser"
password = "Test@123"
conn = pg.connect(dbname=database, user=user, password=password, host=host, port=port)
cursor = conn.cursor()
# create app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# setmapbox style
# current script path
scripty_path = os.path.dirname(os.path.realpath(__file__))
mapbox_access_token = 'pk.eyJ1IjoibXo4NiIsImEiOiJja2J0azVhN3MwOXJhMnpud2VsYjI5ZjJrIn0.8cBcxThR38B2bTaxQ8qsUw'
px.set_mapbox_access_token(mapbox_access_token)

# sql connection

app.layout = html.Div([
    html.Div([
        html.H4('Smart Flash'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*100000, # in milliseconds
            n_intervals=0)])
])

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    postgreSQL_select_Query='SELECT sensorid,time,lat,lon,signal from test WHERE ( unix_timestamp( ) - unix_timestamp( time ) ) < 10 GROUP BY CONCAT(sensorid, time) HAVING COUNT(*) = 1'
    cursor.execute(postgreSQL_select_Query)
    df = pd.read_sql_query(postgreSQL_select_Query, conn)
    #df = pd.DataFrame(cars, columns = ['time', 'lat','lon','signal'])
    #print(df)
    #print('ploting')
    # Create the graph with subplots
    figure = px.scatter_mapbox(df,
                               lat='lat',
                               lon='lat',
                               color='lat',
                               color_discrete_map = {"Red": "red", "Green": "green", "Orange":"orange"},
                               size_max=16,
                               zoom=9)

    figure.update_layout(uirevision = True,
                         mapbox = {'center': {'lon':-73.862614, 'lat': 40.799312}})
    print(df)
    print('to plot')
    return figure


if __name__ == '__main__':
    app.run_server(debug=True,host='ec2-18-144-9-66.us-west-1.compute.amazonaws.com')
                                                                                    
