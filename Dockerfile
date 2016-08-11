FROM python:2.7

WORKDIR /canary/

ADD requirements/common.txt /canary/common.txt
ADD requirements/dev.txt /canary/dev.txt
RUN pip install -r dev.txt
RUN adduser --disabled-password --gecos '' canary-worker
ENV FLASK_APP=healthcheck/manage.py
ENV FLASK_CONFIG=docker
ADD . /canary
CMD flask run --host=0.0.0.0 --port=5000
