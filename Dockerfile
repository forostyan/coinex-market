FROM python:3.8.10

LABEL maintainer='Vladislav Forostyn', email='e.shakhmaev@timeweb.ru'

ENV TZ='Europe/Moscow'

WORKDIR /code

RUN apt-get update && apt-get install -y gcc

# installing python stuff
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python /code/tgbot.py