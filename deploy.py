import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import urllib.request
import joblib

import extract_real_data as xrd
from BigQuery import upload_to_bigquery

# -------------------- MODEL -----------------------
model =  joblib.load("./tuned_model.joblib")
# -------------------- SETTINGS --------------------
def make_prediction(df_row):
    #input: tail of df
    stats_for_predict = df_row.drop(["time","win_probability"],axis=1)
    df_row["win_probability"] = model.predict_proba(stats_for_predict)[0][1]
    return df_row

def game_phase(df_now):
    #check game phases
    return

df_current = pd.DataFrame([{}])

try:
    df_new_stats = pd.DataFrame([xrd.current_stats(xrd.get_live_data())])
    df_current = make_prediction(df_new_stats)
except urllib.request.URLError:
    pass
print(df_current)

pd.options.plotting.backend = "plotly"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],update_title = None )
app.title = "Real time LOL Prediction"
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Real-time LoL Winning Prediction", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
            dcc.Graph(id='graph', config={
                'staticPlot': False,
                'scrollZoom': True,
                'doubleClick': 'reset',
                'showTips': False,
                'displayModeBar': True,
                'watermark': False,
            })
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("Algorithm is evaluating live match data such as Kills, Dragons, Tower acquisition of both teams, etc.", className="text-center"), width=12)
    ]),
    #  dbc.Row([
    #     dbc.Col(html.Div(id='first-blood-indicator'), width=4),
    #     # dbc.Col(html.Div(id='first-dragon-indicator'), width=4),
    #     # dbc.Col(html.Div(id='first-tower-indicator'), width=4)
    # ]),
], fluid=True)



@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):
    
    global df_current
    
    try:
        df_new_stats = pd.DataFrame([xrd.current_stats(xrd.get_live_data())])
        df_new_stats = make_prediction(df_new_stats)
        df_current = df_current.append(df_new_stats)
        upload_to_bigquery(df_new_stats)
        print(df_current)
    except urllib.request.URLError:
        pass
    fig = df_current.plot(x="time",y="win_probability", template = 'plotly_dark')
    return(fig)

# @app.callback(
#     Output('first-blood-indicator', 'children'),
#     [Input('interval-component', 'n_intervals')])
# def update_first_blood_indicator(n):
#     data = xrd.get_live_data()
#     first_blood_team = xrd.first_blood(data)
#     if first_blood_team == "t1":
#         return dbc.Badge("First Blood: Team 1", color="success", className="mr-1")
#     elif first_blood_team == "t2":
#         return dbc.Badge("First Blood: Team 2", color="danger", className="mr-1")
#     else:
#         return ""



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
# --------------------------------------------------

