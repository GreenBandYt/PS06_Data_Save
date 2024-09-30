import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver  = webdriver.Chrome()

url = "https://www.divan.ru/smolensk/category/sadovye-stoly"

driver.get(url)
time.sleep(5)

stoly = driver.find_elements(By.CLASS_NAME, 'lsooF')
print(stoly)
parsed_data = []

for stol in stoly:
    try:
        title = stol.find_element(By.CSS_SELECTOR, 'class.ui-GPFV8').text
        #price = stol.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU KIkOH').text
        #link = stol.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8 qUioe ProductName ActiveProduct').get_attribute('href')
    except:
        print("Произошла ошибка при парсинге")
        continue


    parsed_data.append([title])
driver.quit()

with open('hh.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Название', 'Цена', 'Ссылка'])
    writer.writerows(parsed_data)




