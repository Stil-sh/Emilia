import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN, PROXY_URL
from parser import get_random_waifu, search_waifu
from database import Database

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL if PROXY_URL else None)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database("waifu_db.sqlite")

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        "Привет! Я бот с аниме-девочками 🎀\n"
        "Доступные команды:\n"
        "/waifu – случайная девочка\n"
        "/search [тег] – поиск по тегу\n"
        "/fav – добавить в избранное\n"
        "/myfav – мои сохранённые\n"
        "/nsfw [on/off] – режим 18+"
    )

# Случайная вайфу (/waifu)
@dp.message_handler(commands=['waifu'])
async def random_waifu(message: types.Message):
    try:
        img_url = await get_random_waifu()
        await message.reply_photo(img_url, reply_markup=get_fav_keyboard(img_url))
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

# Поиск по тегу (/search cat_girl)
@dp.message_handler(commands=['search'])
async def search_by_tag(message: types.Message):
    tag = message.get_args()
    if not tag:
        await message.reply("Укажи тег, например: /search cat_girl")
        return
    try:
        img_url = await search_waifu(tag)
        await message.reply_photo(img_url, reply_markup=get_fav_keyboard(img_url))
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

# Кнопка "Добавить в избранное"
def get_fav_keyboard(img_url: str):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("❤️ Добавить в избранное", callback_data=f"fav_{img_url}")
    )

# Обработка избранного
@dp.callback_query_handler(Text(startswith="fav_"))
async def add_to_fav(callback: types.CallbackQuery):
    img_url = callback.data.split("_")[1]
    user_id = callback.from_user.id
    db.add_to_favorites(user_id, img_url)
    await callback.answer("Сохранено в избранное!")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
