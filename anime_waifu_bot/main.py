import logging
from aiogram import Bot, Dispatcher, executor, types
from scrolller_parser import ScrolllerParser

# Конфигурация
logging.basicConfig(level=logging.INFO)
TOKEN = "7954452949:AAFPjobmKF43QWu6oFC2szX_xTvoc9uClkk"
PROXY = "http://104.19.217.219:80"

# Инициализация
bot = Bot(token=TOKEN, proxy=PROXY)
dp = Dispatcher(bot)
parser = ScrolllerParser(proxy=PROXY)

# Клавиатура
start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(types.KeyboardButton("Аниме девочки"))
start_kb.add(types.KeyboardButton("Неко"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Выберите категорию:", reply_markup=start_kb)

@dp.message_handler(text=["Аниме девочки", "Неко"])
async def send_content(message: types.Message):
    try:
        subreddit = "awwnime" if message.text == "Аниме девочки" else "neko"
        posts = await parser.get_posts(subreddit, limit=3)
        
        for post in posts:
            if post['type'] == 'image':
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=post['url']
                )
            elif post['type'] == 'gif':
                await bot.send_animation(
                    chat_id=message.chat.id,
                    animation=post['url']
                )
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Ошибка загрузки, попробуйте позже")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
