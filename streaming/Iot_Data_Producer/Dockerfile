FROM python:3.9

WORKDIR /app

COPY Iot_Data_Producer/requirements.txt .
RUN pip install -r requirements.txt

COPY Iot_Data_Producer/kafka_producer.py .

CMD ["python", "kafka_producer.py"]