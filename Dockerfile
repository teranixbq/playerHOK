FROM python:3.9-alpine

# Install Chromium and dependencies
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Tell Pyppeteer to use system Chromium
# On Alpine, the binary is usually at /usr/bin/chromium-browser
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

WORKDIR /app

# Install Pyppeteer
RUN pip install --no-cache-dir pyppeteer

COPY src/hok_scraper.py .

ENTRYPOINT ["python", "hok_scraper.py"]
