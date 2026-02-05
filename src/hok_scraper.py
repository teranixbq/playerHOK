#!/usr/bin/env python3
import asyncio
import json
import sys
from pyppeteer import launch

import os

class HOKScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
    
    async def start(self):
        launch_args = {
            'headless': self.headless,
            'args': ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        }
        
        if os.environ.get('PYPPETEER_EXECUTABLE_PATH'):
            launch_args['executablePath'] = os.environ.get('PYPPETEER_EXECUTABLE_PATH')
            
        self.browser = await launch(**launch_args)
        self.page = await self.browser.newPage()
        await self.page.setUserAgent(
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        return self
    
    async def get_player_info(self, game_id):
        url = f"https://camp.honorofkings.com/h5/app/index.html#/settings/personal-homepage?userType=3&visitor_id={game_id}"
        
        try:
            await self.page.goto(url, {'waitUntil': 'networkidle2', 'timeout': 30000})
            await self.page.waitForFunction('document.querySelector(".personal-homepage") !== null', {'timeout': 15000})
        except:
            pass 
        
        await asyncio.sleep(2)
        
        return await self.page.evaluate('''(gameId) => {
            let charName = '';
            const nameSelectors = ['[class*="username"]', '[class*="name"]', '[class*="nickname"]', '.personal-homepage [class*="name"]'];
            
            for (const s of nameSelectors) {
                const el = document.querySelector(s);
                if (el && el.innerText?.trim()) {
                    charName = el.innerText.trim();
                    break;
                }
            }
            
            if (!charName) {
                const candidates = Array.from(document.querySelectorAll('div, span')).filter(el => {
                    const t = el.innerText?.trim();
                    return t && t.length > 0 && t.length < 30 && !t.includes('\\n');
                });
                if (candidates.length) charName = candidates[0].innerText.trim();
            }
            
            let headUrl = '';
            const avatarSelectors = ['.avatar img', '[class*="avatar"] img', '.personal-homepage img'];
            
            for (const s of avatarSelectors) {
                const el = document.querySelector(s);
                if (el && el.src && (el.src.includes('avatar') || el.src.includes('head'))) {
                    headUrl = el.src;
                    break;
                }
            }
            
            if (!headUrl) {
                const img = Array.from(document.querySelectorAll('img')).find(i => 
                    i.width > 50 && (i.src.includes('avatar') || i.src.includes('head') || i.src.includes('upload'))
                );
                if (img) headUrl = img.src;
            }
            
            return { gameId, characName: charName || 'Not found', headUrl: headUrl || 'Not found' };
        }''', game_id)
    
    async def close(self):
        if self.browser:
            await self.browser.close()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python hok_scraper.py <game_id>")
        sys.exit(1)
    
    scraper = HOKScraper()
    try:
        await scraper.start()
        game_ids = sys.argv[1:]
        results = []
        
        for gid in game_ids:
            results.append(await scraper.get_player_info(gid))
            
        print(json.dumps(results[0] if len(results) == 1 else results, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
