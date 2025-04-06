import os
import json
import django
from django.utils.text import slugify

# Настрой Django (если запускаешь вне manage.py)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")  
django.setup()

from main.models import Category, Product

# Маппинг URL на слаги категорий
url_to_slug_mapping = {
    "https://exportural.kz/stalnoj-list/": "stalnoj-list",
    "https://exportural.kz/ocinkovannyj-list/": "ocinkovannyj-list",
    "https://exportural.kz/listovaya-gest/": "listovaya-gest",
    "https://exportural.kz/riflyonyj-list/": "stalnye-riflenye-listy",
    "https://exportural.kz/perforirovannyj-list/": "perforirovannyj-list",
    "https://exportural.kz/prosechno-vytyazhnoj-list/": "prosechno-vytyazhnoj-list",
    "https://exportural.kz/goryachekatanyj-list/": "goryachekatanyj-list",
    "https://exportural.kz/holodnokatanyj-list/": "holodnokatanyj-list",
    "https://exportural.kz/nizkolegirovannyj-list/": "nizkolegirovannyj-list",
    "https://exportural.kz/legirovannyj-list/": "legirovannyj-list",
    "https://exportural.kz/zharoprochnyj-list/": "zharoprochnyj-list",
    "https://exportural.kz/konstrukcionnyj-list/": "konstrukcionnyj-list",
    "https://exportural.kz/instrumentalnyj-list/": "instrumentalnyj-list",
    "https://exportural.kz/bystrorezhushij-list/": "bystrorezhushij-list",
}

def import_products_from_file(json_file, category_slug):
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
        name = item.get("name")
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

def import_all_products():
    base_path = '/app/src/listovoi'  # Укажи путь до папки с JSON-файлами

    # Проходим по каждому JSON-файлу и импортируем товары
    for folder_name, category_slug in url_to_slug_mapping.items():
        json_file = os.path.join(base_path, f"{category_slug}.json")
        import_products_from_file(json_file, category_slug)

if __name__ == "__main__":
    import_all_products()
