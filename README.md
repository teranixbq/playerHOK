# Honor of Kings Profile Scraper API

REST API untuk mengambil **avatar** dan **game name** pemain Honor of Kings berdasarkan Game ID.

## Features

- ✅ REST API dengan FastAPI
- ✅ Playwright scraper (tidak perlu install Chrome)
- ✅ Docker support
- ✅ Auto-generated API docs

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run API
python src/api.py
```

API akan berjalan di `http://localhost:8000`

### Docker

```bash
# Build
docker build -t hok-scraper-api .

# Run
docker run -p 8000:8000 hok-scraper-api
```

## API Endpoints

### GET /player/{game_id}

Ambil data single player

```bash
curl http://localhost:8000/player/9392966519886164346
```

**Response:**
```json
{
  "gameId": "9392966519886164346",
  "characName": "ノデニクス",
  "headUrl": "https://camp.honorofkings.com/client/upload/hok/avatar/..."
}
```

### POST /players

Ambil data multiple players

```bash
curl -X POST http://localhost:8000/players \
  -H "Content-Type: application/json" \
  -d '{"game_ids": ["9392966519886164346", "1284190959244230155"]}'
```

**Response:**
```json
[
  {
    "gameId": "9392966519886164346",
    "characName": "ノデニクス",
    "headUrl": "https://..."
  },
  {
    "gameId": "1284190959244230155",
    "characName": "MүsticͥEͣyͫesツ",
    "headUrl": "https://..."
  }
]
```

## Documentation

Akses interactive API docs di:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
