import aiohttp

async def get_danbooru_image(tags):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://danbooru.donmai.us/posts/random.json",
                params={"tags": f"{tags} rating:safe"}
            ) as resp:
                data = await resp.json()
                return data.get("file_url", "https://i.imgur.com/example.jpg")
    except Exception:
        return "https://i.imgur.com/example.jpg"  # Фолбэк изображение
