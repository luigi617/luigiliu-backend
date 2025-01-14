# syntax=docker/dockerfile:1
# pull official base image
FROM python:3.11-slim
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# set work directory
WORKDIR /code



RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  poppler-utils \
  && rm -rf /var/lib/apt/lists/*



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