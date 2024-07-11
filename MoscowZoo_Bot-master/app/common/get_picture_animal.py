import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

# URL страницы, которую мы хотим открыть
url = "https://moscowzoo.ru/animals/kinds"

# Создаем экземпляр веб-драйвера (например, Chrome)
driver = webdriver.Chrome()

# Открываем URL
driver.get(url)

try:
    # Ожидание загрузки всей страницы с помощью JavaScript
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

    # Получаем HTML содержимое страницы
    page_source = driver.page_source

    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Ищем все элементы с классом 'animal-item'
    elements = soup.find_all('div', class_='animal-item')

    # Список для хранения данных
    animals = []

    # Обрабатываем каждый элемент
    for element in elements:
        # Извлекаем название животного
        title_element = element.find('span', class_='animal-item__title')
        if title_element:
            title = title_element.text.strip().title()
        else:
            title = "No title"

        # Извлекаем ссылку на изображение
        img_element = element.find('img', class_='animal-item__animal-img')
        if img_element:
            img_url = img_element['src']
        else:
            img_url = "No image"

        # Добавляем данные в список
        animals.append({
            'title': title,
            'image_url': img_url
        })

    # Сохраняем данные в JSON файл
    with open('animals.json', 'w', encoding='utf-8') as f:
        json.dump(animals, f, ensure_ascii=False, indent=4)

    print("Данные успешно сохранены в файл animals.json")
finally:
    # Закрываем драйвер
    driver.quit()
