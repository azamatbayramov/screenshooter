FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install playwright python-telegram-bot && \
    playwright install --with-deps chromium

WORKDIR /app

COPY capture_screenshot.py .
COPY cleanup_screenshots.py .
COPY telegram_sender.py .

RUN mkdir -p /app/screenshots

CMD python3 capture_screenshot.py