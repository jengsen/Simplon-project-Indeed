import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import dash_table
import json
df= pd.read_csv("scrapindeed.csv")
job = ['développeur', 'business intelligence', 'data analyst', 'data scientist']
city = ['Bordeaux','Lyon','Nantes','Paris','Toulouse']
k = df.groupby('Scrapped_location')['Scrapped_job'].value_counts()
bord = k['Bordeaux'].values
Lyo = k['Lyon'].values
Nant = k['Nantes'].values
Par = k['Paris'].values
Toul = k['Toulouse'].values

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
html.Div(children=[
    html.H4(children='Offres par villes et jobs')
]),
        html.Br(),
        html.Br(),
    html.Div([
    dcc.Graph(id='heatmap',
            figure = {
            'data': [go.Heatmap(
            z=[bord, Lyo,Nant, Par,Toul],
            x= job,
            y=city,
            colorscale ='Rainbow')],
            'layout': go.Layout(
            xaxis=dict(title= 'Villes'),
            yaxis= dict(title= 'Jobs'),
            )})
            ]),
    #Saut
        html.Br(),
        html.Br(),
    #Saut
    html.Div([
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=city,
                        y=[1668,3297,2982,7945, 3040],
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
    ]),
    # Saut
    html.Br(),
    html.Br(),
    html.Br(),
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
    ]),
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