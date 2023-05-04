import random

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message


BOT_TOKEN: str = '5915056188:AAHIMEHYEG_sxcQyNEfIc5IB_y0of-Zzf3Y'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

# Кортежи со словами
words = list()
for ind, length in enumerate(range(4, 9)):
    with open('words/words_len_' + str(length), 'r', encoding="utf-8") as f:
        words.append(tuple(line.strip() for line in f.readlines()))

# Словарь, в котором будут храниться данные пользователей
users: dict = {}


def get_words_with_length(word_length: int) -> tuple:
    """
    Получить кортеж слов длины len.
    word_length-4, т.к. минимальная длина угадываемого слова равна 4.
    Параметры
    ---------

    word_length: int
         Длина слова

    Возвращаемое значение
    ---------------------
    tuple: кортеж слов длины len
    """
    return words[word_length-4]


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    if users.get("{0}".format(message.chat.id), False) is False:
        users["{0}".format(message.chat.id)] = {'in_game': False,
                                                'secret_word': None,
                                                'total_attempts': 5,
                                                'temp_attempts': 5,
                                                'word_len': 5,
                                                'total_games': 0,
                                                'wins': 0}
    await message.answer('Привет!\nДавай сыграем в игру "Угадай слово"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message_handler(commands=['help'])
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю слово из '
                         f'{users["{0}".format(message.chat.id)]["word_len"]} букв, '
                         f'а вам нужно его угадать\nУ вас есть {users["{0}".format(message.chat.id)]["total_attempts"]}'
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message_handler(commands=['stat'])
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users["{0}".format(message.chat.id)]["total_games"]}\n'
                         f'Игр выиграно: {users["{0}".format(message.chat.id)]["wins"]}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message_handler(commands=['cancel'])
async def process_cancel_command(message: Message):
    if users["{0}".format(message.chat.id)]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        users["{0}".format(message.chat.id)]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.strip().upper() in ['ДА', 'ДАВАЙ', 'СЫГРАЕМ', 'ИГРА', 'ДАВАЙ ИГРАТЬ',
                                                                     'ИГРАТЬ', 'ХОЧУ ИГРАТЬ'])
# TODO: Обрезать знаки препинания
# TODO Система подсказок
async def process_positive_answer(message: Message):
    await message.answer('Ура!\n\nЯ загадал слово, попробуй угадать!')
    users["{0}".format(message.chat.id)]['in_game'] = True
    users["{0}".format(message.chat.id)]['secret_word'] = random.choice(get_words_with_length(5))
    users["{0}".format(message.chat.id)]['temp_attempts'] = users["{0}".format(message.chat.id)]["total_attempts"]


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.upper() in ['НЕТ', 'НЕ', 'НЕ ХОЧУ', 'НЕ БУДУ', 'ВЫХОД'])
async def process_negative_answer(message: Message):
    if users["{0}".format(message.chat.id)]['in_game']:
        await message.answer(f'Было загадано слово {users["{0}".format(message.chat.id)]["secret_word"]}.'
                             f'\n\nЕсли захотите поиграть - просто напишите об этом!')
    else:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')


# Этот хэндлер будет срабатывать на отправку пользователем слов нужной длины
@dp.message_handler(
    lambda message: message.text.isalpha() and len(message.text) == users["{0}".format(message.chat.id)]["word_len"])
async def process_word_answer(message: Message):
    if users["{0}".format(message.chat.id)]['in_game']:

        # Победа
        if str(message.text).upper() == users["{0}".format(message.chat.id)]['secret_word']:
            await message.answer('Ура!!! Вы угадали слово!\n\n'
                                 'Может, сыграем еще?')
            users["{0}".format(message.chat.id)]['in_game'] = False
            users["{0}".format(message.chat.id)]['total_games'] += 1
            users["{0}".format(message.chat.id)]['wins'] += 1

        # Попытка
        else:
            # Проверка слова на существование
            if str(message.text).upper() in get_words_with_length(5):

                # Шаблон для удаления букв в случае повторяющихся букв в слове-загадке
                mistery: str = users["{0}".format(message.chat.id)][
                    'secret_word']

                # Слово-ответ с подсветкой
                w = ''
                for letter1, letter2 in zip(users["{0}".format(message.chat.id)]['secret_word'],
                                            str(message.text).upper()):
                    if letter1 == letter2:
                        w += '<u>' + letter2.upper() + '</u>'
                        mistery = mistery.replace(letter2.upper(), '', 1)
                    elif letter2 in mistery and str(message.text).upper()[mistery.index(letter2)] != \
                            users["{0}".format(message.chat.id)]['secret_word'][mistery.index(letter2)]:
                        w += '<b>' + letter2.upper() + '</b>'
                        mistery = mistery.replace(letter2.upper(), '', 1)
                    else:
                        w += '<s>' + letter2.upper() + '</s>'

                await message.answer(f' {w}', parse_mode="HTML")
                users["{0}".format(message.chat.id)]['temp_attempts'] -= 1
            else:
                await message.answer(f'Такого слова нет. '
                                     f'Осталось {users["{0}".format(message.chat.id)]["temp_attempts"]} попыток.')

        if users["{0}".format(message.chat.id)]['temp_attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое слово '
                                 f'было {users["{0}".format(message.chat.id)]["secret_word"]}\n\nДавайте '
                                 f'сыграем еще?')
            users["{0}".format(message.chat.id)]['in_game'] = False
            users["{0}".format(message.chat.id)]['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message_handler()
async def process_other_text_answers(message: Message):
    if users["{0}".format(message.chat.id)]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, слово.')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    executor.start_polling(dp)
