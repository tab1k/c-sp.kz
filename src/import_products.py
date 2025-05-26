import os
import json
import django
from django.utils.text import slugify


# Настрой Django (если запускаешь вне manage.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")  
django.setup()

from main.models import *

def import_products():
    category_slug = input("Введите slug категории: ").strip()
    json_file = input("Введите путь к JSON-файлу с товарами: ").strip()

    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        print(f"❌ Категория с slug '{category_slug}' не найдена!")
        return

    if not os.path.exists(json_file):
        print(f"❌ Файл '{json_file}' не найден!")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    count = 0
    for item in products_data:
        name = item.get("title")
        if not name:
            continue

        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product = Product.objects.create(
            name=name,
            category=category,
            slug=slug,
            description="Автоматически добавленный товар",
        )

        # Обработка атрибутов
        attributes = item.get("attributes", {})
        for attr_name, attr_value in attributes.items():
            # Получаем или создаём атрибут
            attribute_obj, created = ProductAttribute.objects.get_or_create(name=attr_name)

            # Создаём значение атрибута для продукта
            ProductAttributeValue.objects.create(
                product=product,
                attribute=attribute_obj,
                value=attr_value
            )

        count += 1

    print(f"✅ Добавлено {count} товаров в категорию '{category.name}'")


if __name__ == "__main__":
    import_products()
