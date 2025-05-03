import aiohttp
from bs4 import BeautifulSoup
import random

class ScrolllerParser:
    def __init__(self, proxy=None):
        self.proxy = proxy
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    async def get_posts(self, subreddit: str, limit=3):
        url = f"https://scrolller.com/r/{subreddit}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                proxy=self.proxy,
                headers=self.headers,
                timeout=10
            ) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    posts = []
                    for item in soup.select('div[data-testid="post-container"]')[:limit]:
                        img = item.find('img')
                        if img and 'src' in img.attrs:
                            posts.append({
                                'url': img['src'],
                                'type': 'gif' if '.gif' in img['src'] else 'image'
                            })
                    
                    return posts or [{
                        'url': 'https://i.imgur.com/neko_fallback.jpg',
                        'type': 'image'
                    }]
                raise Exception(f"Status: {resp.status}")
