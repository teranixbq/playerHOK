#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import json
import sys
import time


class HOKPlaywrightScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        )
        self.page = self.context.new_page()
        return self

    def get_player_info(self, game_id):
        url = f"https://camp.honorofkings.com/h5/app/index.html#/settings/personal-homepage?userType=3&visitor_id={game_id}"
        
        print(f"Fetching data for game ID: {game_id}")
        self.page.goto(url, wait_until='networkidle')
        time.sleep(2)
        
        result = self.page.evaluate("""
            (gameId) => {
                let charName = '';
                const usernameSelectors = [
                    '[class*="username"]',
                    '[class*="name"]',
                    '[class*="nickname"]',
                    '.personal-homepage [class*="name"]'
                ];
                
                for (const selector of usernameSelectors) {
                    const el = document.querySelector(selector);
                    if (el && el.innerText && el.innerText.trim().length > 0 && el.innerText.trim().length < 50) {
                        charName = el.innerText.trim();
                        break;
                    }
                }
                
                if (!charName) {
                    const allDivs = Array.from(document.querySelectorAll('div, span'));
                    const candidates = allDivs.filter(el => {
                        const text = el.innerText?.trim();
                        return text && text.length > 0 && text.length < 30 && !text.includes('\\n');
                    });
                    
                    if (candidates.length > 0) {
                        charName = candidates[0].innerText.trim();
                    }
                }
                
                let headUrl = '';
                const avatarSelectors = [
                    '.avatar img',
                    '[class*="avatar"] img',
                    '.personal-homepage img'
                ];
                
                for (const selector of avatarSelectors) {
                    const el = document.querySelector(selector);
                    if (el && el.src && (el.src.includes('avatar') || el.src.includes('head') || el.src.includes('upload'))) {
                        headUrl = el.src;
                        break;
                    }
                }
                
                if (!headUrl) {
                    const allImages = Array.from(document.querySelectorAll('img'));
                    const potentialAvatar = allImages.find(img => 
                        img.width > 50 && img.height > 50 && 
                        (img.src.includes('avatar') || img.src.includes('head') || img.src.includes('upload') || img.src.includes('client'))
                    );
                    if (potentialAvatar) headUrl = potentialAvatar.src;
                }
                
                return {
                    gameId: gameId,
                    characName: charName || 'Not found',
                    headUrl: headUrl || 'Not found'
                };
            }
        """, game_id)
        
        return result

    def get_multiple_players(self, game_ids):
        results = []
        for game_id in game_ids:
            info = self.get_player_info(game_id)
            results.append(info)
            time.sleep(1)
        return results

    def close(self):
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python hok_scraper.py <game_id> [game_id2] ...")
        print("Example: python hok_scraper.py 9392966519886164346")
        sys.exit(1)
    
    game_ids = sys.argv[1:]
    
    with HOKPlaywrightScraper(headless=True) as scraper:
        if len(game_ids) == 1:
            result = scraper.get_player_info(game_ids[0])
            print("\n" + "="*60)
            print("PLAYER INFORMATION")
            print("="*60)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            results = scraper.get_multiple_players(game_ids)
            print("\n" + "="*60)
            print("PLAYERS INFORMATION")
            print("="*60)
            print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
