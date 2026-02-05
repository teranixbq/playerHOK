from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from hok_scraper import HOKPlaywrightScraper
from typing import List
import uvicorn

app = FastAPI(title="HOK Profile Scraper API")

class PlayerRequest(BaseModel):
    game_id: str

class MultiplePlayersRequest(BaseModel):
    game_ids: List[str]

class PlayerResponse(BaseModel):
    gameId: str
    characName: str
    headUrl: str

@app.get("/")
def root():
    return {"message": "HOK Profile Scraper API", "endpoints": ["/player/{game_id}", "/players"]}

@app.get("/player/{game_id}", response_model=PlayerResponse)
def get_player(game_id: str):
    try:
        with HOKPlaywrightScraper(headless=True) as scraper:
            result = scraper.get_player_info(game_id)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/players", response_model=List[PlayerResponse])
def get_players(request: MultiplePlayersRequest):
    try:
        with HOKPlaywrightScraper(headless=True) as scraper:
            results = scraper.get_multiple_players(request.game_ids)
            return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
