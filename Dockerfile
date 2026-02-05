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

# Install Pyppeteer and API dependencies
RUN pip install --no-cache-dir pyppeteer fastapi uvicorn pydantic requests

COPY src/ src/

# Expose API port
EXPOSE 8000

# Run API server by default
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
