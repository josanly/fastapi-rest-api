FROM python:3.9.17-alpine3.18 AS builder
LABEL maintainer="josso.adrien@gmail.com"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 80
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# Use CMD to add uvicorn option
