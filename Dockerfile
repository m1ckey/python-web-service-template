FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /app
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
# https://www.uvicorn.org/deployment/
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 -k uvicorn.workers.UvicornWorker main:app
