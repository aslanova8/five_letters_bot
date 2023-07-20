import requests
from bs4 import BeautifulSoup
import sqlite3

URL_TEMPLATE = "https://onlinedic.net/ozhegov/letter%i.php"
URL_WORD_TEMPLATE = 'https://onlinedic.net/ozhegov/page/word%i.php'

# Подключение к бд
conn = sqlite3.connect('database/game_db.db', check_same_thread=False)
cursor = conn.cursor()


def db_add_word(word: str, meaning: str):

    cursor.execute(f"SELECT COUNT(*) FROM words WHERE word='{word}'")
    word_exists = cursor.fetchall()[0][0]
    if not word_exists:
        cursor.execute("INSERT INTO words (word, length, meaning) VALUES (?, ?, ?) ",
                       (str(word), int(len(word)), str(meaning)))
        conn.commit()


def parse():
    """
    Спарсить с сайта со словарем слова
    """
    # Корректируем ссылку для текущей буквы
    counter = 1
    for letter_number in range(1, 30):

        # Изменяем ссылку под букву
        r = requests.get(URL_TEMPLATE % letter_number)

        soup = BeautifulSoup(r.content, "html.parser")
        words = soup.find_all('li')

        # Обрезаем переносы на другую строку и пробелы
        words = tuple(map(lambda word: word.text.strip().upper(), words))

        for word in words:

            # Если слово подходит для игры
            if word.isalpha() and 3 <= len(word) <= 20 and word[-2:] not in ('ТЬ', 'ЫЙ', 'ИЙ', 'СЯ'):
                # Ссылка на страницу со словом
                current_url = URL_WORD_TEMPLATE % counter
                print(current_url)
                r = requests.get(current_url)
                word_soup = BeautifulSoup(r.content, "html.parser")

                # Значение слова
                meaning = word_soup.find('div', class_='text')
                meaning = meaning.text.strip()
                db_add_word(word, meaning)
            else:
                words = tuple(filter(lambda w: word != w, words))

            counter += 1


parse()
