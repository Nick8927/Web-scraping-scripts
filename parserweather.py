import requests
from bs4 import BeautifulSoup

def get_weather_info():
    url = "https://www.gismeteo.ru/weather-moscow-4368/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    # Сохраняем весь HTML-код в файл для анализа
    with open("page_content.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    city_name_element = soup.select_one("h1")
    city_name = city_name_element.text.strip() if city_name_element else "Город не найден"

    temperature_element = soup.select_one('temperature-value')
    temperature = temperature_element.get("value") if temperature_element else "Температура не найдена"

    return {
        "city": city_name,
        "temperature": temperature,
    }

def save_weather_info(weather_info, filename="weather_info.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Город: {weather_info['city']}\n")
        file.write(f"Температура: {weather_info['temperature']}°C\n")
    print(f"Информация о погоде сохранена в {filename}")

if __name__ == "__main__":
    weather_info = get_weather_info()
    if weather_info:
        save_weather_info(weather_info, "weather_info.txt")  # можешь в .md писать
        print(weather_info)
