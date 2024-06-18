from dashboard import Dash, dcc, html
import dash_table
from utils.secret import db_mongo
from utils.mongo import get_data_from_mongo

# Créez l'application Dash
dash_app = Dash(__name__)

# Récupérez les données de la collection 'airports'
data = get_data_from_mongo('airports')

print(data)


# Préparez les données pour le tableau
if data:
    table_data = [
        {key: value for key, value in item.items() if key != '_id'}  # Exclure le champ '_id'
        for item in data
    ]
    columns = [{"name": i, "id": i} for i in table_data[0].keys()]
else:
    table_data = []
    columns = []

# Définir la mise en page de l'application Dash
dash_app.layout = html.Div(children=[
    html.H1(children='Airports Data from MongoDB'),

    dash_table.DataTable(
        id='table',
        columns=columns,
        data=table_data,
    )
])

# Exécuter l'application Dash
if __name__ == '__main__':
    dash_app.run_server(debug=True)
