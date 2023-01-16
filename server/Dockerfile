FROM ubuntu:22.04

COPY . .

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3.10 python3-pip virtualenv
RUN virtualenv .venv --python=python3.10
RUN . .venv/bin/activate

RUN python3 manage.py test

RUN pip3 install -r requirements/prod.txt
#RUN python3 manage.py collectstatic --noinput --settings=server.settings.staging

EXPOSE 80