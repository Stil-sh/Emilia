import aiohttp
import random

class NekoParser:
    def __init__(self):
        self.sources = [
            self._get_neko_from_danbooru,
            self._get_neko_fallback
        ]

    async def get_neko_image(self) -> str:
        """Получает случайное изображение неко-девочки"""
        for source in self.sources:
            try:
                url = await source()
                if url: return url
            except:
                continue
        return "https://i.imgur.com/neko_fallback.jpg"

    async def _get_neko_from_danbooru(self) -> str:
        """Пытается получить с Danbooru"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://danbooru.donmai.us/posts/random.json",
                params={"tags": "neko rating:safe"},
                timeout=5
            ) as resp:
                data = await resp.json()
                return f"https://danbooru.donmai.us{data['file_url']}"

    async def _get_neko_fallback(self) -> str:
        """Фолбэк-источники"""
        neko_images = [
            "https://i.imgur.com/neko1.jpg",
            "https://i.imgur.com/neko2.jpg",
            "https://i.imgur.com/neko3.jpg"
        ]
        return random.choice(neko_images)

# Глобальный экземпляр
neko_parser = NekoParser()
