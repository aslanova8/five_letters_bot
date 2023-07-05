from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Создаем кнопки для вызова /help
button_setting_len = KeyboardButton('Изменить длину слов')
button_setting_hint = KeyboardButton('Добавить подсказки')

setting_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_setting_len) \
    .add(button_setting_hint)

# Создаем кнопки для изменения
button_len_4 = KeyboardButton('4')
button_len_5 = KeyboardButton('5')
button_len_6 = KeyboardButton('6')
button_len_7 = KeyboardButton('7')
button_len_8 = KeyboardButton('8')

len_choosing_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_len_4, button_len_5,
                                                                                        button_len_6, button_len_7,
                                                                                        button_len_8)
