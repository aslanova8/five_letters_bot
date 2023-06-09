import random
import sqlite3
import string

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

import keyboards as kb
from text_templates import *


def db_add_user(user_id: int, user_name: str, user_surname: str, username: str, length_of_words: int = 5,
                total_attempts: int = 5):
    guessing = False
    played_games = 0
    using_hints = False
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE user_id={user_id}")
    user_exists = cursor.fetchall()[0][0]
    if not user_exists:
        cursor.execute("INSERT INTO users (user_id, user_name, user_surname, username, length_of_words, total_attempts,"
                       "remaining_attempts, guessing, played_games, wins, using_hints, hints_left) VALUES (?, ?, ?, "
                       "?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                       (user_id, user_name, user_surname, username, length_of_words, total_attempts,
                        guessing, played_games, played_games, guessing, using_hints, 0))
        conn.commit()


def db_get_length_of_words(user_id: int) -> int:
    cursor.execute("SELECT length_of_words FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_hints_left(user_id: int) -> int:
    cursor.execute("SELECT hints_left FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_total_attempts(user_id: int) -> int:
    cursor.execute("SELECT total_attempts FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_remaining_attempts(user_id: int) -> int:
    cursor.execute("SELECT remaining_attempts FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_played_games(user_id: int) -> int:
    cursor.execute("SELECT played_games FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_wins(user_id: int) -> int:
    cursor.execute("SELECT wins FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_guessing(user_id: int) -> int:
    cursor.execute("SELECT guessing FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_len(user_id: int) -> int:
    cursor.execute("SELECT length_of_words FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_get_word(user_id: int) -> str:
    cursor.execute("SELECT word FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_set_remaining_attempts(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET remaining_attempts=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_guessing(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET guessing=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_wins(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET wins=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_played_games(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET played_games=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_word(user_id: int, value: str) -> None:
    cursor.execute("UPDATE users SET word=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_change_len(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET length_of_words=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_change_attempts(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET total_attempts=? WHERE user_id=?", (value, user_id))
    conn.commit()
    cursor.execute("UPDATE users SET remaining_attempts=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_hints(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET using_hints=? WHERE user_id=?", (value, user_id))
    conn.commit()
    cursor.execute("UPDATE users SET hints_left=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_hints_left(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET hints_left=? WHERE user_id=?", (value, user_id))
    conn.commit()


# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

# Подключение к бд
conn = sqlite3.connect('database/game_db.db', check_same_thread=False)
cursor = conn.cursor()

# Слова
words = [tuple() for _ in range(9)]
for length in range(4, 9):
    with open(f'words/words_len_{length}.txt', 'r', encoding='utf-8') as f:
        words[length] = words[length] + tuple(line.strip() for line in f.readlines())


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    db_add_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    await message.answer(HELLO_TEXT % us_name)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message_handler(commands=['help'])
async def process_help_command(message: Message):
    await message.reply(RULES_TEXT % (db_get_length_of_words(message.from_user.id),
                                      db_get_total_attempts(message.from_user.id)), reply_markup=kb.setting_kb)


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message_handler(commands=['stat'])
async def process_stat_command(message: Message):
    await message.answer(
        STATISTICS_TEXT % (db_get_played_games(message.from_user.id), db_get_wins(message.from_user.id)))


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message_handler(commands=['cancel'])
async def process_cancel_command(message: Message):
    if db_get_guessing(message.from_user.id):
        db_set_guessing(message.from_user.id, False)

        await message.answer(EXIT_TEXT)

    else:
        await message.answer(OFFER_GAME_TEXT)


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.strip().upper()
                    .translate(str.maketrans('', '', string.punctuation)) in AGREEMENT_WORDS)
async def process_positive_answer(message: Message):
    db_set_guessing(message.from_user.id, True)
    db_set_word(message.from_user.id, random.choice(words[db_get_len(message.from_user.id)]))
    db_set_remaining_attempts(message.from_user.id, db_get_total_attempts(message.from_user.id))
    db_set_hints_left(message.from_user.id, 1)
    await message.answer(LETS_GUESS_TEXT)


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.upper() in EXIT_WORDS)
async def process_negative_answer(message: Message):
    if db_get_guessing(message.from_user.id):
        db_set_played_games(message.from_user.id, db_get_played_games(message.from_user.id) + 1)
        db_set_guessing(message.from_user.id, False)
        await message.answer(OPEN_MISTERY_TEXT % db_get_word(message.from_user.id))

    else:
        await message.answer(EXIT_TEXT)


# Этот хендлер будет срабатывать на нажатие кнопки "Изменить длину слов"
@dp.message_handler(lambda message: message.text == CHANGE_LEN_TEXT)
async def process_choose_len(message: Message):
    await message.reply(CHOOSE_LEN_TEXT, reply_markup=kb.len_choosing_kb)


# Этот хендлер будет срабатывать на нажатие кнопки "Добавить подсказки"
@dp.message_handler(lambda message: message.text == ADD_HINTS_TEXT)
async def process_add_hints(message: Message):
    db_set_hints(message.from_user.id, 1)
    # TODO добавить удаление подсказок
    # TODO добавить слова в бд
    await message.answer(HINTS_ADDED_TEXT)


# Этот хендлер будет срабатывать на запрос подсказки
@dp.message_handler(lambda message: message.text.strip().upper() in HINT_WORDS)
async def process_hint(message: Message):
    if db_get_guessing(message.from_user.id):
        await message.reply(CHOOSE_HINT_TEXT, reply_markup=kb.hint_kb)

    else:
        await message.answer(NOT_A_WORD_OUT_GAME_TEXT)


# Этот хендлер принимает число - длину слова
@dp.message_handler(lambda message: message.text.isdigit() and 4 <= int(message.text) <= 8)
async def process_change_len(message: Message):
    db_change_len(message.from_user.id, int(message.text))
    db_change_attempts(message.from_user.id, int(message.text))
    await message.answer(LEN_CHANGED_TEXT)


@dp.message_handler(lambda message: message.text == OPEN_VOWELS_TEXT)
async def process_open_vowels(message: Message):
    db_set_hints_left(message.from_user.id, db_get_hints_left(message.from_user.id) - 1)
    mistery = list(db_get_word(message.from_user.id))
    for index, letter in enumerate(mistery):
        if letter not in VOWELS:
            mistery[index] = '*'
    await message.answer(''.join(mistery))


@dp.message_handler(lambda message: message.text == OPEN_SPECIFIC_LETTER_TEXT)
async def process_open_letter_request(message: Message):
    await message.answer(OPEN_SPECIFIC_LETTER_REQUEST_TEXT)


@dp.message_handler(lambda message: message.text.isalpha() and len(message.text) == 1)
async def process_letter(message: Message):
    db_set_hints_left(message.from_user.id, db_get_hints_left(message.from_user.id) - 1)
    mistery = list(db_get_word(message.from_user.id))
    for index, letter in enumerate(mistery):
        if letter != message.text:
            mistery[index] = '*'
    await message.answer(''.join(mistery))


@dp.message_handler(lambda message: message.text == OPEN_LETTER_IN_CERTAIN_PLACE_TEXT)
async def process_open_letter_place_request(message: Message):
    await message.answer(WHAT_PLACE_TEXT)


@dp.message_handler(lambda message: message.text.isdigit() and 1 <= int(message.text) <= 10)
#TODO верхняя граница
async def process_open_place(message: Message):
    db_set_hints_left(message.from_user.id, db_get_hints_left(message.from_user.id) - 1)
    mistery = list(db_get_word(message.from_user.id))
    for index, letter in enumerate(mistery):
        if index + 1 != int(message.text):
            mistery[index] = '*'
    await message.answer(''.join(mistery))


# Этот хэндлер будет срабатывать на отправку пользователем слов нужной длины
@dp.message_handler(
    lambda message: message.text.isalpha() and len(message.text) == db_get_length_of_words(message.from_user.id))
async def process_word_answer(message: Message):
    if db_get_guessing(message.from_user.id):

        # Победа
        if str(message.text).upper() == db_get_word(message.from_user.id):
            db_set_guessing(message.from_user.id, False)
            db_set_played_games(message.from_user.id, db_get_played_games(message.from_user.id) + 1)
            db_set_wins(message.from_user.id, db_get_wins(message.from_user.id) + 1)
            await message.answer(WORD_IS_GUESSED_TEXT)

        # Попытка
        else:
            # Проверка слова на существование
            if str(message.text).upper() in words[db_get_len(message.from_user.id)]:

                # Шаблон для удаления букв в случае повторяющихся букв в слове-загадке
                mistery: str = db_get_word(message.from_user.id)

                # Слово-ответ с подсветкой
                # TODO переименовать
                w = ''
                for letter1, letter2 in zip(db_get_word(message.from_user.id), str(message.text).upper()):
                    if letter1 == letter2:
                        w += '<u>' + letter2.upper() + '</u>'
                        mistery = mistery.replace(letter2.upper(), '', 1)
                    elif letter2 in mistery and str(message.text).upper()[mistery.index(letter2)] != \
                            db_get_word(message.from_user.id)[mistery.index(letter2)]:
                        w += '<b>' + letter2.upper() + '</b>'
                        mistery = mistery.replace(letter2.upper(), '', 1)
                    else:
                        w += '<s>' + letter2.upper() + '</s>'

                db_set_remaining_attempts(message.from_user.id,
                                          db_get_remaining_attempts(message.from_user.id) - 1)
                await message.answer(f' {w}', parse_mode="HTML")

            else:
                await message.answer(MISTAKE_TEXT % db_get_remaining_attempts(message.from_user.id))

        if db_get_remaining_attempts(message.from_user.id) == 0:
            db_set_guessing(message.from_user.id, False)
            db_set_played_games(message.from_user.id, db_get_played_games(message.from_user.id) + 1)
            await message.answer(ATTEMPTS_ENDED_TEXT % db_get_word(message.from_user.id))

    else:
        await message.answer(OFFER_GAME_TEXT)


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message_handler()
async def process_other_text_answers(message: Message):
    if db_get_guessing(message.from_user.id):
        await message.answer(NOT_A_WORD_IN_GAME_TEXT)
    else:
        await message.answer(NOT_A_WORD_OUT_GAME_TEXT)


if __name__ == '__main__':
    executor.start_polling(dp)
