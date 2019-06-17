import dash
import dash_core_components as dcc
import dash_html_components as html
from viz_util import *
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#load the dataset
data = read_data()

#clean dataset
data = clean_data(data)

#dataset to plot countries with all the three pages
all_pages = get_country_all_pages(data)

global conversions
#proportion of traffic moving from homepage to checkout is considered as conversion for homepage
conversions = get_conversions(data)
conversions_ = conversions.sort_values(by="PayPal Home",ascending=False)

#get sample size for deafult values of Alpha,beta and effect size
get_sample_size(conversions,10,0.05,0.2,10)

#initialize dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.Div([
    html.H1(children='Experimentation'),

    #bar chart plotting top 15 countries with highest traffic for Homepage
    dcc.Graph(
        id='graph1',
        figure={
            'data': [
                {'x': conversions_["country_code"][0:15], 'y': conversions_["PayPal Home"][0:15] , 'type': 'bar', 'name': 'PayPal Home'},
                {'x': conversions_["country_code"][0:15], 'y': conversions_["Checkout"][0:15] , 'type': 'bar', 'name': 'Checkout'},
            ],
            'layout': {
                'title': 'HomePage - Checkout'
            }
        }
    ),
    #plotting traffic for countries with all three pages
    dcc.Graph(
            id='graphx',
            figure={
                'data': [
                    {'x': all_pages["country_code"], 'y': all_pages["PayPal Home"] ,
                     'type': 'bar', 'name': 'PayPal Home'},
                    {'x': all_pages["country_code"], 'y': all_pages["Customer Merchant Home"] ,
                     'type': 'bar', 'name': 'Customer Merchant Home'},
                    {'x': all_pages["country_code"], 'y': all_pages["Checkout"] ,
                                         'type': 'bar', 'name': 'Checkout'},
                ],
                'layout': {
                    'title': 'HomePage -- Customer Merchant Home -- Checkout'
                }
            }
        ),


    ],style={'font-family': 'verdana;','text-align':'center'}),

    #Calculating the proportion of weeks required to run experiment with selected parameters
    html.Div([
        html.H4(children='Weeks required for Experimentation'),
    ],style={'font-family': 'verdana;','text-align':'center'}),

    html.Div([html.H5(children='Significance level α:'),
              dcc.Slider(
        id='alpha-slider',
        min=0.0,
        max=1.0,
        value=0.05,
        marks= {str(round(alpha,2)) : str(round(alpha,2)) for alpha in np.linspace(0,1,21)},
        step=None
    )],
    style={'width': '50%','height':'100px', 'display': 'inline-block'}),

    html.Div([html.H5(children='Beta β'),
              dcc.Slider(
            id='beta-slider',
            min=0.0,
            max=1.0,
            value=0.2,
            marks= {str(round(beta,2)) : str(round(beta,2)) for beta in np.linspace(0,1,21)},
            step=None
        )],
    style={'width': '50%','height':'100px'}),

    html.Div([html.H5(children='Effect Size'),
              dcc.Slider(
        id='Effect_size-slider',
        min=0,
        max=100,
        value=5,
        marks={str(eff_size): str(eff_size) for eff_size in range(0,100,5)},
        step=None
    )],
    style={'width': '50%','height':'100px'}),

    html.Div([html.H5(children='Percentage of traffic used'),
              dcc.Slider(
        id='per_traffic-slider',
        min=5,
        max=100,
        value=5,
        marks={str(per_tarffic): str(per_tarffic) for per_tarffic in range(0,100,5)},
        step=None
    )],
    style={'width': '50%','height':'100px'}),

    dcc.Graph(
            id='graph2',
            figure={
                'data': [
                    {'x': conversions["country_code"][0:15],
                     'y': conversions["weeks_for_sample_size"][0:15] ,
                     'type': 'bar', 'name': 'Weeks needed'},
                ],
                'layout': {
                    'title': 'Weeks needed for Experimentation'
                }
            }
        ),

    # PLot showing the change in sample size with change in Confidence intervals for selected country and effect size
    html.Div([html.H4("Sample size by country")],
             style={'font-family': 'verdana;','text-align':'center'}),

    html.Div([html.H5(children='Select Country:'),
              dcc.Dropdown(
                  id='country_code',
                  options=[{'label': i, 'value': i} for i in conversions["country_code"]],
                  value='US'
              )],
             style={'width': '10%', 'height': '100px', 'display': 'inline-block'}),


    html.Div([html.H5(children='Effect Size :'),
              dcc.Input(id='country_effect_size', value=2, type='number')],
             style={'width': '10%', 'height': '100px'}),


        dcc.Graph(
            id='graph3',
            figure={
                'data': [
                    {'x': [(1 - i)*100 for i in np.linspace(0,1,100)][1:99],
                     'y': get_sample_size_custom(conversions,"US",2,0.01) ,
                     'type': 'line', 'name': '99% Confidence Interval'},

                    {'x': [(1 - i) * 100 for i in np.linspace(0, 1, 100)][1:99],
                     'y': get_sample_size_custom(conversions, "US", 2, 0.05),
                     'type': 'line', 'name': '95% Confidence Interval'},

                    {'x': [(1 - i) * 100 for i in np.linspace(0, 1, 100)][1:99],
                     'y': get_sample_size_custom(conversions, "US", 2, 0.1),
                     'type': 'line', 'name': '90% Confidence Interval'},

                ],
                'layout': {
                    'title': 'Country Analysis',

                }
            }
        ),

])


#callback function to update plots
@app.callback(
    Output('graph3', 'figure'),
    [Input('country_code', 'value'),
     Input('country_effect_size', 'value')
     ])
def update_figure(selected_country_code,
                  selected_effect_size,
                  ):
    return {
        'data': [
                    {'x': [(1 - i)*100 for i in np.linspace(0,1,100)][1:99],
                     'y': get_sample_size_custom(conversions,selected_country_code,selected_effect_size,0.05) ,
                     'type': 'line', 'name': '95% Confidence Interval'},

                    {'x': [(1 - i) * 100 for i in np.linspace(0, 1, 100)][1:99],
                     'y': get_sample_size_custom(conversions, selected_country_code,selected_effect_size, 0.01),
                     'type': 'line', 'name': '99% Confidence Interval'},

                    {'x': [(1 - i) * 100 for i in np.linspace(0, 1, 100)][1:99],
                     'y': get_sample_size_custom(conversions, selected_country_code,selected_effect_size, 0.1),
                     'type': 'line', 'name': '90% Confidence Interval'},

                ],
        'layout': go.Layout(
            xaxis={'title': 'Power of test'},
            yaxis={'title': 'Sample size'},
            hovermode='closest'
        )

    }

#callback function to update plot
@app.callback(
    Output('graph2', 'figure'),
    [Input('alpha-slider', 'value'),
     Input('beta-slider', 'value'),
     Input('Effect_size-slider', 'value'),
     Input('per_traffic-slider', 'value')])
def update_figure(selected_alpha,
                  selected_beta,
                  selected_eff_size,
                  selected_per_tarffic):
    get_sample_size(conversions,selected_eff_size,selected_alpha,selected_beta,selected_per_tarffic)
     #conversions_
    return {
        'data': [
                    {'x': conversions["country_code"][0:15],
                     'y': conversions["weeks_for_sample_size"][0:15] ,
                     'type': 'bar', 'name': 'Weeks needed'},
                ],
        'layout': go.Layout(

            xaxis={'title': 'Country'},
            yaxis={'title': 'Weeks'},
            hovermode='closest'
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)