import requests
from bs4 import BeautifulSoup
from .models import News
from datetime import datetime, timedelta
import re
import pytz
from django.db.models import Max


def parse_and_save_data():
    base_url = 'https://ria.ru/tourism_news/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    containers1 = soup.find_all('div', class_='list-item')

    data_list = []

    latest_news_title = News.objects.filter(time=News.objects.aggregate(Max('time'))['time__max']).first()

    for container in containers1:
        title = container.find('a', class_='list-item__title').text
        if latest_news_title and title == latest_news_title.title:
            break

        link = container.find('a', class_='list-item__image')['href']
        news_url = link
        news_response = requests.get(news_url)
        news_soup = BeautifulSoup(news_response.text, 'html.parser')

        article_text_divs = news_soup.find_all('div', class_='article__text')

        body = ""
        for article_text_div in article_text_divs:
            body += '<p class="post__text">' + article_text_div.text + "<p>"

        image = container.find('img', class_='responsive_img')['src']
        time_str = container.find('div', class_='list-item__date').text

        # Создайте словарь для сопоставления названий месяцев и их числовых значений
        month_mapping = {
            'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
            'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
        }


        if time_str == re.search(r'\d+:\d+', time_str).group(0) or time_str == re.search(r'\d+:\d+', time_str):  # Если время в формате HH:MM
            time_str = re.search(r'\d+:\d+', time_str).group(0) if re.search(r'\d+:\d+', time_str) else time_str
            time = datetime.now(pytz.utc).replace(
                hour=int(time_str.split(':')[0]),
                minute=int(time_str.split(':')[1]),
                second=0,
                microsecond=0,
            )
        elif 'Вчера' in time_str:  # Если время вида "Вчера 12:10"
            time_parts = time_str.split(', ')
            time = datetime.now(pytz.utc) - timedelta(days=1)
            time = time.replace(
                hour=int(time_parts[1].split(':')[0]),
                minute=int(time_parts[1].split(':')[1]),
                second=0,
                microsecond=0,
            )
        else:  # Другие форматы, включая "день месяц время"
            time_parts = time_str.split(' ')
            day = int(time_parts[0])
            month = month_mapping.get(time_parts[1].lower())
            if month is not None:
                current_year = datetime.now(pytz.utc).year
                time = datetime(current_year, month, day)
                time = time.replace(
                    hour=int(time_parts[2].split(':')[0]),
                    minute=int(time_parts[2].split(':')[1]),
                    second=0,
                    microsecond=0,
                )

        news_data = {
            'title': title,
            'image': image,
            'time': time,
            'body': body,
        }

        data_list.insert(0, news_data)

        for news_data in data_list:
            news_item, created = News.objects.get_or_create(title=news_data['title'],
                                                            defaults={'image': news_data['image'],
                                                                      'time': news_data['time'],
                                                                      'body': news_data['body']})

            if created or news_item.time != news_data['time']:
                news_item.image = news_data['image']
                news_item.time = news_data['time']
                news_item.body = news_data['body']
                news_item.save()


parse_and_save_data()
