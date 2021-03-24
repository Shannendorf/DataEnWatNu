FROM python:3.9.2-buster

ENV DATABASE_URL postgresql+psycopg2://postgres@127.0.0.1/DataEnWatNu

WORKDIR /usr/src/app

RUN apt-get update -y
RUN apt-get install -y texlive-full
RUN apt-get install tree

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app

RUN tree /usr/src/app
RUN chmod +x /usr/src/app/tools/generate_radar_plot.py

CMD ["/usr/src/app/entrypoint.sh"]