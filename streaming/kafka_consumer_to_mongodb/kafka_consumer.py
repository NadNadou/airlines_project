import os
import threading
import json
from confluent_kafka import Consumer, KafkaException, KafkaError
from pymongo import MongoClient

# Environment Variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
MONGO_URI = "mongodb://localhost:27017"  # Update this to your local MongoDB URI

def mongodb_insert_flight_data(flight_id, flight_data):
    try:
        client = MongoClient(MONGO_URI)
        db = client['iot_flights']
        collection = db[flight_id]

        # Insert data into the collection
        collection.insert_one({
            'flight_id': flight_data['flight_id'],
            'airline_name': flight_data['airline_name'],
            'timestamp': flight_data['timestamp'],
            'departure_country': flight_data['departure_country'],
            'arrival_country': flight_data['arrival_country'],
            'departure_airport': flight_data['departure_airport'],
            'arrival_airport': flight_data['arrival_airport'],
            'latitude': flight_data['location']['latitude'],
            'longitude': flight_data['location']['longitude'],
            'speed': flight_data['speed'],
            'altitude': flight_data['altitude']
        })

        client.close()

    except Exception as e:
        print(f"Error connecting to MongoDB or inserting data: {e}")

def kafka_consume_and_process(flight_id):
    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': f'flight-consumer-{flight_id}',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([f"flight_{flight_id}"])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Process message
            try:
                flight_data = json.loads(msg.value().decode('utf-8'))
                mongodb_insert_flight_data(flight_id, flight_data)
            except Exception as e:
                print(f"Error processing message: {e}")

    except KeyboardInterrupt:
        print(f"Consumer for flight {flight_id} interrupted")
    finally:
        consumer.close()

def consume_flights():
    threads = []
    for flight in ['LH102', 'LH453', 'LH610']:
        thread = threading.Thread(target=kafka_consume_and_process, args=(flight,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    consume_flights()
