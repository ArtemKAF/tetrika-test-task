import asyncio
import csv
import os
import random
from collections import defaultdict

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Tag
from fake_useragent import UserAgent as ua

base_url = "https://ru.wikipedia.org/"
sub_url = "wiki/Категория:Животные_по_алфавиту"

beasts = defaultdict(int)


async def fetch(session: aiohttp.ClientSession, url: str) -> str | None:
    """
    Асинхронно загружает содержимое указанной веб-страницы.

    :param session: Клиентская сессия aiohttp.
    :param url: URL-адрес целевой страницы.
    :return: HTML-контент страницы или None в случае ошибки.
    """
    headers = {"User-Agent": ua().random}

    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Ошибка при получении ответа: {e}")
        return None


def extract_next_sub_url(soup: BeautifulSoup) -> str | None:
    """
    Находит ссылку на следующую страницу категории 'Животные по алфавиту'.

    :param soup: Объект BeautifulSoup с разобранным HTML.
    :return: href следующей страницы или None, если не найден.
    """
    next_link = soup.find(
        lambda tag: (
            tag.name == "a"
            and tag.get("title") == "Категория:Животные по алфавиту"
            and tag.text.strip() == "Следующая страница"
        )
    )
    if isinstance(next_link, Tag):
        href = next_link.get("href", None)
        return str(href)
    return None


def parse_beast_links(soup: BeautifulSoup) -> None:
    """
    Парсит список животных и увеличивает счётчики по первой букве.

    :param soup: Объект BeautifulSoup с разобранным HTML.
    :return: None
    """
    beasts_list = soup.select("#mw-pages div.mw-category-group li a")

    for link in beasts_list:
        title = link.get_text(strip=True)
        if title:
            first_char = title[0].upper()
            beasts[first_char] += 1


def save_results_to_file(filename: str = "beasts.csv") -> None:
    """
    Сохраняет результаты анализа в текстовый файл.

    :param filename: Имя файла для сохранения.
    :return: None
    """
    try:
        file_exists = os.path.isfile(filename)

        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["Буква", "Количество"])

            for letter, count in sorted(beasts.items()):
                writer.writerow([letter, count])

        print(f"✅ Результаты успешно сохранены в '{filename}'")

    except Exception as e:
        print(f"❌ Не удалось сохранить файл: {e}")


async def main(start_url: str) -> None:
    """
    Основной асинхронный процесс: проход по страницам категории,
    сбор данных о первых буквах названий животных.

    :param start_url: Начальный URL для парсинга.
    :return: None
    """
    url = start_url
    while url:
        async with aiohttp.ClientSession() as session:
            html_responce = await fetch(session, url)
            if html_responce:
                soup = BeautifulSoup(html_responce, "lxml")

                parse_beast_links(soup)

                next_page = extract_next_sub_url(soup)
                url = f"{base_url}{next_page}" if next_page else None

        delay = random.uniform(0.5, 2)
        print(f"Ждём {delay:.2f} секунд перед следующим запросом...")
        await asyncio.sleep(delay)


if __name__ == "__main__":
    start_url = f"{base_url}{sub_url}"
    asyncio.run(main(start_url))

    save_results_to_file()
