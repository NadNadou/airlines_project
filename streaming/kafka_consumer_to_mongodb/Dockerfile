FROM python:3.9

WORKDIR /app

COPY kafka_consumer_to_mongodb/requirements.txt .
RUN pip install -r requirements.txt

COPY kafka_consumer_to_mongodb/kafka_consumer.py .

CMD ["python", "kafka_consumer.py"]