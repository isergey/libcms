FROM ubuntu:16.04
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN apt-get update && apt-get install -y \
        python-pip \
        python-lxml \
        memcached \
        libmemcached-dev\
        libmysqlclient-dev\
        python-dev\
        g++
 RUN pip install -r requirements.txt
 ADD . /code/

