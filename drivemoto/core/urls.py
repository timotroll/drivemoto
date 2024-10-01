from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('get_products_by_category/<int:category_id>/', views.get_products_by_category, name='get_products_by_category'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:category_id>', views.catalog_category, name='category_catalog'),
    path('product/', views.product_page, name='product')
]