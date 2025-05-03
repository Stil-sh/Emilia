import aiohttp
import random

async def get_random_waifu() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=rating:safe") as resp:
            data = await resp.json()
            return random.choice(data["post"])["file_url"]

async def search_waifu(tag: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags={tag}") as resp:
            data = await resp.json()
            if not data["post"]:
                raise ValueError("Тег не найден!")
            return random.choice(data["post"])["file_url"]
