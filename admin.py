from aiogram.dispatcher.filters import Command, Text, ContentTypeFilter
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from main import dp, bot
import conf
from conf import admin_id, acc, bot_token
from insta import send_insta

class FSMAdmin(StatesGroup):
    admin_mode = State()
    tg_post = State()
    tg_photo = State()
    tg_spam_text = State()
    afisha_url = State()
    post_telegram = State()
    insta_photo = State()
    insta_spam_text = State()
    post_insta = State()

@dp.message_handler(commands=['admin'], state=None)
async def show_admin_panel(message: types.Message):
    if message.chat.id in admin_id: #give acces to functional button
        make_post_tg = InlineKeyboardButton(text="Пост tg", callback_data="create_post_tg")
        make_post_insta = InlineKeyboardButton(text="Пост Inst", callback_data="create_post_insta")
        kb_inline = InlineKeyboardMarkup().add(make_post_tg, make_post_insta)
        conf.add_user(message.chat.id)
        await FSMAdmin.admin_mode.set()
        await message.answer("\t\t~Админка~", reply_markup=kb_inline)
    else:
        await message.answer("Access denied")

#---------Telegram post part---------------
@dp.callback_query_handler(text=["create_post_tg"], state=FSMAdmin.admin_mode)
async def make_tg_post(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await FSMAdmin.tg_photo.set()
    await callback.message.answer("Кинь картинку для telegram")

@dp.message_handler(content_types=['photo'], state=FSMAdmin.tg_photo)
async def save_photo(message: types.Message, state: FSMContext):
    global foto_id
    foto_id = message.photo[-1].file_id
    await FSMAdmin.tg_spam_text.set()
    await message.answer("Готово. Тепер текст для поста")

@dp.message_handler(state=FSMAdmin.tg_spam_text)
async def gettext(message: types.Message, state: FSMContext):
    global spam_text
    spam_text = message.text
    await FSMAdmin.afisha_url.set()
    await message.answer("Готово. Тепер силку на інсту (друга кнопка в пості)") 

@dp.message_handler(state=FSMAdmin.afisha_url)
async def getafisha(message: types.Message, state: FSMContext):
    global afisha_url
    afisha_url = message.text
    #show example
    await message.answer("~Here is an example~")
    #button initialization
    blank_btn = InlineKeyboardButton('Заполнить анкету', url='https://docs.google.com/forms/d/e/1FAIpQLScpNhb_zeb7tDLB8dp1xc43wqogzwVL6MmthhubLRt_D9UtEA/viewform?usp=sf_link')
    inst_btn = InlineKeyboardButton('Сделать репост', url=afisha_url)
    try:
        button_block = InlineKeyboardMarkup(row_width=1).add(blank_btn, inst_btn)
        await bot.send_photo(message.chat.id, photo = foto_id)
        await bot.send_message(message.chat.id, text = spam_text, reply_markup=button_block)
        await FSMAdmin.post_telegram.set()
        post_btn = InlineKeyboardButton(text="Post", callback_data="post")
        cancel_btn = InlineKeyboardButton(text="Cancel", callback_data="cancel")
        kb_inline = InlineKeyboardMarkup().add(post_btn,cancel_btn)
        await message.answer("Щоб запустити розсилку в telegram нажми кнопку Post", reply_markup=kb_inline)
    except:
        await message.answer("Error: Потрібна силка. Давай по новой /admin")
        await state.finish()

@dp.callback_query_handler(text =["post", "cancel"], state=FSMAdmin.post_telegram)
async def send_spam(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "post":
        #button initialization
        blank_btn = InlineKeyboardButton('Заполнить анкету', url='https://docs.google.com/forms/d/e/1FAIpQLScpNhb_zeb7tDLB8dp1xc43wqogzwVL6MmthhubLRt_D9UtEA/viewform?usp=sf_link')
        inst_btn = InlineKeyboardButton('Сделать репост', url=afisha_url)
        button_block = InlineKeyboardMarkup(row_width=1).add(blank_btn, inst_btn)
        for id in acc:
            await bot.send_photo(id, photo = foto_id)
            await bot.send_message(id, text = spam_text, reply_markup=button_block)
        await callback.message.delete()
        with open("last_post.txt", "w", encoding="utf-8") as last_post:
            last_post.write(foto_id+"&")
            last_post.write(spam_text+"&")
            last_post.write(afisha_url)
        last_post.close()
        await callback.message.answer("Posting finished. To start again type /admin")
    elif callback.data == "cancel":
        await callback.message.answer("Posting canceled. To start again type /admin")
        await callback.message.delete()
    await state.finish()


#---------Instagram post part---------------
@dp.callback_query_handler(text=["create_post_insta"], state=FSMAdmin.admin_mode)
async def make_insta_post(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await FSMAdmin.insta_photo.set()
    await callback.message.answer("Кинь картинку для instagram")

@dp.message_handler(content_types=['photo'], state=FSMAdmin.insta_photo)
async def save_photo(message: types.Message, state: FSMContext):
    global foto_url, foto_id
    foto_id = message.photo[-1].file_id
    file = await bot.get_file(foto_id)
    foto_path = file.file_path
    foto_url = "https://api.telegram.org/file/bot"+bot_token+"/"+foto_path
    await FSMAdmin.insta_spam_text.set()
    await message.answer("Готово. Тепер текст для direct")

@dp.message_handler(state=FSMAdmin.insta_spam_text)
async def save_photo(message: types.Message, state: FSMContext):
    global spam_text
    spam_text = message.text
    post_btn = InlineKeyboardButton(text="Post", callback_data="post")
    cancel_btn = InlineKeyboardButton(text="Cancel", callback_data="cancel")
    kb_inline = InlineKeyboardMarkup().add(post_btn,cancel_btn)
    #show example
    await message.answer("~Here is an example~")
    await bot.send_photo(message.chat.id, photo = foto_id)
    await bot.send_message(message.chat.id, text = spam_text)
    await FSMAdmin.post_insta.set()
    await message.answer("Щоб запустити розсилку в Instagram нажми кнопку Post", reply_markup=kb_inline)
    
@dp.callback_query_handler(text =["post", "cancel"], state=FSMAdmin.post_insta)
async def send_spam(callback: types.CallbackQuery, state: FSMContext):
    global foto_url
    if callback.data == "post":
        await callback.message.answer("~It take some time. Please wait for message about success or error~")
        if send_insta(foto_url, spam_text):
            await callback.message.answer("~Done~")
        else:
            await callback.message.answer("~Something went wrong!~\nTo start again type /admin")
    elif callback.data == "cancel":
        await callback.message.answer("Posting canceled. To start again type /admin")
    await callback.message.delete()
    await state.finish()