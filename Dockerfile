FROM python:3.11-slim

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt create_db.py ./
COPY app app

RUN pip install -r requirements.txt
RUN apt update && apt -y install libpq-dev gcc && pip install psycopg2

EXPOSE 8010
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]