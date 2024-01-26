import handlers.keyboards as kb
import database as db
from handlers.tables import tables
from aiogram.filters import CommandStart
from aiogram import Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import BotAction


router = Router()
database: db.PostgresDB = db.PostgresDB()
dbase = db.PostgresDB()
count = 0

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # Нужен для сбора данных, определяет собираем ли ключи
    await state.set_state(BotAction.table)
    await message.answer("Выберете с какой таблицей вы хотите работать...",
                         reply_markup=kb.MainKeyboard)



# Выбор с какой бд работать
@router.message(BotAction.table)
async def table_state(message: Message, state: FSMContext):
    await state.set_state(BotAction.action)
    await message.answer(f'Какое действие выполнить с таблицей "{message.text}"',
                         reply_markup=kb.MenuKeyboard)
    if message.text == 'Владелец':
        await state.update_data(table='owners',
                                ru_table='Владелец')
    elif message.text == 'Автор':
        await state.update_data(table='author',
                                ru_table='Автор')
    elif message.text == 'Типография':
        await state.update_data(table='printery',
                                ru_table='Типография')
    elif message.text == 'Издательство':
        await state.update_data(table='publishing_office',
                                ru_table='Издательство')
    elif message.text == 'Книга':
        await state.update_data(table='book',
                                ru_table='Книга')
    elif message.text == 'Печать':
        await state.update_data(table='printing',
                                ru_table='Печать')
    elif message.text == 'Произведения':
        await state.update_data(table='work',
                                ru_table='Произведения')


@router.message(BotAction.action)
async def action_state(message: Message, state: FSMContext):
    current_table = await state.get_data()
    current_table = current_table.get('table')

    columns = tables.get_db_columns(current_table)
    ru_columns = tables.get_ru_columns(current_table)
    global count

    if message.text == 'Назад':
        await message.answer("Выберете с какой таблицей вы хотите работать...", reply_markup=kb.MainKeyboard)
        await state.set_state(BotAction.table)

    elif message.text == 'Вставить':
        await state.update_data(action='insert')
        # Пропускаем id, так как они автогенерируемы
        if '!id_' in columns[0]:
            count = 1

        await message.answer(f'Введите {ru_columns[count]}',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(BotAction.dataCollect)

    elif message.text == 'Изменить':
        await message.answer(f'Введите {ru_columns[count]}',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(action='update')
        await state.set_state(BotAction.dataCollect)

    elif message.text == 'Удалить':
        await message.answer(f'Введите {ru_columns[count]}',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(action='delete')
        # В моем случае у меня всегда один ключ, поэтому делаем так, чтобы мы собрали данные один раз
        count = tables.get_size(current_table) - 1
        await state.set_state(BotAction.dataCollect)

    elif message.text == 'Показать':
        answer, Table = dbase.ShowTable(current_table)
        await message.answer(answer)

        if not Table == '':
            text = await prepareTable(Table, current_table)
            for el in text:
                await message.answer(f'{el}')


# Эдакий оператор for, но для сбора данных у пользователя, разбиения на случаи, а также выполнения запросов к бд

# Эдакий оператор for, но для сбора данных у пользователя, разбиения на случаи, а также выполнения запросов к бд
@router.message(BotAction.dataCollect)
async def data_collect(message: Message, state: FSMContext):
    global count
    # Получение метаданных
    current_table = await state.get_data()
    ru_table = current_table.get('ru_table')    # Нужно, чтобы делать красивое обращение к пользователю
    action = current_table.get('action')        # Действие с таблицей
    current_table = current_table.get('table')  # Название таблицы, с которой в данный момент работаем

    column = tables.get_db_columns(current_table)
    ru_column = tables.get_ru_columns(current_table)

    if action == 'update':
        tables.add_transfer_columns(current_table, column[count])
    elif action == 'delete':
        tables.add_transfer_columns(current_table, column[0].replace('!', ''))
    else:
        tables.add_transfer_columns(current_table, column[count].replace('!', ''))

    if count >= tables.get_size(current_table) - 1:
        # Этот блок отвечает за окончание сбора данных от пользователя,
        # а также выполнения одного из трех случая изменения данных в бд

        tables.add_transfer_data(current_table, message.text)

        if action == 'insert':
            await message.answer(
                dbase.InsertData(current_table,
                                 tables.get_transfer_columns(current_table),
                                 tables.get_transfer_data(current_table))
            )

        elif action == 'delete':
            await message.answer(
                dbase.DeleteData(current_table,
                                 tables.get_transfer_columns(current_table),
                                 tables.get_transfer_data(current_table))
            )

        elif action == 'update':
            await message.answer(
                dbase.UpdateData(current_table,
                                 tables.get_transfer_columns(current_table),
                                 tables.get_transfer_data(current_table))
            )

        count = 0
        tables.clear_transfer_columns(current_table)
        tables.clear_transfer_data(current_table)

        await message.answer(f'Какое действие выполнить с таблицей "{ru_table}"',
                             reply_markup=kb.MenuKeyboard)

        await state.set_state(BotAction.action)

    else:
        # Блок сбора данных от пользователя, выполняется пока
        # счетчик не станет равным количеству полей в таблице

        await message.answer(f'Введите {ru_column[count + 1]}')

        tables.add_transfer_data(current_table, message.text)
        count += 1


# Подготовка сообщений для отправки пользователю по кнопке Показать
async def prepareTable(Table, current_table):
    ru_column = tables.get_ru_columns(current_table)
    text = []
    buf = ''
    for row in Table:
        for i in range(len(row)):
            column = ru_column[i].replace('у', 'а').capitalize()
            buf += f'{column}: {row[i]}\n'
        text.append(buf)
        buf = ''
    print(text)
    return text


