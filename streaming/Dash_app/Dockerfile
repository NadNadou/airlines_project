FROM python:3.9

WORKDIR /app

COPY Dash_app/requirements.txt .
RUN pip install -r requirements.txt

COPY Dash_app/app.py .

CMD ["python", "app.py"]