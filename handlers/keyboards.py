from aiogram import Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

#Создание главных конпок для навигации

kbMain = [
        [KeyboardButton(text="Владелец")],
        [KeyboardButton(text="Автор")],
        [KeyboardButton(text="Типография")],
        [KeyboardButton(text="Издательство")],
        [KeyboardButton(text="Книга")],
        [KeyboardButton(text="Печать")],
        [KeyboardButton(text="Произведения")]
    ]
MainKeyboard = ReplyKeyboardMarkup(keyboard=kbMain,
                                   resize_keyboard=True)


kbMenu = [
        [KeyboardButton(text="Вставить")],
        [KeyboardButton(text="Изменить")],
        [KeyboardButton(text="Удалить")],
        [KeyboardButton(text="Показать")],
        [KeyboardButton(text="Назад")]
    ]
MenuKeyboard = ReplyKeyboardMarkup(keyboard=kbMenu,
                                   resize_keyboard=True
                                   )

