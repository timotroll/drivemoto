from django.db import models
from django.utils.text import slugify
import random
import math
import string
from django.utils import timezone
from datetime import date


def generate_unique_articul():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Путь для хранения изображений варианта продукта
def product_variant_image_directory_path(instance, filename):
    return f'products/{instance.variant.product.id}/variants/{instance.variant.id}/{filename}'

class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sale(models.Model):
    name = models.CharField(max_length=255)  # Название скидки
    discount_percent = models.PositiveIntegerField()
    start_date = models.DateTimeField()  # Дата начала скидки
    end_date = models.DateTimeField()  # Дата окончания скидки

    @property
    def is_active(self):
        # Проверяем, активна ли скидка
        return self.start_date <= timezone.now() <= self.end_date

    def calculate_discounted_price(self, original_price):
        # Рассчитываем новую цену со скидкой и округляем
        if self.is_active:
            
            discount = (original_price * self.discount_percent) // 100
            discounted_price = original_price - discount
            # Округляем до ближайших 100 рублей
            return (discounted_price // 100)
        return original_price

    def __str__(self):
        return f"{self.discount_percent}% discount from {self.start_date} to {self.end_date}"
    

# Модель для категорий товаров
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Модель для характеристик, связанных с категорией
class Characteristic(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='characteristics', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    def save(self, *args, **kwargs):
        # Если slug не указан, создаем его на основе имени
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Модель для значений характеристик
class CharacteristicValue(models.Model):
    characteristic = models.ForeignKey(Characteristic, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.value} ({self.characteristic.name})"

# Модель для товаров
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    characteristic_values = models.ManyToManyField(CharacteristicValue, related_name='products')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    articul = models.CharField(max_length=10, unique=True, default=generate_unique_articul)
    extentions = models.CharField(max_length=10, choices=[
        ('new', 'New'),
        ('dealer', 'Dealer'),
        ('hit', 'Hit'),
    ], blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Если slug не указан, создаем его на основе имени
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

from django.core.exceptions import ValidationError

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name='variants', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(help_text="Цена в копейках")
    quantity = models.PositiveIntegerField()
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def get_price_in_rub(self):
        return self.price / 100
    
    @property
    def discounted_price(self):
        if self.sale:
            return self.sale.calculate_discounted_price(self.price)
        return self.price


    def __str__(self):
        return f'{self.product.name} ({self.color.name})'
    
    # def clean(self):
    #     """Ограничение количества изображений для варианта продукта"""
    #     if self.images.count() < 1 or self.images.count() > 5:
    #         raise ValidationError('Каждый вариант продукта должен иметь от 1 до 5 изображений.')
        
# Модель для хранения изображений варианта продукта
class ProductVariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_variant_image_directory_path)

    def __str__(self):
        return f'Image for {self.variant}'

