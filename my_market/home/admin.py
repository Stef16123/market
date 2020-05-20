from django.contrib import admin

from .models import *
# from .forms import *

# Register your models here.

@admin.register(ProductDescribeModel)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'price' ,'image', 'get_category')


admin.site.register(CategoryModel)

admin.site.register(ProductModel)
admin.site.register(BasketModel)
