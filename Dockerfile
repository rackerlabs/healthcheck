FROM python:2.7

WORKDIR /canary/

ADD requirements/common.txt /canary/common.txt
ADD requirements/dev.txt /canary/dev.txt
RUN pip install -r dev.txt

ADD . /canary

CMD python /canary/manage.py