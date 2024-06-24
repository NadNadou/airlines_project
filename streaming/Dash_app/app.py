import os
import json
import threading
from confluent_kafka import Consumer, KafkaError
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Shared dictionary to store flight data
flight_data = {
    'flight_id': ['LH102', 'LH453', 'LH610'],  # Dummy flight IDs
    'latitude': [50.0379, 48.3538, 48.1102],   # Dummy coordinates
    'longitude': [8.5622, 11.7861, 16.5697]
}
lock = threading.Lock()

def consumer_thread(topics):
    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'flight-consumer',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(topics)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    break

            data = json.loads(msg.value().decode('utf-8'))
            print(f"Received data: {data}")  # Debugging: print received data
            with lock:
                flight_id = data['flight_id']
                index = flight_data['flight_id'].index(flight_id) if flight_id in flight_data['flight_id'] else None

                if index is not None:
                    flight_data['latitude'][index] = data['location']['latitude']
                    flight_data['longitude'][index] = data['location']['longitude']
                    print(f"Updated flight data: {flight_data}")  # Debugging: print updated data
                else:
                    flight_data['flight_id'].append(flight_id)
                    flight_data['latitude'].append(data['location']['latitude'])
                    flight_data['longitude'].append(data['location']['longitude'])
                    print(f"Appended new flight data: {flight_data}")  # Debugging: print new data

    finally:
        consumer.close()

def start_consumer():
    flight_topics = ['flight_LH102', 'flight_LH453', 'flight_LH610']  # Add other flight topics as needed
    threading.Thread(target=consumer_thread, args=(flight_topics,), daemon=True).start()

# Dash app setup
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='europe-map',
        style={'height': '100vh'}
    ),
    dcc.Interval(
        id='interval-component',
        interval=6 * 1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='loading-indicator', children='Loading...', style={'display': 'block'})  # Loading indicator
])

@app.callback(
    [Output('europe-map', 'figure'), Output('loading-indicator', 'style')],
    [Input('interval-component', 'n_intervals')]
)
def update_map(n):
    with lock:
        df = pd.DataFrame(flight_data)

    # Debugging: print the DataFrame
    print(f"DataFrame to plot: {df}")

    if df.empty:
        return {}, {'display': 'block'}

    fig = px.scatter_mapbox(
        df, lat='latitude', lon='longitude', hover_name='flight_id', zoom=4,
        mapbox_style="open-street-map"
    )
    return fig, {'display': 'none'}  # Hide loading indicator when data is available

if __name__ == '__main__':
    # Start single Kafka consumer thread as a daemon
    start_consumer()

    # Run Dash app
    app.run_server(debug=True)
