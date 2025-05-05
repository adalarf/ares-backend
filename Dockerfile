FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && \
    PIP_NO_CACHE_DIR=off pipenv install --system --deploy

COPY . .

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
