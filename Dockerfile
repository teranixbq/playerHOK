FROM python:3.11-slim

WORKDIR /app

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY src/ ./src/

EXPOSE 8000

CMD ["python", "src/api.py"]
