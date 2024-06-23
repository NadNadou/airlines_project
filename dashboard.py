import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import datetime
import pandas as pd

from utils.secret import *
from utils.lufthansa import *
from utils.mongo import *
import datetime

# Lien CDN pour Bootstrap
external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
]

# Initialisez l'application Dash
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

# Récupérez les données combinaison departure x arrival
unique_departure_cities, unique_arrival_cities, combinations_departure_arrival, df_intermediate = get_from_data()

# Définir les dates minimales et maximales
min_date = datetime.date(2024, 6, 22)
max_date = datetime.date(2025, 6, 22)

app.layout = html.Div([
    html.H1("Airlines, des milliers de vols au bout de votre souris.", className='header'),

    html.Div([
        html.Div([
            html.Label('De', className='label'),
            html.Br(),
            dcc.Dropdown(
                id='from-dropdown',
                options=[{'label': city, 'value': city} for city in unique_departure_cities],
                value=unique_departure_cities[0]  # Valeur par défaut
            )
        ], className='element col-lg-6'),

        html.Div([
            html.Label('Vers', className='label'),
            html.Br(),
            dcc.Dropdown(
                id='to-dropdown',
                options=[],
                value=''
            )
        ], className='element col-lg-6'),
         html.Div([
            html.Label('Départ', className='label'),
            html.Br(),
            dcc.DatePickerSingle(
                id='depart-date',
                placeholder='Ajouter une date',
                min_date_allowed=min_date,
                max_date_allowed=max_date
            )
        ], className='element col-lg-6'),

        html.Div([
            html.Label('Retour', className='label'),
            html.Br(),
            dcc.DatePickerSingle(
                id='return-date',
                placeholder='Ajouter une date',
                min_date_allowed=min_date,
                max_date_allowed=max_date
            )
        ], className='element col-lg-6'),

       

    ], className='container row'),

    html.Div([
        html.Br(),
        html.Button('Rechercher', id='search-button', n_clicks=0, className='btn btn-primary'),
    ], className='button-container'),

    html.Div(id='results-container')
])

# Callback pour mettre à jour les options du dropdown "Vers" en fonction de la sélection dans le dropdown "De"
@app.callback(
    Output('to-dropdown', 'options'),
    Input('from-dropdown', 'value')
)
def set_arrival_options(selected_departure_city):
    filtered_combinations = [
        {'label': comb['arrival_city_name'], 'value': comb['arrival_city_name']}
        for comb in combinations_departure_arrival
        if comb['departure_city_name'] == selected_departure_city
    ]
    return filtered_combinations

# Callback pour afficher les résultats de la recherche
@app.callback(
    Output('results-container', 'children'),
    Input('search-button', 'n_clicks'),
    State('from-dropdown', 'value'),
    State('to-dropdown', 'value'),
    State('depart-date', 'date'),
    State('return-date', 'date')
)
def update_results(n_clicks, from_city, to_city, depart_date, return_date):
    if n_clicks > 0 and from_city and to_city and depart_date:
        filtered_df = df_intermediate[
            (df_intermediate['departure_city_name'] == from_city) &
            (df_intermediate['arrival_city_name'] == to_city) &
            (df_intermediate['departure_scheduled_time'].str.startswith(depart_date))
        ][["duration", "departure_city_name", "arrival_city_name", "departure_scheduled_time", "arrival_scheduled_time"]].drop_duplicates()
        
        filtered_df['departure_scheduled_time'] = pd.to_datetime(filtered_df['departure_scheduled_time'])
        filtered_df['arrival_scheduled_time'] = pd.to_datetime(filtered_df['arrival_scheduled_time'])
        
        filtered_df['Date de départ'] = filtered_df['departure_scheduled_time'].dt.strftime('%d/%m/%Y')
        filtered_df['Heure de départ'] = filtered_df['departure_scheduled_time'].dt.strftime('%Hh%M')
        filtered_df['Date d\'arrivée'] = filtered_df['arrival_scheduled_time'].dt.strftime('%d/%m/%Y')
        filtered_df['Heure d\'arrivée'] = filtered_df['arrival_scheduled_time'].dt.strftime('%Hh%M')

        filtered_df = filtered_df.rename(columns={
            'duration': 'Durée',
            'departure_city_name': 'De',
            'arrival_city_name': 'Vers'
        })
        
        filtered_df = filtered_df[["Durée", "De", "Vers", "Date de départ", "Heure de départ", "Date d'arrivée", "Heure d'arrivée"]]
        
        if filtered_df.empty:
            return html.Div("Aucun vol trouvé pour les critères sélectionnés.")
        
        return html.Br(),html.Div([
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in filtered_df.columns],
                data=filtered_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                page_size=10  # Nombre de lignes par page
            )
        ])
    return html.Div()

if __name__ == '__main__':
    app.run_server(debug=True)
