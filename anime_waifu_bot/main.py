import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# Настройки
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7954452949:AAFPjobmKF43QWu6oFC2szX_xTvoc9uClkk"  # Замените на реальный токен!
ADMIN_CODE = "123"   # Ваш секретный код

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# База данных (в продакшене замените на PostgreSQL)
db = {
    "categories": {
        "Девушки": "rating:safe",
        "Котики": "neko",
        "Мейд": "maid",
        "NSFW": "rating:explicit"
    },
    "users": {}
}

# Клавиатура с категориями
def categories_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for name in db["categories"]:
        kb.insert(types.InlineKeyboardButton(name, callback_data=f"cat_{name}"))
    return kb

# Админ-панель
def admin_kb():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Добавить категорию", callback_data="add_category"),
        types.InlineKeyboardButton("Удалить категорию", callback_data="del_category")
    )

# Команды
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("🎌 Выберите категорию:", reply_markup=categories_kb())

@dp.message_handler(commands=['admin'])
async def admin_cmd(message: types.Message):
    if message.get_args() == ADMIN_CODE:
        await message.answer("👑 Админ-панель:", reply_markup=admin_kb())
    else:
        await message.answer("🚫 Неверный код!")

# Обработка выбора категории
@dp.callback_query_handler(Text(startswith="cat_"))
async def send_category(callback: types.CallbackQuery):
    cat_name = callback.data.split("_")[1]
    tag = db["categories"][cat_name]
    
    # Здесь должен быть ваш парсер (пример ниже)
    image_url = await get_danbooru_image(tag)
    
    await callback.message.answer_photo(
        photo=image_url,
        caption=f"Категория: {cat_name}"
    )
    await callback.answer()

# Админ: добавление категории
@dp.callback_query_handler(Text("add_category"))
async def add_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите в формате:\n<Название>;<Тег Danbooru>\nПример: Ангелы;angel")
    await state.set_state("wait_new_category")
    await callback.answer()

@dp.message_handler(state="wait_new_category")
async def process_category(message: types.Message, state: FSMContext):
    try:
        name, tag = message.text.split(";")
        db["categories"][name.strip()] = tag.strip()
        await message.answer(f"✅ Добавлено: {name} → {tag}")
        await state.finish()
    except:
        await message.answer("❌ Неверный формат! Пример: Демоны;demon")
        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
