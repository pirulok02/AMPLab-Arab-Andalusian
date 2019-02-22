FROM ubuntu

COPY requirements.txt /

RUN apt-get update
RUN apt install -y python3.7
RUN apt install -y python3-pip
RUN apt-get install -y vim
RUN pip3 install 'setuptools<20.2'

RUN mkdir /data

RUN pip3 install -r requirements.txt

WORKDIR /data

COPY . .

