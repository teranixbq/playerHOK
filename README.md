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

### Pull from DockerHub

```bash
docker pull YOUR_USERNAME/playerhok:latest
docker run -p 8000:8000 YOUR_USERNAME/playerhok:latest
```

### Build locally

```bash
docker build -t playerhok .
docker run -p 8000:8000 playerhok
```

## Setup GitHub Actions (Auto-build to DockerHub)

1. Buat secrets di GitHub repository:
   - `DOCKERHUB_USERNAME` - Username DockerHub Anda
   - `DOCKERHUB_TOKEN` - Access token dari DockerHub

2. Setiap push ke branch `main` akan otomatis build & push ke DockerHub

## Docs

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
