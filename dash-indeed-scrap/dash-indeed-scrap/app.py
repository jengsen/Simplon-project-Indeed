from pymongo import MongoClient
import functools
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash_table
import os

#Connexion à mongoDB 'Tentative'

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.job_offers #Select the database
todos = db.Simplon_Indeed #Select the collection name

#Dataframe utilisées

df2 = pd.read_csv("data/skills_bbd.csv", encoding='utf8', engine='python')

df= pd.read_csv("data/scrapindeed.csv", encoding='utf8', engine='python')

df_pred = pd.read_csv("data/mean_pred_salaries.csv", encoding='utf8', engine='python')

#Lien Github
GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/jengsen/Simplon-project-Indeed",
)

#Variable utiliser pour les graph (Heatmap et histogram)
job = ['développeur', 'business intelligence', 'data analyst', 'data scientist']
city = ['Bordeaux','Lyon','Nantes','Paris','Toulouse']


k = df.groupby('Scrapped_location')['Scrapped_job'].value_counts()
bord = k['Bordeaux'].values
Lyo = k['Lyon'].values
Nant = k['Nantes'].values
Par = k['Paris'].values
Toul = k['Toulouse'].values

#Colonne du Dataframe selectionnées
colum = ['Titre', 'Entreprise', 'Ville', 'Salaire',
            'Descriptif_du_poste', 'Scrapped_job', 'Scrapped_location']

#Variable graph 3D
selected_x = df2.iloc[:, -1].tolist()
selected_y = df2.iloc[:, 3].tolist()
selected_z = df2.iloc[:, 5].tolist()

#Style des tableaux
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
    'color': 'black',
    'padding': '6px'
}

#Début du 'Frontend' de Dash (L'organisation de la page

app = dash.Dash()

colors = {
    'text': 'black'
}

app.layout = html.Div([
    #Header
    html.Div([
        html.A(html.Img(className="logo", src=app.get_asset_url("dash-logo.png")),href="https://dash.plot.ly/",target="_blank",),
        html.Div(
            className="header",
            children=[
                html.Div(
                    className="div-info",
                    children=[
                        html.H2(className="title", children="Projet Indeed"),
                        #J'ai mis du Lorem Ipsum en attendant du texte pour le début
                        html.P(
                            """
                            Contexte :  
                            
                            Je suis CEO d’une boite qui s’occupe de faire des statistiques sur l’emploi dans le secteur du développement informatique et de la data à Paris, Lyon, Toulouse, Nantes et Bordeaux. 
                            Je m’intéresse tout particulièrement aux différences de salaires entre ces métiers + villes.
                            Je vous mandate afin de me fournir une étude sur ce marché à présenter sous forme de Dashboard.

                            """
                        ),
                        html.A(
                            children=html.Button("View On Github", className="button"),
                            href=GITHUB_LINK,
                            target="_blank",
                        ),
                    ],
                ),
            ],
        ),
    ]),

    html.Hr(),
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
                                        {"name": i, "id": i, "deletable": True} for i in df[colum]
                                    ],
                                    data=df.to_dict('records'),
                                    filter_action="native",
                                    #Style du header du tableau
                                    style_header={
                                        "textTransform": "Uppercase",
                                        "fontWeight": "bold",
                                        "backgroundColor": "#ffffff",
                                        "padding": "5px 0px",
                                    },
                                    style_table={'overflowX': 'scroll'},
                                    style_cell={
                                            'height': '25px',
                                            'minWidth': '0px', 'maxWidth': '200px',
                                            'whiteSpace': 'normal'
                                    }
                                ),
                                #Div d'apparition du tableau
                                html.Div(id='datatable-filter-container')
                            ])
                            ])
                        ]),
                        #Côté ML
                        dcc.Tab(label='Machine Learning', children=[
                            html.Div([
                                html.Div([html.H1("'salaire pertinant' (salaire prédit) en fonction des skills trouvés")],
                                         style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
                                html.Div(
                                    #Selection de X,Y et Z pour le Graph 3D
                                    [html.Div(dcc.Dropdown(id="select-xaxis",
                                                           options=[{'label': i.title(), 'value': i} for i in
                                                                    df2.columns[9:]],
                                                           value='mean', ), className="four columns",
                                              style={"display": "block", "margin-left": "auto",
                                                     "margin-right": "auto", "width": "33%"}),
                                     html.Div(dcc.Dropdown(id="select-yaxis",
                                                           options=[{'label': i.title(), 'value': i} for i in
                                                                    df2.columns[9:]],
                                                           value='nb annonces', ), className="four columns",
                                              style={"display": "block", "margin-left": "auto",
                                                     "margin-right": "auto", "width": "33%"}),
                                     html.Div(dcc.Dropdown(id="select-zaxis",
                                                           options=[{'label': i.title(), 'value': i} for i in
                                                                    df2.columns[9:]],
                                                           value='coef', ), className="four columns",
                                              style={"display": "block", "margin-left": "auto",
                                                     "margin-right": "auto", "width": "33%"})
                                     ], className="row",
                                    style={"padding": 14, "display": "block", "margin-left": "auto",
                                           "margin-right": "auto", "width": "80%",'display': 'none'}),
                                html.Div([dcc.Graph(id="my-graph2")])
                            ], className="container"),
                            html.Div([
                                #Graph pour le 'df_final avec la moyenne et la prédiction (Ne possède pas de callback
                                dcc.Graph(id='selected',
                                figure={
                                        'data': [go.Scatter(
                                        x=df_pred['prediction'],
                                        y=df_pred['avg_salaire'],
                                        name='Différence entre la moyenne et la prédiction du salaire',
                                        text=df_pred['skills'],
                                        mode='markers',
                                        marker_color=df_pred['avg_salaire']
                                        ),
                                        go.Scatter(
                                            x=[0,140000], y=[0,140000],
                                            line_color='Blue',
                                            name='Average'
                                        )],
                                        "layout": go.Layout(
                                            title='Prédiction Vs Moyenne',
                                            xaxis={"title": "Prédiction"},
                                            yaxis={"title": "Salaire Moyen"},
                                        ),
                                },
                                ),
                            ]),
                        ]),
                ]),
        ])
],className="body")

#Fin  du Front-end du Dash

#Exception pour éviter trouver plus facilement les variable disponible que dans le callback
app.config.suppress_callback_exceptions = True

#Callback pour le premier nuage de mots et le texte ou image des étapes suivis
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
            html.Div(children='Métier (développeur, data scientist…)'
                                'Type de contrat recherché (CDI, CDD, freelance…)'
                                'Lieu de recherche (Paris, Toulouse, …)'
                     'Les infos à scraper :'
                                'Titre'
                                'Nom de la boite'
                                'Adresse'
                               ' Salaire'
                                'Descriptif du poste'
                                'Date de publication de l’annonce')
        ])
#Callback Pour le heatmap et l'histogram
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
                        colorscale ='Rainbow'
                    )],
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
                                #Ref variables du début
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

#Callback pour les word cloud par villes

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

#Callback du tableau

@app.callback(
    Output('datatable-filter-container', "children"),
    [Input('datatable-filtering-fe', "data")])
def update_graph(rows):
    if rows is None:
        dfr = df
    else:
        dfr = pd.DataFrame(rows)

    return html.Div()


#Callback Graph 3D 'Resultat NLP'

@app.callback(
    dash.dependencies.Output("my-graph2", "figure"),
    [dash.dependencies.Input("select-xaxis", "value"),
     dash.dependencies.Input("select-yaxis", "value"),
     dash.dependencies.Input("select-zaxis", "value")]

)

def ugdate_figure(selected_x, selected_y, selected_z):
    z = df2[selected_z]
    trace = [go.Scatter3d(
        x=df2[selected_x], y=df2[selected_y], z=df2[selected_z],
        name=str(df2["skill"]),text=df2["skill"],
        mode='markers', marker={'size': 8, 'color': z, 'colorscale': 'Blackbody', 'opacity': 0.8, "showscale": True,
                                "colorbar": {"thickness": 15, "len": 0.5, "x": 0.8, "y": 0.6, }, })]
    return {"data": trace,
            "layout": go.Layout(
                height=700, title=f"<br>{selected_x.title(), selected_y.title(), selected_z.title()}",
                paper_bgcolor="#f3f3f3",
                scene={"aspectmode": "cube", "xaxis": {"title": f"Salaire Moyen", },
                       "yaxis": {"title": f"Nombre d'Annonces' ", },
                       "zaxis": {"title": f"Coefficient ", }})
            }

#Callback Heatmap

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
#Appel du CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        "/assets/style.css",]

if __name__ == '__main__':
    #log_reg_model = pickle.load(open(filename, 'rb'))
    #result = log_reg_model.score(X_test, y_test)
    app.run_server(port=3400, debug=True)