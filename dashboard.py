import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

from utils.secret import *
from utils.lufthansa import *
from utils.mongo import *

# Initialisez l'application Dash
app = dash.Dash(__name__)

# Récupérez les données de la collection 'airports'
data = get_data_from_mongo('airports')

# Préparez les données pour le tableau
if data:
    table_data = [
        {key: value for key, value in item.items() if key != '_id'}  # Exclure le champ '_id'
        for item in data
    ]
    columns = [{"name": i, "id": i} for i in table_data[0].keys()]
    airports_names = sorted({item['airport_name'] for item in table_data})
else:
    table_data = []
    columns = []
    airports_names = []

# Définir la mise en page de l'application Dash
app.layout = html.Div(children=[
    html.H1(children='Airports Data from MongoDB'),
    html.Div(children='''
        PlaneDash: A web application dedicated to Lufthansa flights in Europe.
    '''),

    dcc.Dropdown(
        id='airport-filter',
        options=[{'label': name, 'value': name} for name in airports_names],
        multi=True,
        placeholder="Select airports"
    ),

    dash_table.DataTable(
        id='table',
        columns=columns,
        data=table_data,
    )
])

# Callback pour mettre à jour le tableau en fonction du filtre sélectionné
@app.callback(
    Output('table', 'data'),
    [Input('airport-filter', 'value')]
)
def update_table(selected_airports):
    if not selected_airports:
        return table_data
    filtered_data = [row for row in table_data if row['airport_name'] in selected_airports]
    return filtered_data

if __name__ == '__main__':
    app.run_server(debug=True)
