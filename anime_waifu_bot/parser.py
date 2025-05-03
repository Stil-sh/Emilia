import aiohttp
import random

async def get_anime_image(category="", nsfw=False):
    try:
        if nsfw:
            return "https://i.imgur.com/NSFW_EXAMPLE.jpg"
        return f"https://i.imgur.com/{random.randint(100000, 999999)}.jpg"
    except Exception:
        return "https://i.imgur.com/DEFAULT_IMAGE.jpg"
