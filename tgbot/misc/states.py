from aiogram.fsm.state import State, StatesGroup


class AdminFSM(StatesGroup):
    home = State()
    get_catalog = State()


class UserFSM(StatesGroup):
    home = State()
    name = State()
    contact = State()

    time_to_call = State()