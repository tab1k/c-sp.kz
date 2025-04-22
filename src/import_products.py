import os
import json
import django
from django.utils.text import slugify


# Настрой Django (если запускаешь вне manage.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")  
django.setup()

from main.models import Category, Product 

def import_products():
    category_slug = input("Введите slug категории: ").strip()
    json_file = input("Введите путь к JSON-файлу с товарами: ").strip()

    # Проверяем существование категории
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        print(f"❌ Категория с slug '{category_slug}' не найдена!")
        return

    # Проверяем файл
    if not os.path.exists(json_file):
        print(f"❌ Файл '{json_file}' не найден!")
        return

    # Загружаем товары
    with open(json_file, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    count = 0
    for item in products_data:
        print("ITEM:", item)
        name = item.get("title")
        if not name:
            continue

        # Генерируем slug (проверяем уникальность)
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Создаем продукт
        Product.objects.create(
            name=name,
            category=category,
            slug=slug,
            description="Автоматически добавленный товар",
        )
        count += 1

    print(f"✅ Добавлено {count} товаров в категорию '{category.name}'")

if __name__ == "__main__":
    import_products()
