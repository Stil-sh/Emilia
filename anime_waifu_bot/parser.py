import aiohttp
import random

async def get_random_danbooru_image():
    async with aiohttp.ClientSession() as session:
        try:
            # Получаем случайный пост с рейтингом Safe
            async with session.get(
                "https://danbooru.donmai.us/posts/random.json?tags=rating:safe"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["file_url"]
                return "https://i.imgur.com/9pNffOY.jpg"  # Фолбэк-изображение
        except Exception:
            return "https://i.imgur.com/9pNffOY.jpg"  # Фолбэк при ошибке
