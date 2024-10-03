import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Создаем экземпляр драйвера
driver = webdriver.Chrome()

# URL для парсинга
url = "https://www.divan.ru/smolensk/category/divany-i-kresla"

# Открываем страницу
driver.get(url)

# Явное ожидание загрузки элементов
wait = WebDriverWait(driver, 10)

# Находим все элементы с диванами
sofa_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lsooF')))

# Создаем списки для хранения данных
titles = []
prices_raw = []
links = []

# Извлекаем данные
for sofa in sofa_elements:
    try:
        # Извлекаем название дивана
        title_element = sofa.find_element(By.XPATH, ".//span[@itemprop='name']")

        # Извлекаем цену дивана (используя более общий подход)
        price_element = sofa.find_element(By.XPATH,
                                          ".//span[contains(@class, 'ui-LD-ZU') and contains(@class, 'KIkOH')]")

        # Получаем текст цены и валюту
        price_value = price_element.text.strip().replace(" ", "")  # Убираем пробелы из цены
        price_currency = price_element.find_element(By.XPATH,
                                                    ".//span[contains(@class, 'ui-i5wwi')]").text.strip()  # Получаем валюту
        full_price = f"{price_value} {price_currency}"  # Форматируем полную цену

        # Получаем ссылку на диван
        link_element = sofa.find_element(By.XPATH, ".//a[contains(@class, 'ui-GPFV8')]")  # Получаем элемент ссылки

        titles.append(title_element.text.strip())
        prices_raw.append(full_price)  # Добавляем полную цену
        links.append(link_element.get_attribute('href'))

        # Выводим информацию для отладки
        print(
            f"Название: {title_element.text.strip()}, Цена: {full_price}, Ссылка: {link_element.get_attribute('href')}")
    except Exception as e:
        print(f"Ошибка извлечения данных: {e}")

# Закрываем драйвер
driver.quit()

# Сохраняем данные в CSV файл
data = {
    'Название': titles,
    'Цена': prices_raw,
    'Ссылка': links
}
df = pd.DataFrame(data)
df.to_csv('sofa_data.csv', index=False, encoding='utf-8-sig')  # Убедитесь, что файл сохранен с правильной кодировкой
print("Данные успешно спарсены и сохранены в sofa_data.csv")
