import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    CallbackQuery, message

import config
import settings

TOKEN = settings.TG_TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

Help_btn = KeyboardButton('Помощь')
Shop_btn = KeyboardButton('Магазин')
Start_btn = KeyboardButton('Начать')
main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(Help_btn, Shop_btn, Start_btn)

Click_btn = InlineKeyboardButton('Клик', callback_data="/add")
farm_kb = InlineKeyboardMarkup(resize_keyboard=True).add(Click_btn)

DoublePoint_btn = InlineKeyboardButton('+2 м/к за 50м', callback_data="2p/c")
FivePoint_btn = InlineKeyboardButton(f'+5 м/к за 1250м', callback_data="5p/c")
TenPoint_btn = InlineKeyboardButton('+10 м/к за 2500м', callback_data="10p/c")
TwentyPoint_btn = InlineKeyboardButton('+20 м/к за 4500м', callback_data="20p/c")
FiftyPoint_btn = InlineKeyboardButton('+50 м/к за 7900м', callback_data="50p/c")
OneHundredPoint_btn = InlineKeyboardButton('+100 м/к за 11300м', callback_data="100p/c")
shop_kb = InlineKeyboardMarkup(resize_keyboard=True).add(DoublePoint_btn, FivePoint_btn, TenPoint_btn, TwentyPoint_btn, FiftyPoint_btn,
                                     OneHundredPoint_btn)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text='Этот бот-игра, тут за каждый клик вам будут начисляться монеты для прокачки твоего клика.',
                           reply_markup=main_kb)


@dp.message_handler(text="Помощь")
async def send_help(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text='Для того чтобы прокачаться нажмите кнопку магазина, для того что бы задать вопрос пишите сюда: @hkkk89')


@dp.message_handler(text="Начать")
async def start_play(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'У вас: {settings.point} монет', reply_markup=farm_kb)


@dp.message_handler(text="Магазин")
async def start_play(message: types.Message):
    await bot.send_message(message.from_user.id, text='Магазин', reply_markup=shop_kb)


@dp.callback_query_handler(text=["2p/c", "5p/c", "10p/c", "20p/c", "50p/c", "100p/c", "back"])
async def add_point(callback: CallbackQuery):
    if callback.data == DoublePoint_btn.callback_data and settings.point >= 50:
        config.Boughtpoint += 2
        config.point -= 50
        await callback.message.edit_text('куплено!')
    if callback.data == FivePoint_btn.callback_data and settings.point >= 1250:
        config.Boughtpoint += 5
        config.point -= 1250
        await callback.message.edit_text('куплено!')
    if callback.data == TenPoint_btn.callback_data and settings.point >= 2500:
        config.Boughtpoint += 10
        callback.point -= 2500
        await callback.message.edit_text('куплено!')
    if callback.data == TwentyPoint_btn.callback_data and settings.point >= 4500:
        config.Boughtpoint += 20
        config.point -= 4500
        await callback.message.edit_text('куплено!')
    if callback.data == FiftyPoint_btn.callback_data and settings.point >= 7900:
        config.Boughtpoint += 50
        config.point -= 7900
        await callback.message.edit_text('куплено!')
    if callback.data == OneHundredPoint_btn.callback_data and settings.point >= 11300:
        config.Boughtpoint += 100
        config.point -= 11300
        await callback.message.edit_text('куплено!')


@dp.callback_query_handler(text="/add")
async def add_point(callback: CallbackQuery):
    config.point += config.Boughtpoint
    await callback.message.edit_text(f'У вас: {config.point} монет', reply_markup=farm_kb)


if __name__ == '__main__':
    executor.start_polling(dp)
