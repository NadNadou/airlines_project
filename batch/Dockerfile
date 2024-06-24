from ubuntu:18.04

RUN apt update && apt clean  && apt install -y python3 python3-pip curl cron\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD test /app/test
ADD utils /app/utils
ADD app.py /app/app.py
ADD requirements.txt /app/requirements.txt
ADD update_mongo.sh /app/update_mongo.sh
ADD crontab /etc/cron.d/crontab

RUN pip3 install -r requirements.txt 
RUN chmod +x /app/update_mongo.sh
RUN chmod 0644  /etc/cron.d/crontab  


EXPOSE 8000

CMD cron && python3 app.py 




