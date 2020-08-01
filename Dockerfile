FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

LABEL maintainer="toni057"

COPY ./app /app
COPY ./models /models

ADD requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt