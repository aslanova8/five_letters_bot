BOT_TOKEN: str = '5915056188:AAHIMEHYEG_sxcQyNEfIc5IB_y0of-Zzf3Y'

VOWELS = 'АУЕОЭЮЫИЯЁ'

AGREEMENT_WORDS: list[str] = ['ДА', 'ДАВАЙ', 'СЫГРАЕМ', 'ИГРА', 'ДАВАЙ ИГРАТЬ', 'ИГРАТЬ', 'ХОЧУ ИГРАТЬ']

HINT_WORDS: list[str] = ['ПОДСКАЗКА', 'ХОЧУ ПОДСКАЗКУ', 'ДАЙ ПОДСКАЗКУ', 'ПОДСКАЖИ']

EXIT_WORDS: list[str] = ['СДАЮСЬ', 'НЕТ', 'НЕ', 'НЕ ХОЧУ', 'НЕ БУДУ', 'ВЫХОД']

HELLO_TEXT: str = 'Привет, %s!\nДавай сыграем в игру "Угадай слово"?\nЧтобы получить правила игры и список доступных ' \
                  'команд - отправьте команду /help'

RULES_TEXT: str = 'Правила игры:\n\nЯ загадываю слово из %i букв, ' \
                  'а Вам нужно его угадать\nУ вас есть %i ' \
                  'попыток\n\nДоступные команды:\n/help - правила ' \
                  'игры и список команд\n/cancel - выйти из игры\n' \
                  '/stat - посмотреть статистику\n\nДавай сыграем?'

STATISTICS_TEXT: str = 'Всего игр сыграно: %i\nИгр выиграно: %i'

OFFER_GAME_TEXT: str = 'Мы еще не играем. Хотите сыграть?'

EXIT_TEXT: str = 'Вы вышли из игры. Если захотите сыграть снова - напишите об этом'

LETS_GUESS_TEXT: str = 'Ура!\nЯ загадал слово, попробуй угадать!'

MISTAKE_TEXT: str = 'Такого слова нет. Осталось %i попыток.'

ATTEMPTS_ENDED_TEXT: str = 'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\nМое слово было %s' \
                           '\n\nДавайте сыграем еще?'

CHANGE_LEN_TEXT: str = 'Изменить длину слов'

ADD_HINTS_TEXT: str = 'Добавить подсказки'

CHOOSE_LEN_TEXT: str = 'Выберите длину слова'

OPEN_MISTERY_TEXT: str = 'Было загадано слово %s.\n\nЕсли захотите поиграть - просто напишите об этом!'

HINTS_ADDED_TEXT: str = 'Подсказки добавлены'

CHOOSE_HINT_TEXT: str = 'Выберите подсказку'

LEN_CHANGED_TEXT: str = 'Длина изменена. Играем дальше?'

WORD_IS_GUESSED_TEXT: str = 'Ура!!! Вы угадали слово!\nМожет, сыграем еще?'

NOT_A_WORD_IN_GAME_TEXT: str = 'Мы же сейчас с вами играем. Присылайте, пожалуйста, слово.'

NOT_A_WORD_OUT_GAME_TEXT: str = 'Я довольно ограниченный бот, давайте просто сыграем в игру?'

OPEN_VOWELS_TEXT: str = 'Открыть гласные'

WHAT_PLACE_TEXT: str = 'Какую по счету букву открыть?'

OPEN_SPECIFIC_LETTER_TEXT: str = 'Открыть определенную букву'

OPEN_SPECIFIC_LETTER_REQUEST_TEXT: str = 'Пришлите букву'

PROMOTION_TEXT: str = 'Тебя давно не было в Wordle!'

NO_HINT_TEXT: str = 'Подсказок больше нет'

OPEN_LETTER_IN_CERTAIN_PLACE_TEXT: str = 'Открыть букву на определенном месте'
