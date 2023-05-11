from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext

from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging


import keyboards
from config import API_TOKEN
from sqlighter import SQLighter
from states import Registration, NewEmployee, ChangeEmpRights, DeleteEmp

# set up logging lvl
logging.basicConfig(level=logging.INFO)

# initialize bot
bot = Bot(API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# connect to db
db = SQLighter('database/stand_db.db')


async def count_hours(user_id):
    try:
        pass
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call_back: call_back.data == 'adm_change_db')
async def choose_option(call_back):
    await bot.answer_callback_query(call_back.id, '')
    keyboard = keyboards.change_db_keyboard()
    await bot.send_message(call_back.message.chat.id, 'Выберите опцию.', reply_markup=keyboard)


@dp.callback_query_handler(lambda call_back: call_back.data == 'new_employee')
async def add_employee(call_back):
    await bot.answer_callback_query(call_back.id)
    await bot.send_message(call_back.message.chat.id, 'Введите ник нового сотрудника.')
    await NewEmployee.waiting_for_nickname.set()


@dp.callback_query_handler(lambda call_back: call_back.data == 'change_rights')
async def change_emp_rights(call_back):
    await bot.answer_callback_query(call_back.id)
    await bot.send_message(call_back.message.chat.id, 'Введите ник сотрудника.')
    await ChangeEmpRights.waiting_for_nickname.set()


@dp.callback_query_handler(lambda call_back: call_back.data == 'del_employee')
async def delete_emp(call_back):
    await bot.answer_callback_query(call_back.id)
    await bot.send_message(call_back.message.chat.id, 'Введите ник сотрудника, '
                                                      'которого хотите удалить из базы данных')
    await DeleteEmp.waiting_for_nickname.set()


@dp.message_handler(state=DeleteEmp.waiting_for_nickname)
async def delete_emp_nickname(message: types.Message, state: FSMContext):
    is_exist = bool(len(db.get_employee(message.text)))
    if not is_exist:
        await bot.send_message(message.chat.id, 'Сотрудника с таким ником не существует! '
                                                'Проверьте данные и повторите ввод.')
        return
    await state.update_data(nickname=message.text)
    await DeleteEmp.next()
    keyboard = keyboards.yes_no_keyboard()
    await bot.send_message(message.chat.id, 'Подтвердить удаление сотрудника из базы данных?', reply_markup=keyboard)


@dp.message_handler(state=DeleteEmp.waiting_for_confirmation)
async def delete_emp_confirm(message: types.Message, state: FSMContext):
    if message.text not in ['Да', 'Нет']:
        await bot.send_message(message.chat.id, 'При ответе используйте, пожалуйста, клавиатуру')
        return
    user_data = await state.get_data()
    nickname = user_data['nickname']
    if message.text == 'Да':
        db.del_emp(nickname)
        await bot.send_message(message.chat.id, 'Сотрудник был успешно удален!')
    else:
        await bot.send_message(message.chat.id, 'Вы отменили удаление сотрудника.')


@dp.message_handler(state=ChangeEmpRights.waiting_for_nickname)
async def change_rights_emp_nickname(message: types.Message, state: FSMContext):
    is_exist = bool(len(db.get_employee(message.text)))
    if not is_exist:
        await bot.send_message(message.chat.id, 'Сотрудника с таким ником не существует! '
                                                'Проверьте данные и повторите ввод.')
        return
    await state.update_data(nickname=message.text)
    await ChangeEmpRights.next()
    keyboard = keyboards.yes_no_keyboard()
    await bot.send_message(message.chat.id, 'Предоставить сотруднику права администратора?', reply_markup=keyboard)


@dp.message_handler(state=ChangeEmpRights.waiting_for_right_lvl)
async def change_rights_emp_right(message: types.Message, state: FSMContext):
    if message.text not in ['Да', 'Нет']:
        await bot.send_message(message.chat.id, 'При ответе используйте, пожалуйста, клавиатуру')
        return
    user_data = await state.get_data()
    nickname = user_data['nickname']
    if message.text == 'Да':
        is_admin = 1
    else:
        is_admin = 0
    db.change_emp_rights(nickname, is_admin)

    await bot.send_message(message.chat.id, 'Права сотрудника были успешно изменены!')


@dp.message_handler(state=NewEmployee.waiting_for_nickname)
async def new_employee_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await NewEmployee.next()
    keyboard = keyboards.yes_no_keyboard()
    await bot.send_message(message.chat.id, 'Предоставить сотруднику права администратора?', reply_markup=keyboard)


@dp.message_handler(state=NewEmployee.waiting_for_adm_rights)
async def new_employee_rights(message: types.Message, state: FSMContext):
    if message.text not in ['Да', 'Нет']:
        await bot.send_message(message.chat.id, 'При ответе используйте, пожалуйста, клавиатуру')
        return
    user_data = await state.get_data()
    nickname = user_data['nickname']
    if message.text == 'Да':
        is_admin = 1
    else:
        is_admin = 0
    emp_password = db.add_employee(nickname, is_admin)
    keyboard = keyboards.yes_no_keyboard()
    await NewEmployee.next()
    await bot.send_message(message.chat.id,
                           f'Никнейм сотрудника: <b>{nickname}</b>\n'
                           f'Пароль сотрудника: <b>{emp_password}</b>\n'
                           f'Подтвердить добавление нового сотрудника?', reply_markup=keyboard, parse_mode='HTML')


@dp.message_handler(state=NewEmployee.waiting_for_confirmation)
async def new_employee_confirm(message: types.Message, state: FSMContext):
    if message.text not in ['Да', 'Нет']:
        await bot.send_message(message.chat.id, 'Пожалуйста, при ответе используйте клавиатуру')
        return
    if message.text == 'Да':
        await bot.send_message(message.chat.id, 'Сотрудник успешно добавлен в базу данных!')

        await state.finish()
        await start_message(message)
    else:
        await bot.send_message(message.chat.id, 'Все изменения были отменены.')

        await state.finish()


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    pass


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if db.is_registered(message.chat.id):
        if db.is_admin(message.chat.id):
            keyboard = keyboards.admin_menu_keyboard()
        else:
            keyboard = keyboards.user_menu_keyboard()
        await bot.send_message(message.chat.id, 'Список команд.', reply_markup=keyboard)
    else:
        await bot.send_message(message.chat.id, 'Вы не зарегистрированы. '
                                                'Для регистрации используйте команду /register')


@dp.message_handler(commands=['register'])
async def registration(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите логин, предоставленный администратором.')
    await Registration.waiting_for_login.set()


@dp.message_handler(state=Registration.waiting_for_login)
async def registration_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    is_correct = bool(len(db.get_employee(message.text)))
    if not is_correct:
        await message.answer('Неверный логин! Повторите ввод.')
        return
    await Registration.next()
    await message.answer('Введите пароль.')


@dp.message_handler(state=Registration.waiting_for_password)
async def registration_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data['login']
    password = message.text

    if db.register_employee(message.chat.id, login, password):
        await message.answer('Регистрация прошла успешно! Для просмотра списка команд напишите /help')
        await state.finish()
    else:
        await message.answer('Неверный пароль! Повторите ввод.')
        return


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

