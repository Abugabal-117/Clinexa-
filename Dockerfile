FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/src/data

ENV FLASK_APP=src/app.py
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "src/app.py"]
