import django_filters
from django import forms
from .models import Product, ProductAttributeValue, ProductAttribute

class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_name',
        label='Поиск',
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Поиск по товарам...'
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Получаем queryset из self.queryset или kwargs
        qs = getattr(self, 'queryset', None)
        if qs is None:
            qs = kwargs.get('queryset', None)
        if qs is not None and qs.exists():
            category = qs.first().category

            attribute_ids = ProductAttributeValue.objects.filter(
                product__category=category
            ).values_list('attribute', flat=True).distinct()

            for attribute_id in attribute_ids:
                attribute = ProductAttribute.objects.get(id=attribute_id)
                values = ProductAttributeValue.objects.filter(
                    product__category=category,
                    attribute=attribute
                ).values_list('value', flat=True).distinct()

                # Обновляем фильтры динамически
                self.filters.update({
                    f'attr_{attribute_id}': django_filters.ChoiceFilter(
                        label=attribute.name,
                        choices=[(v, v) for v in values],
                        method=self.filter_by_attribute(attribute),
                        widget=forms.Select(attrs={'class': 'form-select form-select-sm mb-3'}),
                        required=False
                    )
                })

    def filter_by_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)

    def filter_by_attribute(self, attribute):
        def inner_filter(queryset, name, value):
            if not value:
                return queryset
            return queryset.filter(
                attributes__attribute=attribute,
                attributes__value=value
            )
        return inner_filter

    class Meta:
        model = Product
        # Можно оставить пустым, т.к. поля создаются динамически
        fields = ['search']

