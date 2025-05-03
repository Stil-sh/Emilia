import os
import logging
import hashlib
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# Настройки
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7954452949:AAFPjobmKF43QWu6oFC2szX_xTvoc9uClkk"  # Замените на реальный токен!
ADMIN_CODE = "1234"   # Замените на свой код
PROXY = None              # "http://proxy.server:3128" для РФ

bot = Bot(token=BOT_TOKEN, proxy=PROXY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# База данных (вместо реальной БД для примера)
db = {
    "users": {},
    "categories": ["waifu", "neko", "maid"],
    "nsfw_tags": ["rating:explicit"]
}

# Генерация клавиатур
def user_settings_kb(user_id):
    user = db["users"].setdefault(user_id, {"buttons": True, "nsfw": False})
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            f"🔘 Кнопки: {'ВКЛ' if user['buttons'] else 'ВЫКЛ'}",
            callback_data=f"toggle_buttons_{user_id}"
        ),
        types.InlineKeyboardButton(
            f"🔞 NSFW: {'ВКЛ' if user['nsfw'] else 'ВЫКЛ'}",
            callback_data=f"toggle_nsfw_{user_id}"
        )
    )

def categories_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for cat in db["categories"]:
        kb.insert(types.InlineKeyboardButton(cat.capitalize(), callback_data=f"cat_{cat}"))
    return kb

def admin_kb():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton("➕ Добавить категорию", callback_data="add_category"),
        types.InlineKeyboardButton("➖ Удалить категорию", callback_data="del_category")
    )

# Команды
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    db["users"].setdefault(user_id, {"buttons": True, "nsfw": False})
    
    await message.answer_photo(
        photo="https://i.imgur.com/JQ1v0Yl.png",
        caption="🌸 Аниме-бот с настройками\n\n⚙️ Выберите параметры:",
        reply_markup=user_settings_kb(user_id)
    )

@dp.message_handler(commands=['admin'])
async def admin_cmd(message: types.Message):
    if message.get_args() == ADMIN_CODE:
        await message.answer("👑 Админ-панель:", reply_markup=admin_kb())
    else:
        await message.answer("🚫 Неверный код доступа!")

# Обработчики кнопок
@dp.callback_query_handler(Text(startswith="toggle_"))
async def toggle_setting(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    setting = callback.data.split("_")[1]
    db["users"][user_id][setting] = not db["users"][user_id][setting]
    await callback.message.edit_reply_markup(user_settings_kb(user_id))
    await callback.answer(f"Настройка {setting} изменена!")

@dp.callback_query_handler(Text(startswith="cat_"))
async def send_category(callback: types.CallbackQuery):
    category = callback.data.split("_")[1]
    user_nsfw = db["users"].get(callback.from_user.id, {}).get("nsfw", False)
    
    # Здесь должен быть ваш парсер (пример ниже)
    image_url = f"https://i.imgur.com/{hashlib.md5(category.encode()).hexdigest()[:6]}.jpg"
    
    user_buttons = db["users"].get(callback.from_user.id, {}).get("buttons", True)
    kb = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("❤️ В избранное", callback_data=f"fav_{hashlib.md5(image_url.encode()).hexdigest()}")
    ) if user_buttons else None
    
    await callback.message.answer_photo(
        photo=image_url,
        caption=f"Категория: {category.capitalize()}",
        reply_markup=kb
    )
    await callback.answer()

# Админ-функции
@dp.callback_query_handler(Text("add_category"))
async def add_category(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Введите название новой категории:")
    await state.set_state("wait_category")
    await callback.answer()

@dp.message_handler(state="wait_category")
async def process_category(message: types.Message, state: FSMContext):
    new_cat = message.text.strip().lower()
    if new_cat not in db["categories"]:
        db["categories"].append(new_cat)
        await message.answer(f"✅ Категория '{new_cat}' добавлена!")
    else:
        await message.answer(f"⚠️ Категория '{new_cat}' уже есть")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
