FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY somesite .

CMD ["gunicorn", "somesite.wsgi:application", "--bind", "0.0.0.0:8000"]