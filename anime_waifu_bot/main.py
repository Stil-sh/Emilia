import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from parser import get_danbooru_image
from database import Database

# Настройки
logging.basicConfig(level=logging.INFO)
bot = Bot(token="7954452949:AAFPjobmKF43QWu6oFC2szX_xTvoc9uClkk")  # ← Замените на реальный токен!
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

# Клавиатура категорий
def get_categories_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    categories = db.get_categories()
    for cat_id, cat_name in categories.items():
        kb.insert(types.InlineKeyboardButton(
            cat_name, 
            callback_data=f"cat_{cat_id}"
        ))
    return kb

# Команда /start
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(
        "🎌 Выберите категорию:",
        reply_markup=get_categories_kb()
    )

# Обработка нажатия кнопки
@dp.callback_query_handler(Text(startswith="cat_"))
async def process_category(callback: types.CallbackQuery):
    cat_id = callback.data.split("_")[1]
    category = db.get_category(cat_id)
    
    if not category:
        await callback.answer("Категория не найдена")
        return
    
    try:
        image_url = await get_danbooru_image(category['tag'])
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=image_url,
            caption=f"Категория: {category['name']}"
        )
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await callback.answer("Не удалось загрузить изображение")
    finally:
        await callback.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
