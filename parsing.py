import requests
from bs4 import BeautifulSoup as bs

URL_TEMPLATE = "http://nskhuman.ru/unislov/suschestv.php?nlet1=1&nlet2=2"
FILE_NAME = "test.csv"


def parse(letter: str, length: int, url: str = URL_TEMPLATE) -> tuple:
    """
    Спарсить с сайта со словарем слова на букву letter
    длины length

    Параметры
    ---------

    letter: str
         Первая буква слова
    length: int
         Длина слова
    url: str
        Ссылка на словарь

    Возвращаемое значение
    ---------------------
        tuple
        Кортеж слов на букву letter длины length
    """
    # Корректируем ссылку для текущей буквы
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    words = soup.find_all('a', class_='position_title')

    print(words)
    # Обрезаем переносы на другую строку и пробелы
    # words = tuple(filter(lambda x:  len(x) == length, tuple(map(lambda word: word.text.strip().upper(), words))))

    return words


def get_tuple_const_length(length, url: str = URL_TEMPLATE) -> tuple:
    """
    Получить слова длины length

    Параметры
    ---------

    length: int
         Длина слова
    url: str
        Ссылка на словарь

    Возвращаемое значение
    ---------------------
        tuple
        Кортеж слов длины length
    """
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    tuple_const_length = tuple()
    for letter in alphabet:
        tuple_const_length = tuple_const_length + parse(letter, length, url)
    return tuple_const_length


def write_to_txt(length, url: str = URL_TEMPLATE) -> None:
    """
    Запись в текстовый файл списка слов

    Параметры
    ---------

    length: int
         Длина слова
    url: str
        Ссылка на словарь

    Возвращаемое значение
    ---------------------
    None
    """
    with open("words_len_" + str(length), "w", encoding="utf-8") as fin:
        fin.write('\n'.join(list(get_tuple_const_length(length, url))))


# write_to_txt(4)
# write_to_txt(5)
# write_to_txt(6)
# write_to_txt(7)
# write_to_txt(8)
parse('F', 2)
