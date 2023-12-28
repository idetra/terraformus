FROM python:3.10-slim

RUN apt update

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /htc

COPY requirements.txt /htc/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /htc/

