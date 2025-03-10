import requests
from bs4 import BeautifulSoup
import time
import random
import os
import django
import json
from django.utils.text import slugify

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from main.models import Product, Category  # Импорт моделей

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Читаем категории из JSON
with open('products.json', 'r', encoding='utf-8') as file:
    categories = json.load(file)

def parse_page(url, category):
    """Функция парсинга страницы"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при запросе {url}: {e}")
        return False  # Вернём False, если запрос не удался

    soup = BeautifulSoup(response.content, "html.parser")
    product_rows = soup.find_all("tr", class_="product-table__item")

    if not product_rows:
        print(f"⚠️ Нет товаров на {url}, возможно, это последняя страница.")
        return False  # Если товаров нет, значит дальше парсить не нужно

    for row in product_rows:
        title_tag = row.find("div", class_="short-product__title")
        if title_tag:
            product_name = title_tag.get_text(strip=True)
            product_slug = slugify(product_name)

            if not Product.objects.filter(slug=product_slug).exists():
                Product.objects.create(
                    name=product_name,
                    slug=product_slug,
                    category=category
                )
                print(f"✅ Добавлен: {product_name} в категорию {category.slug}")
            else:
                print(f"⚠️ Уже в базе: {product_name}")

    return True  # Если успешно обработаны товары, продолжаем парсинг

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
        page_url = category_data["url"] if page == 1 else f"{category_data['url']}page__{page}/"
        if not parse_page(page_url, category):
            break  # Если товаров нет или ошибка, выходим из цикла

        time.sleep(random.uniform(2, 5))  # Пауза, чтобы не забанили
