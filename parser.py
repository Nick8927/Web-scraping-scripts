import sqlite3
import requests
from bs4 import BeautifulSoup


def get_hacker_news_titles():
    url = "https://news.ycombinator.com/"
    headers = {"User-Agent": "Mozilla/5.0"}  # Добавляем заголовок, чтобы сайт не блокировал запрос
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    titles = [title.text for title in soup.select(".titleline a")]
    return titles


def save_to_sqlite(titles, db_name="news.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE
        )
    """)

    for title in titles:
        try:
            cursor.execute("INSERT INTO news (title) VALUES (?) ON CONFLICT(title) DO NOTHING", (title,))
        except sqlite3.IntegrityError:
            pass  # Пропускаем дубликаты

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    news_titles = get_hacker_news_titles()
    save_to_sqlite(news_titles)
    for idx, title in enumerate(news_titles, 1):
        print(f"{idx}. {title}")
