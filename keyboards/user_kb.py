from aiogram.utils.keyboard import (InlineKeyboardButton, InlineKeyboardMarkup,
                                    ReplyKeyboardMarkup, KeyboardButton)


def locator_kb():
    button = KeyboardButton(text='Запросить геолокацию', request_location=True)
    return ReplyKeyboardMarkup(keyboard=[[button,]],
                               one_time_keyboard=False, resize_keyboard=True)



def starting_kb():
    button_get_weather = InlineKeyboardButton(text='Погода в населённом пункте',
                                              callback_data='get_weather')
    button_get_locate = InlineKeyboardButton(text='Погода здесь',
                                             callback_data='get_locate')
    return InlineKeyboardMarkup(inline_keyboard=[[button_get_weather, button_get_locate]])


def weather_kb():
    button_get_adv = InlineKeyboardButton(text='Подробнее о погоде',
                                              callback_data='get_advanced')
    button_cancel = InlineKeyboardButton(text='В главное меню',
                                         callback_data='cancel')
    return InlineKeyboardMarkup(inline_keyboard=[[button_get_adv], [button_cancel]])


def no_ways_kb():
    button_cancel = InlineKeyboardButton(text='В главное меню',
                                         callback_data='cancel')
    return InlineKeyboardMarkup(inline_keyboard=[[button_cancel]])

