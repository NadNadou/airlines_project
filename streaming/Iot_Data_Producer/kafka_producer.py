import os
import random
import uuid
from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime
import time
import threading

# Flight data definitions
flights = [
    {
        "flight_id": "LH102",
        "airline_name": "Lufthansa",
        "departure_country": "Germany",
        "departure_airport": "Frankfurt Airport",
        "departure_position": {"latitude": 50.0379, "longitude": 8.5622},
        "arrival_country": "UK",
        "arrival_airport": "Heathrow Airport",
        "arrival_position": {"latitude": 51.4700, "longitude": -0.4543}
    },
    {
        "flight_id": "LH453",
        "airline_name": "Lufthansa",
        "departure_country": "Germany",
        "departure_airport": "Munich Airport",
        "departure_position": {"latitude": 48.3538, "longitude": 11.7861},
        "arrival_country": "France",
        "arrival_airport": "Charles de Gaulle Airport",
        "arrival_position": {"latitude": 49.0034, "longitude": 2.5673}
    },
    {
        "flight_id": "LH610",
        "airline_name": "Lufthansa",
        "departure_country": "Austria",
        "departure_airport": "Vienna International Airport",
        "departure_position": {"latitude": 48.1102, "longitude": 16.5697},
        "arrival_country": "Spain",
        "arrival_airport": "Barcelona–El Prat Airport",
        "arrival_position": {"latitude": 41.2971, "longitude": 2.0785}
    },
]

# Filter flights to include only those between France, Germany, and Spain
filtered_flights = [flight for flight in flights if flight['departure_country'] in ['France', 'Germany', 'Spain'] or flight['arrival_country'] in ['France', 'Germany', 'Spain']]

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

def calculate_flight_movement(departure_position, arrival_position, step, total_steps):
    fraction = min(step / total_steps, 1.0)  # Cap fraction at 1.0

    # Calculate current position
    current_position = {
        'latitude': departure_position['latitude'] + (arrival_position['latitude'] - departure_position['latitude']) * fraction,
        'longitude': departure_position['longitude'] + (arrival_position['longitude'] - departure_position['longitude']) * fraction
    }

    # Add some randomness to simulate flight path
    current_position['latitude'] += random.uniform(-0.0005, 0.0005)
    current_position['longitude'] += random.uniform(-0.0005, 0.0005)

    # Check if flight has arrived
    if fraction >= 1.0:
        current_position = arrival_position

    return current_position

def generate_flight_data(flight, step, total_steps):
    movement = calculate_flight_movement(flight['departure_position'], flight['arrival_position'], step, total_steps)
    return {
        'flight_id': flight['flight_id'],
        'airline_name': flight['airline_name'],
        'timestamp': datetime.now().isoformat(),
        'departure_country': flight['departure_country'],
        'arrival_country': flight['arrival_country'],
        'departure_airport': flight['departure_airport'],
        'arrival_airport': flight['arrival_airport'],
        'location': movement,
        'speed': random.uniform(400, 900),  # Simulate flight speed in km/h
        'altitude': random.uniform(8000, 12000),  # Simulate altitude in meters
    }

def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not serializable')

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic=topic,
        key=str(data['flight_id']),
        value=json.dumps(data, default=json_serializer),
        on_delivery=delivery_report
    )
    producer.flush()

def simulate_flight(producer, flight):
    total_steps = 100
    flight_topic = f"flight_{flight['flight_id']}"  # Create flight-specific topic
    for step in range(total_steps + 1):
        flight_data = generate_flight_data(flight, step, total_steps)
        produce_data_to_kafka(producer, flight_topic, flight_data)
        # Sleep for 5 seconds before updating position
        time.sleep(5)

def simulate_flights(producer):
    threads = []
    for flight in filtered_flights:
        thread = threading.Thread(target=simulate_flight, args=(producer, flight))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }
    producer = SerializingProducer(producer_config)
    try:
        simulate_flights(producer)
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')
