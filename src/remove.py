from main.models import Category, Product

# Список слагов категорий, из которых нужно удалить продукты
slugs = [
    "bystrorezhushij-list",
    "goryachekatanyj-list",
    "zharoprochnyj-list",
    "instrumentalnyj-list",
    "konstrukcionnyj-list",
    "legirovannyj-list",
    "listovaya-gest",
    "nizkolegirovannyj-list",
    "ocinkovannyj-list",
    "perforirovannyj-nerzhaveyushij-list-lge",
    "prosechno-vytyazhnoj-list",
    "riflyonyj-list",
    "stalnoj-list",
    "holodnokatanyj-list",
    "armatura-stalnaya",
    "bystrorezhushij-kvadrat",
    "goryachekatanyj-kvadrat",
    "kalibrovannyj-kvadrat",
    "konstrukcionnyj-kvadrat",
    "otsinkovannyj-kvadrat",
    "bystrorezhushij-krug",
    "instrumentalnyj-krug",
    "konstrukcionnyj-krug",
    "legirovannyj-krug",
    "nizkolegirovannyj-krug",
    "goryachekatanyj-krug",
    "goryachekatanaya-polosa",
    "konstrukcionnaya-polosa",
    "nizkolegirovannaya-polosa",
    "ocinkovannaya-polosa",
    "goryachekatanyj-shestigrannik",
    "besshovnaya-goryachedeformirovannaya-truba",
    "besshovnaya-teplodeformirovannaya-truba",
    "besshovnaya-tolstostennaya-truba",
    "besshovnaya-tonkostennaya-truba",
    "besshovnaya-truba-vysokogo-davleniya",
    "besshovnaya-truba-iz-legirovannoj-stali",
    "besshovnaya-uglerodistaya-truba",
    "besshovnaya-holodnodeformirovannaya-truba",
    "besshovnaya-honingovannaya-truba",
    "burilnaya-truba",
    "truba-vgp",
    "zharoprochnaya-truba",
    "kotelnaya-truba",
    "magistralnaya-truba",
    "neftyanaya-truba",
    "obsadnaya-truba",
    "ocinkovannaya-truba",
]


# Удаление продуктов из указанных категорий
for slug in slugs:
    try:
        category = Category.objects.get(slug=slug)
        products = Product.objects.filter(category=category)
        count = products.count()
        products.delete()
        print(f"Удалено {count} продуктов из категории '{slug}'")
    except Category.DoesNotExist:
        print(f"Категория с слагом '{slug}' не найдена.")
