import requests
import pandas
import json

import chart_studio.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot


def plot1d():

    url = "https://corona.lmao.ninja/v2/states"
    
    response = requests.request("GET", url)

    data_json = json.loads(response.text)

    statesdf=pandas.DataFrame(data_json)

    state_codes = {
    'District of Columbia' : 'DC','Mississippi': 'MS', 'Oklahoma': 'OK', 
    'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR', 
    'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 
    'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ', 
    'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 
    'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT', 
    'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV', 
    'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
    'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 
    'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY', 
    'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 
    'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD', 
    'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 
    'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX', 
    'Nevada': 'NV', 'Maine': 'ME', 'Guam': 'GU', 'Northern Mariana Islands': 'MP',
    'Puerto Rico': 'PR'}

    statesdf['state_code'] = statesdf['state'].map(state_codes) 

    data = dict(type = 'choropleth',
           locations = statesdf['state_code'],
           locationmode = 'USA-states',
           colorscale = [[0.0, "rgb(241, 199, 174)"],
                [0.1111111111111111, "rgb(212, 155, 135)"],
                [0.2222222222222222, "rgb(184, 111, 97)"],
                [0.3333333333333333, "rgb(155, 66, 58)"],
                [0.4444444444444444, "rgb(126, 22, 19)"],
                [0.5555555555555556, "rgb(107, 0, 0)"],
                [0.6666666666666666, "rgb(97, 0, 0)"],
                [0.7777777777777778, "rgb(87, 0, 0)"],
                [0.8888888888888888, "rgb(76, 0, 0)"],
                [1.0, "rgb(66, 0, 0)"]],
           text = statesdf['state'],
           z = statesdf['cases'],
           marker = dict(line = dict(color = '#202940', width=0.5)),
           colorbar = {'title':'Total Cases'})

    layout = dict(title = 'Total COVID-19 Cases by State', font = {"size": 15, "color":"White"},
             geo = dict(scope='usa', showlakes = True, bgcolor= '#202940', lakecolor='rgb(85,173,240)', visible = True), paper_bgcolor='#202940', plot_bgcolor='#202940')

    choromap = go.Figure(data = [data],layout=layout)

    plot_div = plot(choromap, output_type='div', include_plotlyjs=False)

    return plot_div

def plotworld():

       url = "https://corona.lmao.ninja/v2/countries"
        
       response = requests.request("GET", url)

       world_data_json = json.loads(response.text)

       df=pandas.DataFrame(world_data_json)

       country_code = [d.get('iso3') for d in df['countryInfo']]

       # df = pandas.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

       fig = go.Figure(data=go.Choropleth(
       locations = country_code,
       z = df['cases'],
       text = df['country'],
       colorscale = [[0.0, "rgb(151, 67, 59)"],
                [0.1111111111111111, "rgb(122, 22, 20)"],
                [0.2222222222222222, "rgb(102, 0, 0)"],
                [0.3333333333333333, "rgb(93, 0, 0)"],
                [0.4444444444444444, "rgb(88, 0, 0)"],
                [0.5555555555555556, "rgb(84, 0, 0)"],
                [0.6666666666666666, "rgb(79, 0, 0)"],
                [0.7777777777777778, "rgb(74, 0, 0)"],
                [0.8888888888888888, "rgb(69, 0, 0)"],
                [1.0, "rgb(65, 0, 0)"]],
       autocolorscale=False,
       reversescale=False,
       marker_line_color='darkgray',
       marker_line_width=0.5,
       colorbar_title = 'Total<br>Cases',
       ))

       fig.update_layout(
       title_text='Worldwide COVID-19 cases',
       paper_bgcolor='#202940', 
       plot_bgcolor='#202940',
       width=1700,
       height=1000,
       font = {"size": 15, "color":"White"},
       # line = dict(color = '#202940', width=0.5)
       geo=dict(  
              showframe=False,
              showcoastlines=False,
              projection_type='equirectangular',
              bgcolor= '#202940',
       ),
       annotations = [dict(
              x=0.55,
              y=0.1,
              xref='paper',
              yref='paper',
              text='',
              showarrow = False,
       )]
       )

       plot_div = plot(fig, output_type='div', include_plotlyjs=False)

       return plot_div
