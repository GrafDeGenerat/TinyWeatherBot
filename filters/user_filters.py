from aiogram.fsm.state import State, StatesGroup


class FSM(StatesGroup):
    entering_city_name = State()

