from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from hok_scraper import HOKScraper
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
async def get_player(game_id: str):
    scraper = HOKScraper(headless=True)
    try:
        await scraper.start()
        result = await scraper.get_player_info(game_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await scraper.close()

@app.post("/players", response_model=List[PlayerResponse])
async def get_players(request: MultiplePlayersRequest):
    scraper = HOKScraper(headless=True)
    try:
        await scraper.start()
        results = []
        for gid in request.game_ids:
            # Pyppeteer might need small delay between navigations to avoid issues
            results.append(await scraper.get_player_info(gid))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await scraper.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
