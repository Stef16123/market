from django.contrib import admin

from .models import *
# from .forms import *

# Register your models here.

@admin.register(ItemModel)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'price' ,'image', 'get_category')


admin.site.register(CategoryModel)
# admin.site.register(Item, ItemAdmin)
