import aiohttp
import random
from typing import Optional

DANBOORU_API = "https://danbooru.donmai.us"
HEADERS = {"User-Agent": "AnimeBot/1.0"}

class DanbooruParser:
    def __init__(self):
        self.session = aiohttp.ClientSession(headers=HEADERS)
        self.cache = {}

    async def get_random_post(self, tags: str) -> Optional[dict]:
        """Получает случайный пост с Danbooru"""
        cache_key = f"tags_{hash(tags)}"
        if cache_key in self.cache:
            return random.choice(self.cache[cache_key])

        try:
            params = {
                "tags": f"{tags} rating:safe",
                "limit": 50,
                "random": "true"
            }
            
            async with self.session.get(
                f"{DANBOORU_API}/posts.json",
                params=params,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    posts = await response.json()
                    if posts:
                        self.cache[cache_key] = posts
                        return random.choice(posts)
        except Exception as e:
            print(f"Danbooru API error: {e}")
        return None

    async def get_image_url(self, tags: str) -> str:
        """Возвращает URL изображения или фолбэк"""
        post = await self.get_random_post(tags)
        
        if post and 'file_url' in post:
            return f"https://danbooru.donmai.us{post['file_url']}"
        
        # Фолбэк изображения
        fallbacks = [
            "https://i.imgur.com/9pNffOY.jpg",
            "https://i.imgur.com/JQ1v0Yl.png"
        ]
        return random.choice(fallbacks)

    async def close(self):
        await self.session.close()

# Глобальный экземпляр парсера
parser = DanbooruParser()

async def get_danbooru_image(tags: str) -> str:
    """Интерфейсная функция для получения изображения"""
    return await parser.get_image_url(tags)
