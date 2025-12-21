FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the data directory exists
RUN mkdir -p src/data

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "src/app.py"]