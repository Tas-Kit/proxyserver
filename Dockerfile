FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /proxyserver
WORKDIR /proxyserver
ADD requirements.txt /proxyserver/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y gettext
ADD . /proxyserver/
CMD python manage.py runsslserver 0.0.0.0:8000
