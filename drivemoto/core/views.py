from django.shortcuts import render, HttpResponse
from .models import Product, Category, ProductVariant
from django.http import JsonResponse
from django.template.loader import render_to_string

def index(request):
    # Получаем все продукты с их активными вариантами
    product_with_sale = Product.objects.prefetch_related('variants__sale').first()

    categories = Category.objects.all()[:6]
    
    # Получаем товары для первой категории (например, для категории "Запчасти" с ID=1)
    initial_category = Category.objects.filter(pk=categories[0].pk).first() if categories.exists() else None

    # Получаем товары для первой категории (например, для категории "Запчасти" с ID=1)
    initial_products = ProductVariant.objects.filter(product__category=initial_category)[:4] if initial_category else []

    return render(request, 'core/indexx.html', {'saleproduct': product_with_sale,
                                                'categories': categories,
                                                'initial_products': initial_products,})

def get_products_by_category(request, category_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Проверяем, что это AJAX-запрос
        # Получаем категорию по её ID
        category = Category.objects.get(pk=category_id)
        # Получаем 4 товара из этой категории
        products = ProductVariant.objects.filter(product__category=category)[:4]

        # Рендерим HTML для товаров
        html = render_to_string('core/ProductSliderTemplate.html', {'products': products})
        
        return HttpResponse(html)
    return JsonResponse({'error': 'Некорректный запрос'}, status=400)

def catalog_category(request, category_id):
    products = Product.objects.filter(category=category_id)
    return render(request, 'core/catalog_category.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'core/catalog.html', {'products': products})

def product_page(request):
    return render(request, 'core/product_page.html')