import asyncio
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType
from keyboards import user_kb
from filters.user_filters import FSM
from utils.utils import general_info_coord, general_info_citiname


user_router = Router()


def locator(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    return lat, lon


@user_router.message(CommandStart())
async def starting(msg: Message):
    await msg.answer('Привет! Выбери действие:', reply_markup=user_kb.starting_kb())


@user_router.message(Command('help'))
async def help(msg: Message):
    await msg.answer(f'Привет! С моей помощью ты можешь узнать погоду', reply_markup=user_kb.starting_kb())


@user_router.callback_query(F.data.in_(['get_weather']), StateFilter(default_state))
async def input_city(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text('Укажите населённый пункт', reply_markup=user_kb.no_ways_kb())
    await state.set_state(FSM.entering_city_name)


@user_router.callback_query(F.data.in_(['get_locate']))
async def get_locate(cb: CallbackQuery):
    await cb.message.answer(text='Запрос доступа к геолокации...', reply_markup=user_kb.locator_kb())


@user_router.callback_query(F.data.in_(['cancel']))
async def cancel(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_text('Выберите действие:', reply_markup=user_kb.starting_kb())
    await state.clear()


@user_router.message(StateFilter(FSM.entering_city_name))
async def get_weather_from_cityname(msg: Message, state: FSMContext):
    info = await general_info_citiname(msg.text)
    if info:
        await msg.answer(text=f'Погода в {info.get('city')} \n'
                              f'Температура на улице {info.get('temp')}\n'
                              f'Ветер {info.get('wind')} м/с\n'
                              f'Давление {info.get('pressure')} мм рт. столба\n'
                              f'Влажность {info.get('humidity')}%')
        await state.clear()
        await msg.delete()
        await asyncio.sleep(0.5)
        await msg.answer(text='Продолжим?', reply_markup=user_kb.starting_kb())
    else:
        await msg.answer(text='Населённый пункт не найден, попробуйте ещё раз', reply_markup=user_kb.no_ways_kb())


@user_router.message(F.content_type == ContentType.LOCATION, StateFilter(default_state))
async def get_weather_from_locate(msg: Message, state: FSMContext):
    lat = msg.location.latitude
    lon = msg.location.longitude
    info = await general_info_coord(lat=lat, lon=lon)
    await msg.answer(text=f'Вы находитесь в {info.get('city')} \n'
                          f'Температура на улице {info.get('temp')}C°\n'
                          f'Ветер {info.get('wind')} м/с\n'
                          f'Давление {info.get('pressure')} мм рт. столба\n'
                          f'Влажность {info.get('humidity')}%', reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await asyncio.sleep(0.5)
    await msg.answer(text='Продолжим?', reply_markup=user_kb.starting_kb())
    await state.clear()


@user_router.message()
async def no_message_there(msg: Message):
    await msg.delete()