import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import urllib.request
import joblib
import urllib.request

import extract_real_data as xrd

# -------------------- MODEL -----------------------
model =  joblib.load("./tuned_model.jolib")
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
app.layout = html.Div([
    html.H1("Real time LOL winning prediction:"),
    dcc.Interval(
        id='interval-component',
        interval=5000, # in milliseconds
        n_intervals=0
                ),
    dcc.Graph(id='graph',
              config={
                      'staticPlot': False,     
                      'scrollZoom': True,      
                      'doubleClick': 'reset',  
                      'showTips': False,       
                      'displayModeBar': True,  
                      'watermark': False,
                        },
              ),
    html.P(" "),
    html.P("Algorithm is evaluating live match data: such as Kills, Dragons, Tower achquisiton of both teams etc."),
    html.P("Live data is inpreted as match state at 15 minute mark."),
    html.P("Hence most accurate result will be around that time.")
])


@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):
    
    global df_current
    
    try:
        df_new_stats = pd.DataFrame([myf.current_stats(myf.get_live_data())])
        df_new_stats = make_prediction(df_new_stats)
        df_current = df_current.append(df_new_stats)
        print(df_current)
    except urllib.request.URLError:
        pass
    fig = df_current.plot(x="time",y="win_probability", template = 'plotly_dark')
    return(fig)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


# --------------------------------------------------

