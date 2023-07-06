from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from text_templates import *

# Создаем кнопки для вызова /help
button_setting_len = KeyboardButton(CHANGE_LEN_TEXT)
button_setting_hint = KeyboardButton(ADD_HINTS_TEXT)

setting_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_setting_len) \
    .add(button_setting_hint)

# Создаем кнопки для выбора длины слова
button_len_4 = KeyboardButton('4')
button_len_5 = KeyboardButton('5')
button_len_6 = KeyboardButton('6')
button_len_7 = KeyboardButton('7')
button_len_8 = KeyboardButton('8')

len_choosing_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row(button_len_4, button_len_5, button_len_6, button_len_7, button_len_8)

# Создаем кнопки для выбора длины слова
button_open_specific_letter = KeyboardButton(OPEN_SPECIFIC_LETTER_TEXT)
button_open_letter_in_certain_place = KeyboardButton(OPEN_LETTER_IN_CERTAIN_PLACE_TEXT)
button_open_vowels = KeyboardButton(OPEN_VOWELS_TEXT)

hint_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add(button_open_specific_letter).add(button_open_letter_in_certain_place).add(button_open_vowels)
