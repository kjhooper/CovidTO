FROM python:3.7

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install Flask gunicorn mpld3 geopandas matplotlib tensorflow

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app