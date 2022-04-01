KEYWORDS = ['дизайн', 'фото', 'web', 'python']

import requests
from bs4 import BeautifulSoup

ret = requests.get('https://habr.com/ru/all/')
print(ret.text)
soup = BeautifulSoup(ret.text, 'html.parser')

posts = soup.find_all('article')
for article in posts:
    headline = article.h2.a.text
    post_text = article.div.text
    post_link = article.find('a', class_='post__title_link')
    public_date = article.find('span', class1 = 'post__time')
    print(public_date.text, post_link.attrs.get('href'))

    for search_word in KEYWORDS:
        if (search_word.lower() in headline.lower()) or (search_word.lower() in post_text.lower()):
            print(f'Дата: {public_date}')
            print(f'Заголовок: {headline}')
            print(f'Ссылка: {post_link}')

input()