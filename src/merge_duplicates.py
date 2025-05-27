import os
import django

# Настройка Django, если запускаешь скрипт вне manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from django.db import transaction
from main.models import Product, ProductAttributeValue

def merge_duplicate_products():
    # Получаем все уникальные названия товаров в нижнем регистре
    all_names = Product.objects.values_list('name', flat=True)
    unique_names = set(name.lower() for name in all_names)

    for name_lower in unique_names:
        # Находим все товары с таким названием без учета регистра
        products = Product.objects.filter(name__iexact=name_lower)

        if products.count() > 1:
            print(f"Обрабатываем дубликаты для: '{name_lower}' ({products.count()} шт)")

            # Выбираем главный товар — например, товар с самым длинным slug (можно поменять логику)
            main_product = sorted(products, key=lambda p: len(p.slug or ''), reverse=True)[0]

            duplicates = products.exclude(id=main_product.id)

            with transaction.atomic():
                for dup in duplicates:
                    # Переносим уникальные атрибуты на главный товар
                    for attr_val in dup.attributes.all():
                        exists = ProductAttributeValue.objects.filter(
                            product=main_product,
                            attribute=attr_val.attribute
                        ).exists()
                        if not exists:
                            # Переносим атрибут
                            attr_val.product = main_product
                            attr_val.save()
                        else:
                            # Если такой атрибут уже есть у главного товара — удаляем дубликат
                            attr_val.delete()

                    # Можно здесь добавить логику слияния других полей, если нужно

                    # Удаляем дубликат
                    print(f"Удаляем дубликат: {dup.slug} (ID: {dup.id})")
                    dup.delete()

            print(f"Готово с товаром '{main_product.name}'\n")

if __name__ == "__main__":
    merge_duplicate_products()
