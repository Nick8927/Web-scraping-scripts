from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def save_to_file(data, filename="currency_rates.md"):
    """Сохраняет переданные данные в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)
    print(f"Данные сохранены в файл {filename}")


options = Options()
options.add_argument("--headless")  # фоновый запуск браузера

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.cbr.ru/currency_base/daily/")
    time.sleep(3)

    usd_element = driver.find_element(By.XPATH, "//tr[td[contains(text(), 'USD')]]/td[last()]")
    usd_rate = usd_element.text

    eur_element = driver.find_element(By.XPATH, "//tr[td[contains(text(), 'EUR')]]/td[last()]")
    eur_rate = eur_element.text

    result_text = f"Курс доллара: {usd_rate} руб.\nКурс евро: {eur_rate} руб."
    save_to_file(result_text)

    print(f"Курс доллара: {usd_rate} руб.")
    print(f"Курс евро: {eur_rate} руб.")

finally:
    driver.quit()
