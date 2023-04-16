import random

import telegram as telegram
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message

BOT_TOKEN: str = '5915056188:AAHIMEHYEG_sxcQyNEfIc5IB_y0of-Zzf3Y'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 5
WORD_LEN: int = 5

file = open(f'words_len_{WORD_LEN}.txt', 'r', encoding='utf-8')
L_WORDS: list = [line.strip() for line in file.readlines()]
file.close()

# Словарь, в котором будут храниться данные пользователя
user: dict = {'in_game': False,
              'secret_word': None,
              'attempts': None,
              'total_games': 0,
              'wins': 0}


# Функция возвращающая случайное целое слово
def get_random_word() -> str:
    return random.choice(L_WORDS)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай слово"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message_handler(commands=['help'])
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю слово из {WORD_LEN} букв, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message_handler(commands=['stat'])
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_games"]}\n'
                         f'Игр выиграно: {user["wins"]}')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message_handler(commands=['cancel'])
async def process_cancel_command(message: Message):
    if user['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом')
        user['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message_handler(lambda message: message.text.upper() in ['ДА', 'Давай', 'Сыграем', 'Игра',
                                                     'Играть', 'Хочу играть'])
async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer('Ура!\n\nЯ загадал слово,'
                             'попробуй угадать!')
        user['in_game'] = True
        user['secret_word'] = get_random_word()
        user['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на слова '
                             f'из {WORD_LEN} букв '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message_handler(lambda message: message.text in ['Нет', 'Не', 'Не хочу', 'Не буду'])
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             f'пожалуйста, слова из {WORD_LEN} букв')


# Этот хэндлер будет срабатывать на отправку пользователем слов нужной длины
@dp.message_handler(lambda message: message.text.isalpha() and len(message.text) == WORD_LEN)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if str(message.text) == user['secret_word']:
            await message.answer('Ура!!! Вы угадали слово!\n\n'
                                 'Может, сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
        else:
            w = ''
            sig = ''
            for letter1, letter2 in zip(user['secret_word'], str(message.text).upper()):
                if letter1 == letter2:
                    w += '<b>' + letter2.upper() + '</b>'
                    sig += '*'
                elif letter2 in user['secret_word']:
                    w += '<u>'+letter2.upper() + '</u>'
                    sig += '-'
                else:
                    w += letter2.upper()
                    sig += ' '
            await message.answer(f''
                                 f' {w}\n'
                                 f' {sig}', parse_mode="HTML")
            user['attempts'] -= 1

        if user['attempts'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое слово '
                                 f'было {user["secret_word"]}\n\nДавайте '
                                 f'сыграем еще?')
            user['in_game'] = False
            user['total_games'] += 1
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message_handler()
async def process_other_text_answers(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, слово.')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')


if __name__ == '__main__':
    executor.start_polling(dp)
