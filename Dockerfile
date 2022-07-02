FROM python:3.10 as poetry

WORKDIR /app

RUN curl -sSLo install-poetry.py https://install.python-poetry.org
ENV POETRY_HOME=/app/poetry
RUN python3 install-poetry.py --yes
ENV PATH=$POETRY_HOME/bin:$PATH

RUN poetry --version

COPY pyproject.toml poetry.lock ./
RUN poetry export -o requirements.txt

FROM python:3.10

WORKDIR /app

COPY --from=poetry /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY config config/
COPY db db/
COPY log log/
COPY server server/

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
# https://www.uvicorn.org/deployment/
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 -k uvicorn.workers.UvicornWorker main:app
