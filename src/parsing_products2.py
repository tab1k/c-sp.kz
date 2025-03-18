import requests
from bs4 import BeautifulSoup
import time
import random
import os
import django
import json
from django.utils.text import slugify

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from main.models import Product, Category  # Импорт моделей

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Читаем категории из JSON
with open("products.json", "r", encoding="utf-8") as file:
    categories = json.load(file)

def parse_page(url, category):
    """Функция парсинга страницы"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе {url}: {e}")
        return False  # Ошибка → выходим

    soup = BeautifulSoup(response.content, "html.parser")
    product_blocks = soup.find_all("div", class_="col-sm-8 col-lg-6")

    if not product_blocks:
        print(f"⚠️ Нет товаров на {url}, возможно, это последняя страница.")
        return False  # Если товаров нет → дальше не парсим

    for block in product_blocks:
        title_tag = block.find("a", class_="mb-1")
        if not title_tag:
            continue

        product_name = title_tag.text.strip()
        product_url = title_tag["href"]

        # Парсим характеристики
        properties = {}
        props_list = block.find_all("li", class_="mb-1")
        for prop in props_list:
            key_value = prop.get_text(strip=True).split(" ")
            if len(key_value) > 1:
                key = key_value[0]
                value = " ".join(key_value[1:])
                properties[key] = value

        # Создаём slug
        base_slug = slugify(product_name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Запись в базу
        if not Product.objects.filter(name=product_name).exists():
            Product.objects.create(
                name=product_name,
                slug=slug,
                external_url=product_url,
                category=category,
                description=json.dumps(properties, ensure_ascii=False)  # Сохраняем характеристики
            )
            print(f"✅ Добавлен: {product_name} ({product_url}) в {category.slug}")
        else:
            print(f"⚠️ Уже в базе: {product_name}")

    return True  # Если успешно обработаны товары → продолжаем

# Запуск парсинга для всех категорий
for category_data in categories:
    category_name = category_data.get("name", category_data["slug"])  # Если в JSON нет "name", используем slug
    category, created = Category.objects.get_or_create(
        slug=category_data["slug"],
        defaults={"name": category_name}
    )

    if created:
        print(f"✅ Создана категория: {category.slug}")

    for page in range(1, 100):
        page_url = f"{category_data['url']}?page={page}"  # Исправленная пагинация
        if not parse_page(page_url, category):
            break  # Если товаров нет → выходим

        time.sleep(random.uniform(2, 5))  # Пауза для обхода антибота
