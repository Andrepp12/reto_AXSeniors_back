# Use an official Python runtime as the base image
FROM python:3.13-slim

WORKDIR /app

ARG PORT=8000
ENV PORT=${PORT}

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev pkg-config

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${PORT}

ENTRYPOINT ["/bin/bash", "-c", "python3 manage.py runserver 0.0.0.0:$PORT"]
