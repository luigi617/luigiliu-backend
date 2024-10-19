# syntax=docker/dockerfile:1
# pull official base image
FROM python:3.9
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# set work directory
WORKDIR /code

# install psycopg2 dependencies



RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  && apt-get install -y poppler-utils

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./compose/production/entrypoint.sh /entrypoint.sh
RUN sed -i "s/\r$//g" /entrypoint.sh
RUN chmod +x /entrypoint.sh

# copy start
COPY ./compose/production/start.sh /start.sh
RUN sed -i "s/\r$//g" /start.sh
RUN chmod +x /start.sh

COPY . /code/

ENTRYPOINT ["/entrypoint.sh"]