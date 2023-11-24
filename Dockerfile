FROM ubuntu:xenial AS build

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y &&\
    apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev\
    libnss3-dev libssl-dev libreadline-dev libffi-dev wget -y

ENV PYTHON_VERSION=3.8.16

RUN mkdir ~/tmp && cd ~/tmp && \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz &&\
    tar -xvzf Python-${PYTHON_VERSION}.tgz &&\
    cd Python-${PYTHON_VERSION} && ./configure --with-ensurepip=install && make altinstall

RUN pip3.8 install pipenv

WORKDIR /fiuba_news_bot

COPY Pipfile requirements.txt ./

RUN pipenv install -r requirements.txt
RUN pipenv --python 3.8

COPY src ./src/
COPY .env start.sh ./

CMD [ "./start.sh" ]