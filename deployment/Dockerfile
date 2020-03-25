# pull official base image
FROM python:3.8.0-alpine

# set work directory
RUN mkdir /yaatra
WORKDIR /yaatra

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /yaatra/
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt

# copy project
COPY . /yaatra/
