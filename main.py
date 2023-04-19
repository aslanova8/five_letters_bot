import random

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

BOT_TOKEN: str = '5915056188:AAHIMEHYEG_sxcQyNEfIc5IB_y0of-Zzf3Y'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

#
file_len_5 = open(f'words_len_5.txt', 'r', encoding='utf-8')
L_WORDS: list = [line.strip() for line in file_len_5.readlines()]
file_len_5.close()

# Словарь, в котором будут храниться данные пользователей
users: dict = {}


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    if users.get("{0}".format(message.chat.id), False) is False:
        users["{0}".format(message.chat.id)] = {'in_game': False,
                                                'secret_word': None,
                                                'attempts': 5,
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
                         f'а вам нужно его угадать\nУ вас есть {users["{0}".format(message.chat.id)]["attempts"]} '
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
@dp.message_handler(lambda message: message.text.strip().upper() in ['ДА', 'ДАВАЙ', 'СЫГРАЕМ', 'ИГРА',
                                                                     'ИГРАТЬ', 'ХОЧУ ИГРАТЬ'])
# TODO: Обрезать знаки препинания
async def process_positive_answer(message: Message):
    if not users["{0}".format(message.chat.id)]['in_game']:
        await message.answer('Ура!\n\nЯ загадал слово,'
                             'попробуй угадать!')
        users["{0}".format(message.chat.id)]['in_game'] = True
        users["{0}".format(message.chat.id)]['secret_word'] = random.choice(L_WORDS)
        users["{0}".format(message.chat.id)]['attempts'] = users["{0}".format(message.chat.id)]["attempts"]
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на слова '
                             f'из {users["{0}".format(message.chat.id)]["word_len"]} букв '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.upper() in ['НЕТ', 'НЕ', 'НЕ ХОЧУ', 'НЕ БУДУ', 'ВЫХОД'])
async def process_negative_answer(message: Message):
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
            mistery: str = users["{0}".format(message.chat.id)][
                'secret_word']  # Шаблон для удаления букв в случае повторяющихся букв в слове-загадке
            w = ''  # Слово-ответ с подсветкой
            for letter1, letter2 in zip(users["{0}".format(message.chat.id)]['secret_word'], str(message.text).upper()):
                if letter1 == letter2:
                    w += '<u>' + letter2.upper() + '</u>'
                    mistery = mistery.replace(letter2.upper(), '', 1)
                elif letter2 in mistery:
                    w += '<b>' + letter2.upper() + '</b>'
                    mistery = mistery.replace(letter2.upper(), '', 1)
                else:
                    w += '<s>' + letter2.upper() + '</s>'

            await message.answer(f''
                                 f' {w}', parse_mode="HTML")
            users["{0}".format(message.chat.id)]['attempts'] -= 1

        if users["{0}".format(message.chat.id)]['attempts'] == 0:
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
