from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="7954452949:AAFPjobmKF43QWu6oFC2szX_xTvoc9uClkk")  # Обязательно замените на реальный токен!
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Бот жив! Используйте /waifu")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
