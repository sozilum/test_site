FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip "poetry==1.7.1"
RUN poetry config virtyalenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY somesite .

CMD ["gunicorn", "somesite.wsgi:application", "--bind", "0.0.0.0:8000"]