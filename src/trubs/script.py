import requests
from bs4 import BeautifulSoup
import json

# Новый список ссылок
urls = [
    "https://exportural.kz/besshovnaya-goryachedeformirovannaya-truba/",
    "https://exportural.kz/besshovnaya-holodnodeformirovannaya-truba/",
    "https://exportural.kz/besshovnaya-tolstostennaya-truba/",
    "https://exportural.kz/besshovnaya-tonkostennaya-truba/",
    "https://exportural.kz/besshovnaya-teplodeformirovannaya-truba/",
    "https://exportural.kz/besshovnaya-uglerodistaya-truba/",
    "https://exportural.kz/besshovnaya-truba-iz-legirovannoj-stali/",
    "https://exportural.kz/besshovnaya-honingovannaya-truba/",
    "https://exportural.kz/besshovnaya-kalibrovannaya-truba/",
    "https://exportural.kz/besshovnaya-truba-vysokogo-davleniya/",
    "https://exportural.kz/bimetallicheskaya-truba/",
    "https://exportural.kz/elektrosvarnaya-truba/",
    "https://exportural.kz/truba-vgp/",
    "https://exportural.kz/nasosno-kompressornaya-truba/",
    "https://exportural.kz/truba-v-izolyacii/",
    "https://exportural.kz/truba-v-vus-izolyacii/",
    "https://exportural.kz/stalnaya-truba-v-ppu-izolyacii/",
    "https://exportural.kz/truby-s-tspp-pokrytiem/",
    "https://exportural.kz/truba-v-ppm-izolyacii/",
    "https://exportural.kz/futerovannaya-truba/",
    "https://exportural.kz/obsadnaya-truba/",
    "https://exportural.kz/magistralnaya-truba/",
    "https://exportural.kz/burilnaya-truba/",
    "https://exportural.kz/zharoprochnaya-truba/",
    "https://exportural.kz/precizionnaya-truba/",
    "https://exportural.kz/ocinkovannaya-truba/",
    "https://exportural.kz/kotelnaya-truba/",
    "https://exportural.kz/profilnaya-truba/",
    "https://exportural.kz/profilnaya-kvadratnaya-truba/",
    "https://exportural.kz/profilnaya-pryamougolnaya-truba/",
    "https://exportural.kz/ocinkovannaya-profilnaya-truba/",
    "https://exportural.kz/kaplevidnaya-truba/",
    "https://exportural.kz/arochnaya-truba/",
    "https://exportural.kz/konstrukcionnaya-profilnaya-truba/",
    "https://exportural.kz/neftyanaya-truba/"
]

# Функция для получения товаров
def get_products(url):
    products = []
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Ошибка {response.status_code} при загрузке страницы {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    product_blocks = soup.find_all("div", class_="col-sm-8 col-lg-6")

    if not product_blocks:
        print(f"Товары не найдены на странице {url}")
        return []

    for block in product_blocks:
        # Получаем название товара
        name_tag = block.find("a", class_="mb-1")
        name = name_tag.text.strip() if name_tag else "Без названия"
        
        # Добавляем информацию о товаре в список
        products.append({
            "name": name,
            "link": url
        })

    return products

# Функция для сохранения данных в файл
def save_to_json(products, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в {filename}")

# Основная логика
if __name__ == "__main__":
    for url in urls:
        # Получаем товары для каждой ссылки
        products = get_products(url)
        
        # Если товары найдены, сохраняем их в файл
        if products:
            # Формируем имя файла из последней части URL
            filename = url.split("/")[-2] + ".json"
            save_to_json(products, filename)
        else:
            print(f"Нет данных для {url}")
