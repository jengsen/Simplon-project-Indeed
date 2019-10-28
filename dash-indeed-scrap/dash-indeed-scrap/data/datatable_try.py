import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import json
import ast
from dash.exceptions import PreventUpdate

df_svm = pd.read_json('Predictions/main_features_SVM.json')
df_log = pd.read_json('Predictions/main_features_Log Reg.json')
df_rf = pd.read_json('Predictions/main_features_Random Forest.json')
df_ada = pd.read_json('Predictions/main_features_Ada Boost.json')
df_gbo = pd.read_json('Predictions/main_features_Gradient Boost.json')
df_xgbo = pd.read_json('Predictions/main_features_X Gradient Boost.json')


app = dash.Dash()

suppress_callback_exceptions=True

app.layout =html.Div([
    dcc.Store(id='memory-output'),
    dcc.Dropdown(id='memory-field', options=[
        {'label': 'Log reg', 'value': 'REGLOG'},
        {'label': 'SVM', 'value': 'SVM'},
        {'label': 'Random Forest', 'value': 'RF'},
        {'label': 'Ada Boost', 'value': 'ADA'},
        {'label': 'Gradient Boost', 'value': 'GBO'},
        {'label': 'X Gradient Boost', 'value': 'XGBO'}
    ], value='REGLOG'),
    html.Div([
        dash_table.DataTable(id='datatable-upload-container'),
    ])
])


@app.callback(Output('memory-output', 'data'),
              [Input('memory-field', 'value')])
def filter_countries(countries_selected):
    if not countries_selected:
        # Return all the rows on initial load/no country selected.
        return df_log.to_dict('records')

    if countries_selected == 'REGLOG':
        df_mod = df_log
    elif countries_selected == 'SVM':
        df_mod = df_svm
    elif countries_selected == 'RF':
        df_mod = df_rf
    elif countries_selected == 'ADA':
        df_mod = df_ada
    elif countries_selected == 'GBO':
        df_mod = df_gbo
    elif countries_selected == 'XGBO':
        df_mod = df_xgbo
    else:
        df_mod = df_log

    return df_mod.to_json(orient='records')

@app.callback([Output('datatable-upload-container', 'data'),
               Output('datatable-upload-container', 'columns')],
              [Input('memory-field', 'value')])
def update_output(countries_selected):
    if countries_selected is None:
        return [{}], []
    df = filter_countries(countries_selected)
    df = json.dumps(df)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


"""@app.callback(Output('datatable-upload-graph', 'figure'),
              [Input('datatable-upload-container', 'data')])
def display_graph(rows):
    df = pd.DataFrame(rows)

    if (df.empty or len(df.columns) < 1):
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return {
        'data': [{
            'x': df[df.columns[2]],
            'y': df[df.columns[3]],
            'type': 'bar'
        }]
    }"""

if __name__ == '__main__':
    app.run_server(debug=True)