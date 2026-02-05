# HOK Profile Scraper API

REST API untuk scraping data pemain Honor of Kings (avatar & game name).

## Quick Start

```bash
# Install
pip install -r requirements.txt
playwright install chromium

# Run
python src/api.py
```

## API Endpoints

### GET /player/{game_id}

```bash
curl http://localhost:8000/player/1234567890123456789
```

Response:
```json
{
  "gameId": "1234567890123456789",
  "characName": "PlayerName",
  "headUrl": "https://..."
}
```

### POST /players

```bash
curl -X POST http://localhost:8000/players \
  -H "Content-Type: application/json" \
  -d '{"game_ids": ["1234567890", "9876543210"]}'
```

## Docker

```bash
docker build -t hok-api .
docker run -p 8000:8000 hok-api
```

## Docs

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
