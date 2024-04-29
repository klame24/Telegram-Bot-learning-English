from aiogram.types import ReplyKeyboardRemove, KeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from enum import IntEnum, auto


    
# def yes_no_kbrd():
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text="Да",
#         callback_data="yes"
#     )
#     builder.button(
#         text="Нет",
#         callback_data="no"
#     )
#     return builder.as_markup()



start_kbrd = ReplyKeyboardRemove(
    keyboard = [
        [
        KeyboardButton(text="Мой словарь 📖"),
        KeyboardButton(text="Проверка знаний 📚")
        ],
        [
            KeyboardButton(text="Слово дня 💯")
        ],
    ],
    resize_keyboard = True,
    input_field_placeholder = "Choose an action ;)"
)

my_dictionary_kbrd = ReplyKeyboardRemove(
    keyboard = [
        [
            KeyboardButton(text="Список слов"),
            KeyboardButton(text="Добавить слово")
        ],
        [
            KeyboardButton(text="Удалить слово"),
            KeyboardButton(text="Назад")
        ],
    ],
    resize_keyboard = True,
    input_field_placeholder = "Choose an action ;)"
)

yes_or_not_kbrd = ReplyKeyboardRemove(
    keyboard = [
        [
            KeyboardButton(text="Да, хочу"),
            KeyboardButton(text="Нет, не хочу")
        ],
        [
            KeyboardButton(text="Вернуться в меню словаря")
        ],
    ],
    resize_keyboard = True,
    input_field_placeholder = "Choose an action ;)"
)

numbers_kbrd = ReplyKeyboardRemove(
    keyboard = [
        [
            KeyboardButton(text="1 страница"),
            KeyboardButton(text="2 страница")
        ],
        [
            KeyboardButton(text="3 страница"),
            KeyboardButton(text="4 страница")
        ],
        [
            KeyboardButton(text="Вернуться в меню словаря")
        ]
    ],
    resize_keyboard = True,
    input_field_placeholder = "Choose an action ;)"
)

numbers_kbrd_withoutTranslate = ReplyKeyboardRemove(
    keyboard = [
        [
            KeyboardButton(text="Первая страница"),
            KeyboardButton(text="Вторая страница")
        ],
        [
            KeyboardButton(text="Третья страница"),
            KeyboardButton(text="Четвертая страница")
        ],
        [
            KeyboardButton(text="Вернуться в меню словаря")
        ]
    ],
    resize_keyboard = True,
    input_field_placeholder = "Choose an action ;)"
)

