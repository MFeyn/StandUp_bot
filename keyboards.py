from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def yes_no_buttons():
    yes_btn = KeyboardButton('Да')
    no_btn = KeyboardButton('Нет')
    buttons = [yes_btn, no_btn]
    return buttons


def yes_no_keyboard():
    buttons = yes_no_buttons()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def user_menu_buttons():
    buttons = []
    calculate_hours = InlineKeyboardButton(text='Рассчёт трудовых часов за последний месяц',
                                           callback_data='calc_hours')
    buttons.append(calculate_hours)
    return buttons


def user_menu_keyboard():
    buttons = user_menu_buttons()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def admin_menu_buttons():
    buttons = []
    calculate_user_hours = InlineKeyboardButton(text='Рассчёт трудовых часов сотрудника за указанный период',
                                                callback_data='adm_calc_hours')
    analyse_user_hours = InlineKeyboardButton(text='Анализ трудовых часов сотрудника за указанный период',
                                              callback_data='adm_analyse_hours')
    change_db = InlineKeyboardButton(text='Работа с Базой данных', callback_data='adm_change_db')
    output_csv_data = InlineKeyboardButton(text='Выгрузка данных из БД в формате CSV',
                                           callback_data='adm_output_csv_data')
    buttons.extend([calculate_user_hours, analyse_user_hours, change_db, output_csv_data])
    return buttons


def admin_menu_keyboard():
    buttons = admin_menu_buttons()
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def change_db_buttons():
    buttons = []
    add_new_employee = InlineKeyboardButton(text='Добавить нового сотрудника', callback_data='new_employee')
    change_user_rights = InlineKeyboardButton(text='Изменить права сотрудника', callback_data='change_rights')
    del_employee = InlineKeyboardButton(text='Удалить сотрудника из Базы данных', callback_data='del_employee')
    buttons.extend([add_new_employee, change_user_rights, del_employee])
    return buttons


def change_db_keyboard():
    buttons = change_db_buttons()
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
