import aiohttp
import random

async def get_danbooru_image(tags):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://danbooru.donmai.us/posts/random.json",
                params={"tags": tags}
            ) as resp:
                data = await resp.json()
                return data["file_url"]
    except:
        # Фолбэк если Danbooru недоступен
        return "https://i.imgur.com/9pNffOY.jpg"
