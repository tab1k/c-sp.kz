from django.db import models
from django.urls import reverse
from slugify import slugify
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории", db_index=True)
    image = models.ImageField(max_length=255, blank=True, null=True, verbose_name="Картинка категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг", max_length=255)
    about = models.TextField(max_length=555, blank=True, null=True)
    price_list = models.FileField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родительская категория"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('website:category_detail', kwargs={'slug': self.slug})
    
    def get_ancestors(self):
        category = self
        ancestors = []
        while category:
            ancestors.insert(0, category)
            category = category.parent
        return ancestors


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название продукта", db_index=True)
    image = models.ImageField(upload_to='products/', verbose_name="Фото продукта", blank=True)
    external_url = models.URLField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )
    slug = models.SlugField(unique=True, verbose_name="Слаг", blank=True, null=True, max_length=255)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.BigIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        
        indexes = [
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:product_detail', kwargs={'slug': self.slug})
    

class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)  # Например: "Толщина", "Марка стали", "ГОСТ"
    
    class Meta:
        verbose_name = "Атрибут продукта"
        verbose_name_plural = "Атрибуты продуков"

    def __str__(self):
        return self.name
    

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)  # Например: "2 мм", "AISI 304", "ГОСТ 19903-74"

    class Meta:
        verbose_name = "Значение атрибута продукта"
        verbose_name_plural = "Значения атрибутов продукта"
        unique_together = ('product', 'attribute')  # У одного товара не может быть дважды одна и та же характеристика

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"




class Story(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='stories/')
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        return timezone.now() < self.created_at + timedelta(days=3)



class Service(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(max_length=255, blank=False, null=False, verbose_name="Картинка услуг")
    slug = models.SlugField(unique=True, verbose_name="Слаг", max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Заполняем slug, если он не указан вручную
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Service.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:services_detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name