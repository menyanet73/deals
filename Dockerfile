FROM python:3.10-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean\
&& apt-get install netcat -y\
&& apt-get install curl -y 


ENV PATH="${PATH}:/usr/local/bin/python" \
    PYTHONUNBUFFERED=1

WORKDIR /app
ADD . /app/

RUN pip install --upgrade pip\
    && pip install -r requirements.txt\
    && python manage.py collectstatic --noinput
