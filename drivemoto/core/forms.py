from django import forms
from .models import Product, Category, Characteristic, CharacteristicValue, ProductVariant, ProductVariantImage



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'articul', 'brand', 'extentions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если категория уже выбрана, добавляем поля для значений характеристик
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                category = Category.objects.get(pk=category_id)

                # Для каждой характеристики создаем поле для ввода значения
                for characteristic in category.characteristics.all():
                    self.fields[f'characteristic_{characteristic.id}'] = forms.CharField(
                        label=characteristic.name,
                        required=False  # Характеристики могут быть необязательными
                    )
            except (ValueError, Category.DoesNotExist):
                pass
        elif self.instance.pk:
            # Если форма редактируется, загружаем существующие характеристики и значения
            category = self.instance.category
            for characteristic in category.characteristics.all():
                value = self.instance.characteristic_values.filter(characteristic=characteristic).first()
                self.fields[f'characteristic_{characteristic.id}'] = forms.CharField(
                    label=characteristic.name,
                    initial=value.value if value else '',  # Загружаем существующее значение
                    required=False
                )

    def save(self, commit=True):
        # Сначала сохраняем продукт без его характеристик
        instance = super().save(commit=False)

        # Сохраняем объект, чтобы у него был ID
        if commit:
            instance.save()

        # Сохраняем значения характеристик только после того, как продукт имеет ID
        characteristic_values = []
        for field_name, value in self.cleaned_data.items():
            if field_name.startswith('characteristic_') and value:
                characteristic_id = int(field_name.split('_')[1])
                characteristic = Characteristic.objects.get(id=characteristic_id)

                # Создаем или находим значение характеристики
                characteristic_value, created = CharacteristicValue.objects.get_or_create(
                    characteristic=characteristic,
                    value=value
                )

                characteristic_values.append(characteristic_value)

        # Присваиваем продукту значения характеристик (many-to-many field)
        if characteristic_values:
            instance.characteristic_values.set(characteristic_values)

        return instance
    
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['color', 'price', 'quantity', 'sale']

class ProductVariantImageForm(forms.ModelForm):
    class Meta:
        model = ProductVariantImage
        fields = ['image']



