from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from urllib.parse import quote, unquote
import logging

# Настройки
logging.basicConfig(level=logging.INFO)
bot = Bot(token="ВАШ_ТОКЕН")  # Замените на реальный токен!
dp = Dispatcher(bot, storage=MemoryStorage())

# Клавиатура с кнопкой "В избранное"
def get_fav_keyboard(image_url: str):
    # Кодируем URL для безопасности
    safe_url = quote(image_url)
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            "❤️ В избранное",
            callback_data=f"fav_{safe_url}"  # Формат: fav_ЗАКОДИРОВАННЫЙ_URL
        )
    )

# Команда /waifu
@dp.message_handler(commands=['waifu'])
async def send_waifu(message: types.Message):
    try:
        # Получаем случайное изображение (замените на ваш парсер)
        img_url = "https://example.com/waifu.jpg"  # Это пример, используйте реальный URL
        
        # Отправляем фото с кнопкой
        await message.answer_photo(
            photo=img_url,
            reply_markup=get_fav_keyboard(img_url)
        )
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

# Обработчик кнопки
@dp.callback_query_handler(Text(startswith="fav_"))
async def add_to_favorites(callback: types.CallbackQuery):
    try:
        # Декодируем URL
        encoded_url = callback.data.split("_", 1)[1]
        original_url = unquote(encoded_url)
        
        # Здесь сохраняем в БД (реализуйте свою логику)
        # db.add_to_favorites(callback.from_user.id, original_url)
        
        await callback.answer("✅ Добавлено в избранное!")
    except Exception as e:
        await callback.answer("❌ Ошибка сохранения")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
