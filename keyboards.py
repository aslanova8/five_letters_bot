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
button_len_3 = KeyboardButton('3')
button_len_4 = KeyboardButton('4')
button_len_5 = KeyboardButton('5')
button_len_6 = KeyboardButton('6')
button_len_7 = KeyboardButton('7')
button_len_8 = KeyboardButton('8')
button_len_9 = KeyboardButton('9')
button_len_10 = KeyboardButton('10')
button_len_11 = KeyboardButton('11')
button_len_12 = KeyboardButton('12')
button_len_13 = KeyboardButton('13')
button_len_14 = KeyboardButton('14')
button_len_15 = KeyboardButton('15')
button_len_16 = KeyboardButton('16')
button_len_17 = KeyboardButton('17')
button_len_18 = KeyboardButton('18')
button_len_19 = KeyboardButton('19')
button_len_20 = KeyboardButton('20')

len_choosing_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .row(button_len_3, button_len_4, button_len_5, button_len_6, button_len_7, button_len_8, button_len_9,
         button_len_10, button_len_11, button_len_12, button_len_13, button_len_14, button_len_15, button_len_16,
         button_len_17, button_len_18, button_len_19, button_len_20)

# Создаем кнопки для выбора длины слова
button_open_specific_letter = KeyboardButton(OPEN_SPECIFIC_LETTER_TEXT)
button_open_letter_in_certain_place = KeyboardButton(OPEN_LETTER_IN_CERTAIN_PLACE_TEXT)
button_open_vowels = KeyboardButton(OPEN_VOWELS_TEXT)

hint_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) \
    .add(button_open_specific_letter).add(button_open_letter_in_certain_place).add(button_open_vowels)
