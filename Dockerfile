FROM python:3.9


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

COPY app /app/
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install

WORKDIR /app
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080", "--reload"]
