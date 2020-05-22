from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(ProductDescribeModel)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'price' ,'image', 'get_category')


@admin.register(BasketModel)
class BasketAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'get_username')
	list_filter = ('product_describe__title',)
 
admin.site.register(CategoryModel)
admin.site.register(ProductModel)

 
