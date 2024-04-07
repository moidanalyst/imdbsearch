#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dash import Dash, html, dcc, Input, Output
from flask import Flask
import pandas as pd
from dash_table import DataTable
from selenium import webdriver
import webview

df = pd.read_csv(r"C:\Users\JMC\Desktop\Projects\IMDB Movie Ratings\imdb_movie_data_2023.csv")

# Set the maximum number of rows and columns to display
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df.drop(df.columns[0], axis=1, inplace=True)

df.rename(columns={'Moive Name': 'Movie Name'}, inplace=True)

df["Movie Name"] = df["Movie Name"].astype("string", errors='ignore')
df["Genre"] = df["Genre"].astype("string", errors='ignore')
df["PG Rating"] = df["PG Rating"].astype("string", errors='ignore')
df["Cast"] = df["Cast"].astype("string", errors='ignore')
df["Duration"] = df["Duration"].astype("string", errors='ignore')
df["Director"] = df["Director"].astype("string", errors='ignore')

server = Flask(__name__)
app = Dash(__name__, server = server)

app.layout = html.Div([
    html.Br(),
    html.H1("IMDB Movie Database Exploration", style={'margin': '20px'}),
    html.Br(),

    html.Strong("Movie Name", style={'margin': '20px'}),
    dcc.Input(id="Movie", value="", type="text", style={'background-color': 'light grey', 'width': '300px', 'color': 'black'}),
    html.Br(), html.Br(),

    html.Strong("Actor(s)", style={'margin': '20px'}),
    dcc.Input(id="Actors", value="", type="text", style={'background-color': 'light grey', 'width': '300px', 'color': 'black'}),
    html.Br(), html.Br(),

    DataTable(id='Output', columns=[{"name": i, "id": i} for i in df.columns], style_table={'overflowX': 'scroll'})

], style={
    'background-color': 'white',
    'background-blend-mode': 'overlay',
    'background-size': 'cover',
    'background-position': 'center',
    'background-repeat': 'no-repeat',
    'height': '100vh',
    'font-family': ['segoe ui', 'garamond'],
    'color': 'Black',
    'font-size': '14px'
})


@app.callback(
    Output(component_id='Output', component_property='data'),
    Input(component_id='Movie', component_property='value'),
    Input(component_id='Actors', component_property='value'),
)

def update_output_div(mov, act):
    if mov is None and act is None:
        # Return empty data if both inputs are empty
        return []
    
    # Initialize search condition
    search = pd.Series(True, index=df.index)
    if mov:
        # Extend search condition to include movie name if provided
        search &= df["Movie Name"].str.contains(mov, case=False)
    if act:
        # Extend search condition to include actors if provided
        search &= df["Cast"].str.contains(act, case=False)

    # Filter data and convert to dictionary records
    filtered_data = df[search].to_dict('records')
    return filtered_data

# Now we run the Dash App on the Flask Server and show the output in WebView Window
if __name__ == "__main__":
    # Start the Dash server
    app.run_server(debug=False)

    # open the browser
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://localhost:8050")