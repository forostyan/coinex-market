FROM python:3.8.10-slim

LABEL maintainer='Vladislav Forostyn', email='vlad_forostyan@mail.ru'
EXPOSE 5000

ENV TZ='Europe/Moscow'

WORKDIR /code
COPY ./telegram_bot /code/telegram_bot
COPY ./tgbot.py /code/tgbot.py
COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gcc

# installing python stuff
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "/code/tgbot.py"]