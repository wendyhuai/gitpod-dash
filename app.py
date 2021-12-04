import dash
from dash import dcc # dash core components
from dash import html
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output, State




df = pd.read_csv('https://bit.ly/elements-periodic-table')

def identity(x): return x


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Pivot Table"),
    html.H2("Index"),
    dcc.Dropdown(
        id="index",
        options=[{'label': i, 'value': i} for i in df.columns],
        multi=False,
        value="Period"
    ),
    html.H2("Columns"),
    dcc.Dropdown(
        id="columns",
        options=[{'label': i, 'value': i} for i in df.columns],
        multi=False,
        value="Group"
    ),
    html.H2("Values"),
    dcc.Dropdown(
        id="values",
        options=[{'label': i, 'value': i} for i in df.columns],
        multi=False,
        value="Element"
    ),
    html.Br(),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Br(),
    html.Br(),

    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns]
    )
])

@app.callback([
    Output('table', 'data'),
    Output('table', 'columns')
    ], 
    [
        Input('submit-button-state', 'n_clicks'),
        State('index', 'value'),
        State('columns', 'value'),
        State('values', 'value'),
    ])

def update_cols(n_clicks, index, columns, values):
    if index == columns or index == values or values == columns:
        print("Please select different columns")
        return None, None

    pvt_tb = df.pivot_table(
        index=index,
        columns=columns, 
        values=values,
        aggfunc=identity,
    )
    pvt_tb = pd.DataFrame(pvt_tb.to_records())
    pvt_cols = [{"name": i, "id": i} for i in pvt_tb]

    return pvt_tb.to_dict('records'), pvt_cols 

if __name__ == '__main__':
    app.run_server(debug=True)