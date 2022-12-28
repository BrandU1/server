FROM ubuntu:22.04

COPY . .

RUN update && install -y
RUN install -y python3.10 python3-pip virtualenv
RUN virtualenv .venv --python=python3.10
RUN . .venv/bin/activate

RUN pip install -r requirements/prod.txt
#RUN python3 manage.py collectstatic --noinput --settings=server.settings.staging

EXPOSE 80