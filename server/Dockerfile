FROM python:3.10

COPY . .

RUN apt update && apt install -y
RUN pip install virtualenv
RUN virtualenv .venv
RUN . .venv/bin/activate

RUN pip install -r requirements/dev.txt

EXPOSE 8000
