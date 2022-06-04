FROM python:3.6.10-buster

COPY dipmp_server /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]