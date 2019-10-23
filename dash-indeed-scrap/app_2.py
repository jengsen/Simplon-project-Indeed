from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash_table
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.job_offers #Select the database
todos = db.Simplon_Indeed #Select the collection name


df= pd.read_csv("data/scrapingindeed.csv")


job = ['développeur', 'business intelligence', 'data analyst', 'data scientist']
city = ['Bordeaux','Lyon','Nantes','Paris','Toulouse']


k = df.groupby('Scrapped_location')['Scrapped_job'].value_counts()
bord = k['Bordeaux'].values
Lyo = k['Lyon'].values
Nant = k['Nantes'].values
Par = k['Paris'].values
Toul = k['Toulouse'].values


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#ccccff',
    'color': 'black',
    'padding': '6px'
}

app = dash.Dash()

colors = {
    'text': 'black'
}
app.layout = html.Div([

    html.Div(children=[
        html.H1(
            children='Scraping Indeed',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Pour un total de X offres nous avons.....', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        ]),


    html.Div([
                #Tableau principal (Il prend en compte les deux parties (Analysis & ML))
                dcc.Tabs(id="tabs", children=[
                    #Partie 1 du tableau principal (Partie Data Analysis) Graph & text analytique (sans les salaires)
                    dcc.Tab(label='Analysis', children=[
                        html.Div([
                            #Tableau N°1 : (Ref. Callback pour éléments) Image(Word cloud) et Text introductif à REMPLIR  !!!!!
                            html.Div([
                                dcc.Tabs(id="tabs-styled-with-props", value='tab-1', children=[
                                    dcc.Tab(label='Word Cloud', value='tab-1'),
                                    dcc.Tab(label='Explications', value='tab-2'),
                                ], colors={
                                    #Couleurs pour le tableau
                                    "border": "white",
                                    "primary": "mediumblue",
                                    "background": "#ccccff"
                                }),
                                html.Div(id='tabs-content-props')
                            ]),
                                #Saut pour créer un espace entre les éléments
                                html.Br(),
                                #Tableau N°2: Heatmap & graphique en bar.

                           html.Div([
                                dcc.Tabs(id="tabs-styled-with-props2", value='tab-3', children=[
                                    dcc.Tab(label='Offres par villes et jobs', value='tab-3'),
                                    dcc.Tab(label='Offres total par villes', value='tab-4'),
                                ], colors={
                                    "border": "white",
                                    "primary": "mediumblue",
                                    "background": "#ccccff"
                                }),
                                html.Div(id='tabs-content-props2')
                            ]),
                        #Saut pour créer un espace entre les éléments
                                html.Br(),
                                html.Br(),
                            html.Div([
                                dcc.Tabs(id="tabs-styled-with-inline-city", value='tab-a', children=[
                                    dcc.Tab(label='Paris', value='tab-a', style=tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Nantes', value='tab-b', style=tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Toulouse', value='tab-c', style=tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Lyon', value='tab-d', style=tab_style, selected_style=tab_selected_style),
                                    dcc.Tab(label='Bordeaux', value='tab-e', style=tab_style, selected_style=tab_selected_style),

                                ], style=tabs_styles),
                                html.Div(id='tabs-content-inline-city')
                            ]),
                            html.Br(),
                            html.Br(),
                            #Spaces
                            html.Div([
                                dash_table.DataTable(
                                    id='datatable-filtering-fe',
                                    fixed_rows={'headers': True, 'data': 0},
                                    columns=[
                                        {"name": i, "id": i, "deletable": True} for i in df.columns
                                    ],
                                    data=df.to_dict('records'),
                                    filter_action="native",
                                ),
                                html.Div(id='datatable-filter-container')
                            ])
                            ])
                        ]),
                        dcc.Tab(label='Machine Learning', children=[
                                dcc.Graph(
                                    id='ml-part',
                                    figure={
                                        'data': [
                                            {'x': [1, 2, 3], 'y': [1, 4, 1],
                                                'type': 'bar', 'name': 'SF'},
                                            {'x': [1, 2, 3], 'y': [1, 2, 3],
                                             'type': 'bar', 'name': u'Montréal'},
                                        ]
                                    }
                                )
                        ]),
                ]),
    ])
])

app.config.suppress_callback_exceptions = True


@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs-styled-with-props', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Br(),
            html.Img(src=app.get_asset_url('word_cloud.png'),
            style={
                'height': '50%',
                'width': '40%',
                'margin-left': '30%'
            })
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div(children='At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga.At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga.')
        ])

@app.callback(Output('tabs-content-props2', 'children'),
              [Input('tabs-styled-with-props2', 'value')])
def render_content(tab):
    if tab == 'tab-3':
        return html.Div([
            html.Div([
            dcc.Graph(id='heatmap',
                    figure = {
                    'data': [go.Heatmap(
                    z=[bord, Lyo,Nant, Par,Toul],
                    x= job,
                    y=city,
                    #colorscale => doesn't work.
                    colorscale ='Rainbow')],
                    'layout': go.Layout(
                    xaxis=dict(title= 'Villes'),
                    yaxis= dict(title= 'Jobs'),
                    )})
                    ]),
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x=city,
                                y=[2611,4504,4106,11708, 4346],
                                name='Par villes',
                                marker=go.bar.Marker(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                        ],
                        layout=go.Layout(
                            title='Offres total par villes',
                            showlegend=True,
                            legend=go.layout.Legend(
                                x=0,
                                y=1.0
                            ),
                            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                        )
                    ),
                    style={'height': 300},
                    id='my-graph'
                )
            ])
        ])


@app.callback(Output('tabs-content-inline-city', 'children'),
              [Input('tabs-styled-with-inline-city', 'value')])
def render_content(tab):
    if tab == 'tab-a':
        return html.Div([
            html.Br(),
            html.Img(src=app.get_asset_url('paris_jobs.jpg'),
            style={
                'height': '50%',
                'width': '40%',
                'margin-left': '30%'
            })
        ])
    elif tab == 'tab-b':
        return html.Div([
            html.Br(),
            html.Img(src=app.get_asset_url('nantes_jobs.jpg'),
            style={
                'height': '50%',
                'width': '40%',
                'margin-left': '30%'
            })
        ])
    elif tab == 'tab-c':
        return html.Div([
            html.Br(),
            html.Img(src=app.get_asset_url('toulouse_jobs.jpg'),
            style={
                'height': '50%',
                'width': '40%',
                'margin-left': '30%'
            })
        ])
    elif tab == 'tab-d':
        return html.Div([
            html.Br(),
            html.Img(src=app.get_asset_url('lyon_jobs.jpg'),
            style={
                'height': '50%',
                'width': '40%',
                'margin-left': '30%'
            })
        ])
    elif tab == 'tab-e':
        return html.Div([
            html.Br(),
            html.Img(src=app.get_asset_url('bordeaux_jobs.jpg'),
            style={
                'height': '50%',
                'width': '40%',
                'margin-left': '30%'
            })
        ])

@app.callback(
    Output('datatable-filter-container', "children"),
    [Input('datatable-filtering-fe', "data")])
def update_graph(rows):
    if rows is None:
        dff = df
    else:
        dff = pd.DataFrame(rows)

    return html.Div()

@app.callback(
    Output('heatmap', 'figure'),
    [Input('heatmap', 'hoverData'),
     Input('heatmap', 'clickData')])
def display_hoverdata(hoverData, clickData):
    return {
        'data': [go.Heatmap(
        z=[bord, Lyo, Nant, Par, Toul],
        x=job,
        y=city,
        xgap = 2,
        ygap = 2
    )]
    }


if __name__ == '__main__':
    app.run_server(debug=True)