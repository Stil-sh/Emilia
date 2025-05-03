from aiogram import Bot, Dispatcher, executor, types
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
bot = Bot(token="7954452949:AAFPjobmKF43QWu6oFC2szX_xTvoc9uClkk")  # ← Замените на реальный токен!
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Бот жив! Используйте /waifu")

@dp.message_handler(commands=['waifu'])
async def waifu(message: types.Message):
    try:
        # Тестовое изображение (замените на свой источник)
        photo_url = "https://i.imgur.com/9pNffOY.jpg"  # Пример работающего URL
        
        await message.answer_photo(
            photo=photo_url,
            caption="Вот ваша вайфу!",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(
                    "❤️ В избранное", 
                    callback_data="add_fav"
                )
            )
        )
    except Exception as e:
        logging.error(f"Ошибка в /waifu: {e}")
        await message.reply("Не удалось загрузить изображение 😢")

@dp.callback_query_handler(text="add_fav")
async def add_fav(callback: types.CallbackQuery):
    await callback.answer("Добавлено в избранное!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
