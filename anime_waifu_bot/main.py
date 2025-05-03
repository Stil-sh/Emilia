from aiogram import Bot, Dispatcher, executor, types
from parser import get_random_danbooru_image
import logging

# Настройки
logging.basicConfig(level=logging.INFO)
bot = Bot(token="ВАШ_ТОКЕН")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Отправь /waifu для случайной аниме-картинки")

@dp.message_handler(commands=['waifu'])
async def waifu(message: types.Message):
    try:
        img_url = await get_random_danbooru_image()
        
        await message.answer_photo(
            photo=img_url,
            caption="Случайная вайфу с Danbooru",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    "❤️ В избранное",
                    callback_data=f"fav_{img_url.split('/')[-1]}"  # Сохраняем только имя файла
                )
            )
        )
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply("Не удалось загрузить изображение 😢")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
