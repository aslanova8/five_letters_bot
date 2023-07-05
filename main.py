import random
import sqlite3

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

import keyboards as kb

BOT_TOKEN: str = '5915056188:AAHIMEHYEG_sxcQyNEfIc5IB_y0of-Zzf3Y'


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


def db_get_word(user_id: int) -> int:
    cursor.execute("SELECT word FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchall()[0][0]


def db_set_remaining_attempts(user_id: int, value: int) -> None:
    cursor.execute("UPDATE users SET remaining_attempts=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_guessing(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET guessing=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_wins(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET wins=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_played_games(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET played_games=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_set_word(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET word=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_change_len(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET length_of_words=? WHERE user_id=?", (value, user_id))
    conn.commit()


def db_change_attempts(user_id: int, value: bool) -> None:
    cursor.execute("UPDATE users SET total_attempts=? WHERE user_id=?", (value, user_id))
    conn.commit()
    cursor.execute("UPDATE users SET remaining_attempts=? WHERE user_id=?", (value, user_id))
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

    await message.answer('Привет!\nДавай сыграем в игру "Угадай слово"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message_handler(commands=['help'])
async def process_help_command(message: Message):
    await message.reply(f'Правила игры:\n\nЯ загадываю слово из '
                        f'{db_get_length_of_words(message.from_user.id)} букв, '
                        f'а Вам нужно его угадать\nУ вас есть {db_get_total_attempts(message.from_user.id)} '
                        f'попыток\n\nДоступные команды:\n/help - правила '
                        f'игры и список команд\n/cancel - выйти из игры\n'
                        f'/stat - посмотреть статистику\n\nДавай сыграем?', reply_markup=kb.setting_kb)


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message_handler(commands=['stat'])
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {db_get_played_games(message.from_user.id)}\n'
                         f'Игр выиграно: {db_get_wins(message.from_user.id)}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message_handler(commands=['cancel'])
async def process_cancel_command(message: Message):
    if db_get_guessing(message.from_user.id):
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        db_set_guessing(message.from_user.id, False)
    else:
        await message.answer('А мы итак с Вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.strip().upper() in ['ДА', 'ДАВАЙ', 'СЫГРАЕМ', 'ИГРА', 'ДАВАЙ ИГРАТЬ',
                                                                     'ИГРАТЬ', 'ХОЧУ ИГРАТЬ'])
# TODO: Обрезать знаки препинания
async def process_positive_answer(message: Message):
    await message.answer('Ура!\n\nЯ загадал слово, попробуй угадать!')
    db_set_guessing(message.from_user.id, True)
    db_set_word(message.from_user.id, random.choice(words[db_get_len(message.from_user.id)]))
    db_set_remaining_attempts(message.from_user.id, db_get_total_attempts(message.from_user.id))


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.upper() in ['СДАЮСЬ', 'НЕТ', 'НЕ', 'НЕ ХОЧУ', 'НЕ БУДУ', 'ВЫХОД'])
async def process_negative_answer(message: Message):
    if db_get_guessing(message.from_user.id):
        db_set_played_games(message.from_user.id, db_get_played_games(message.from_user.id) + 1)
        db_set_guessing(message.from_user.id, False)
        await message.answer(f'Было загадано слово {db_get_word(message.from_user.id)}.'
                             f'\n\nЕсли захотите поиграть - просто напишите об этом!')
    else:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')


# Этот хендлер будет срабатывать на нажатие кнопки "Изменить длину слов"
@dp.message_handler(lambda message: message.text == 'Изменить длину слов')
async def process_choose_len(message: Message):
    await message.reply('Выберите длину слова', reply_markup=kb.len_choosing_kb)


# Этот хендлер будет срабатывать на нажатие кнопки "Добавить подсказки"
@dp.message_handler(lambda message: message.text == 'Добавить подсказки')
async def process_add_hints(message: Message):
    # TODO
    # TODO кол-во попыток = кол-во букв в слове
    await message.answer('Подсказки добавлены')


@dp.message_handler(lambda message: message.text.isdigit() and 4 <= int(message.text) <= 8)
async def process_change_len(message: Message):
    print(int(message.text))
    db_change_len(message.from_user.id, int(message.text))
    db_change_attempts(message.from_user.id, int(message.text))
    await message.answer('Длина изменена. Играем дальше?')


# Этот хэндлер будет срабатывать на отправку пользователем слов нужной длины
@dp.message_handler(
    lambda message: message.text.isalpha() and len(message.text) == db_get_length_of_words(message.from_user.id))
async def process_word_answer(message: Message):
    if db_get_guessing(message.from_user.id):

        # Победа
        if str(message.text).upper() == db_get_word(message.from_user.id):
            await message.answer('Ура!!! Вы угадали слово!\n\n'
                                 'Может, сыграем еще?')
            db_set_guessing(message.from_user.id, False)
            db_set_played_games(message.from_user.id, db_get_played_games(message.from_user.id) + 1)
            db_set_wins(message.from_user.id, db_get_wins(message.from_user.id) + 1)
        # Попытка
        else:
            # Проверка слова на существование
            if str(message.text).upper() in words[5]:

                # Шаблон для удаления букв в случае повторяющихся букв в слове-загадке
                mistery: str = db_get_word(message.from_user.id)

                # Слово-ответ с подсветкой
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

                await message.answer(f' {w}', parse_mode="HTML")
                db_set_remaining_attempts(message.from_user.id,
                                          db_get_remaining_attempts(message.from_user.id) - 1)

            else:
                await message.answer(f'Такого слова нет. '
                                     f'Осталось {db_get_remaining_attempts(message.from_user.id)} попыток.')

        if db_get_remaining_attempts(message.from_user.id) == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое слово '
                                 f'было {db_get_word(message.from_user.id)}\n\nДавайте '
                                 f'сыграем еще?')
            db_set_guessing(message.from_user.id, False)
            db_set_played_games(message.from_user.id, db_get_played_games(message.from_user.id) + 1)
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message_handler()
async def process_other_text_answers(message: Message):
    if db_get_guessing(message.from_user.id):
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, слово.')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    executor.start_polling(dp)
