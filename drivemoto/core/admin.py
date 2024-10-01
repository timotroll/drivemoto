from django.contrib import admin
from .models import Product, Category, Characteristic, CharacteristicValue, ProductVariantImage, ProductVariant, Color, Sale, Brand
from .forms import ProductForm

class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    inlines = [ProductVariantImageInline]

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    add_form_template = "admin/core/product/add_form.html"
    change_form_template = "admin/core/product/change_form.html"
    list_display = ['name', 'articul', 'category', 'slug', 'extentions']
    prepopulated_fields = {"slug": ("name",)}  # Автоматическая генерация slug на основе имени
    inlines = [ProductVariantInline]

    # Добавляем отображение всех полей в форме администратора
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'slug', 'articul', 'extentions'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Сначала сохраняем продукт (чтобы у него был ID)
        super().save_model(request, obj, form, change)

        # Сохраняем значения характеристик после того, как продукт уже сохранен
        form.save_m2m()  # Это сохраняет many-to-many отношения

    # В админ-классе
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Если данные отправлены через POST
        if request.method == 'POST':
            form = self.get_form(request)(data=request.POST, files=request.FILES)
            
            if form.is_valid():
                # Сначала сохраняем сам продукт
                obj = form.save(commit=False)
                obj.save()  # Теперь у объекта есть ID

                # Теперь можно сохранить many-to-many данные (характеристики и т.д.)
                form.save_m2m()

                # Возвращаемся на страницу списка продуктов
                return self.response_add(request, obj)
            
            # Если форма невалидна, данные передаем в контекст
            extra_context['form'] = form
        else:
            # Инициализируем пустую форму
            form = self.get_form(request)()
            extra_context['form'] = form

        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        # Получаем объект, который редактируем
        obj = self.get_object(request, object_id)

        # Если данные отправлены через POST
        if request.method == 'POST':
            form = self.get_form(request, obj=obj)(data=request.POST, files=request.FILES, instance=obj)
            
            if form.is_valid():
                # Сохраняем изменения
                obj = form.save(commit=False)
                obj.save()  # Сохраняем объект с изменениями

                # Сохраняем many-to-many данные
                form.save_m2m()

                # Возвращаемся на страницу редактирования
                return self.response_change(request, obj)
            
            # Если форма невалидна, передаем данные в контекст
            extra_context['form'] = form
        else:
            # Если форма открывается без отправки данных, загружаем текущие данные
            form = self.get_form(request, obj=obj)(instance=obj)
            extra_context['form'] = form

        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    


admin.site.register(Product, ProductAdmin)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    pass

@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    pass

class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [ProductVariantImageInline]

@admin.register(Brand)
class CharacteristicAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductVariant, ProductVariantAdmin)