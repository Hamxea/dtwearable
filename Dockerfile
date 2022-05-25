FROM tensorflow/tensorflow:latest-py3

#Install postgressql developer package
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main" >/etc/apt/sources.list.d/pgdg.list
RUN apt-get install wget
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install postgresql-server-dev-11 gcc python3-dev musl-dev -y

RUN apt-get install nano

WORKDIR /app
#COPY . /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
#CMD flask run --host=0.0.0.0

#docker build -t hamzaharunamohammed/dtwearable .
#docker run -p 5000:5000 -v D:/source/desktop/dtwearable/:/app hamzaharunamohammed/dtwearable
#docker ps | docker stop d0fcfd68f1ac