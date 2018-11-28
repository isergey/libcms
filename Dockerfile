FROM ubuntu:16.04
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN apt-get update && apt-get upgrade -y && apt-get install -y \
        libyaz4-dev \
        libldap2-dev \
        python-pip \
        python-lxml \
        libmemcached-dev\
        libmysqlclient-dev\
        python-dev\
        g++
 RUN pip install --upgrade pip
 RUN pip install -r requirements.txt
 ADD . /code/

