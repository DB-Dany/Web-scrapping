import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# pip install -r requirements.txt

KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def parse_habr_articles():
    """
    Парсит статьи с Хабра и выводит те, которые содержат ключевые слова: 'дизайн', 'фото', 'web', 'python
    """
    # URL страницы
    url = 'https://habr.com/ru/articles/'

    try:
        # Отправляем запрос
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все статьи
        articles = soup.find_all('article')

        results = []

        for article in articles:
            # Извлекаем заголовок
            title_elem = article.find('h2')
            if not title_elem:
                continue

            title = title_elem.text.strip()

            # Извлекаем ссылку
            link_elem = title_elem.find('a')
            if not link_elem or 'href' not in link_elem.attrs:
                continue

            link = link_elem['href']
            if not link.startswith('http'):
                link = 'https://habr.com' + link

            # Извлекаем дату
            time_elem = article.find('time')
            if time_elem and 'datetime' in time_elem.attrs:
                date_str = time_elem['datetime']
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%d.%m.%Y')
                except:
                    formatted_date = date_str
            else:
                formatted_date = 'Дата не указана'

            # Извлекаем превью текст
            preview_text = ''
            preview_elem = article.find('div', class_=lambda x: x and 'article-formatted-body' in x)
            if preview_elem:
                preview_text = preview_elem.text.strip()

            # Проверяем наличие ключевых слов в заголовке или превью
            text_to_check = f"{title} {preview_text}".lower()

            contains_keyword = any(
                re.search(rf'\b{re.escape(keyword.lower())}\b', text_to_check)
                for keyword in KEYWORDS
            )

            if contains_keyword:
                results.append({
                    'date': formatted_date,
                    'title': title,
                    'link': link
                })

        # Выводим результаты
        if results:
            print("Найденные статьи с ключевыми словами:")
            print("=" * 80)
            for article in results:
                print(f"{article['date']} – {article['title']} – {article['link']}")
            print("=" * 80)
            print(f"Всего статей найдено: {len(results)}")
        else:
            print("Статьи с ключевыми словами не найдены.")

    except requests.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск
if __name__ == "__main__":
    parse_habr_articles()