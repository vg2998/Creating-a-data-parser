import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect(user_login):
    page_num = 0  # начинаем с первой страницы
    data = []
    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/genre/serial/vs/vote/#list{page_num}'  # ссылка с пагинацией
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        # Ищем карточки сериала
        entries = soup.find_all('div', class_ = 'item')
        if len(entries) == 0:  # признак конца списка
            break
        for entry in entries:
            # В каждом элементе <div> ищем элемент с классом 'info'
            # Название сериала и дата релиза
            film_name_details = entry.find('div', class_ = "info")
            # Теперь, внутри info ищем элемент <a> и получаем его текстовое содержимое методом .text:
            film_name = film_name_details.find('a').text
            # Рейтинк сериала
            rating = entry.find('div', class_='rating')
            rating_span = rating.find('b',).text
            data.append({
            'Название сериала и дата релиза': film_name,
            'Рейтинг сериала': rating_span
            })
            page_num += 1
        return data
user_rates = collect(user_login = 46623535)
# Создаем DataFrame и экспорт в Excel
df = pd.DataFrame(user_rates)
df.to_excel('movie_KPrating.xlsx', index=False)
