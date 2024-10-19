# syntax=docker/dockerfile:1
# pull official base image
FROM python:3.9
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# set work directory
WORKDIR /code

# install psycopg2 dependencies
# RUN apk update
# RUN apk add postgresql-dev gcc python3-dev musl-dev
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
COPY ./compose/local/entrypoint.sh /entrypoint.sh
RUN sed -i "s/\r$//g" /entrypoint.sh
RUN chmod +x /entrypoint.sh



COPY . /code/

ENTRYPOINT ["/entrypoint.sh"]