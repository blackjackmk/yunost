import conf
from conf import TOKEN, admin_id
from aiogram import Bot, executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

store=MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=store)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    conf.add_user(user_id)
    #get last post
    with open("last_post.txt", "r", encoding="utf-8") as last:
        full_post = last.read()
    last.close()
    dane = full_post.split("&")
    #button initialization
    blank_btn = InlineKeyboardButton('Заполнить анкету', url='https://docs.google.com/forms/d/e/1FAIpQLScpNhb_zeb7tDLB8dp1xc43wqogzwVL6MmthhubLRt_D9UtEA/viewform?usp=sf_link')
    inst_btn = InlineKeyboardButton('Сделать репост', url=dane[2])
    button_block = InlineKeyboardMarkup(row_width=1).add(blank_btn, inst_btn)
    await bot.send_photo(message.chat.id, photo=dane[0])
    await message.answer(dane[1], reply_markup=button_block)

@dp.message_handler(commands=['get_id'])
async def process_get_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(user_id)

@dp.message_handler(commands=['drop'])
async def process_get_id(message: types.Message):
    if message.chat.id == 461964422:
        exit()



if __name__ == '__main__':
    from admin import dp
    executor.start_polling(dp, skip_updates=False)