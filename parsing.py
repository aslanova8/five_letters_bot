import requests
from bs4 import BeautifulSoup as bs

URL_TEMPLATE = "https://kupidonia.ru/spisok/spisok-suschestvitelnyh-russkogo-jazyka/bukva/"
FILE_NAME = "test.csv"


def parse(letter: str, length: int, url: str = URL_TEMPLATE) -> tuple:
    """
    Спарсить с сайта со словарем слова на букву letter
    длины length
    """
    # Корректируем ссылку для текущей буквы
    r = requests.get(url + letter)
    soup = bs(r.text, "html.parser")
    words = soup.find_all('div', class_='position_title')

    # Обрезаем переносы на другую строку и пробелы
    words = tuple(filter(lambda x:  len(x) == length, tuple(map(lambda word: word.text.strip().upper(), words))))

    return words


def get_tuple_const_length(length) -> tuple:
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'
    tuple_const_length = tuple()
    for letter in alphabet:
        tuple_const_length = tuple_const_length + parse(letter, length)
    return tuple_const_length

