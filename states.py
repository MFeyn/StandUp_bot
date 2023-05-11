from aiogram.dispatcher.filters.state import State, StatesGroup


# registration states
class Registration(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()


class NewEmployee(StatesGroup):
    waiting_for_nickname = State()
    waiting_for_adm_rights = State()
    waiting_for_confirmation = State()


class ChangeEmpRights(StatesGroup):
    waiting_for_nickname = State()
    waiting_for_right_lvl = State()


class DeleteEmp(StatesGroup):
    waiting_for_nickname = State()
    waiting_for_confirmation = State()
