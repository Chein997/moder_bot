import logging
from db_main import BotDB
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

API_TOKEN = ('5851460615:AAGmNkJNZflND1t0StkEjJl6oXAJPjmDwAE')


bot = Bot(token=API_TOKEN)
db=BotDB('wordsforbot1.db')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
moder_chat_id=[-1001860696378]

class Form(StatesGroup):
    word = State()
    word1 = State()

@dp.message_handler(commands='menu')
async def menu(message):
    markup= ReplyKeyboardMarkup(resize_keyboard=True)
    add_word_markup= KeyboardButton('/add_word')
    del_word_markup=KeyboardButton('/del_word')
    all_words_markup=KeyboardButton('/all_words')
    markup.add(add_word_markup, del_word_markup, all_words_markup)
    if message.chat.id not in moder_chat_id:
        msg1=await message.answer('нет')
        await msg1.delete()
    else:
        await message.answer('menu', reply_markup=markup)

@dp.message_handler(commands='add_word')
async def add_word(message: types.Message):
    if message.chat.id not in moder_chat_id:
        msg2=await message.answer('Нет')
        await msg2.delete()
    else:
        await Form.word.set()

        await message.reply("Напиши слово которое нужно добавить")

@dp.message_handler(state=Form.word)
async def add_word1(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['word'] = message.text

    await Form.next()
    db.add_words(data['word'])
    await message.answer('Слово успешно добавлено)')
    await state.finish()

@dp.message_handler(commands='del_word')
async def del_word(message: types.Message):
    if message.chat.id not in moder_chat_id:
        msg3=await message.answer('Нет')
        await msg3.delete()
    else:
        await Form.word1.set()

        await message.reply("Напиши слово которое нужно удалить")

@dp.message_handler(state=Form.word1)
async def del_word1(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['word1'] = message.text

    await Form.next()
    db.del_words(data['word1'])
    await message.answer('Слово успешно удалено)')
    await state.finish()

@dp.message_handler(commands='all_words')
async def all_words(message:types.Message):
    if message.chat.id not in moder_chat_id:
        msg4=await message.answer('Нет')
        await msg4.delete()
    else:
        await message.answer(db.get_words())

@dp.message_handler()
async def forb_words(message:types.Message):
    mess_id = message.message_id
    mess_id1 = str(mess_id)
    chat_id=message.chat.id
    chat_id1 = str(chat_id)
    if '-100' in chat_id1:
        chat_id1=chat_id1.replace('-100', '', 1)
    link='https://t.me/c/' + chat_id1 + '/' + mess_id1
    if db.words_exists(message.text):
        await bot.send_message(-1001860696378, 'Встречено слово:' + message.text + ' ' +link)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)