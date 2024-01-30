FROM python:3-alpine3.9

RUN apk update && \
    apk add --virtual python3-dev libpq-dev

COPY app /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN pip install wheel setuptools Flask psycopg2==2.8.6

EXPOSE 80

CMD ["python", "app.py"]
