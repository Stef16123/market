from django.contrib import admin

from .models import *
# Register your models here.

class RatingInLines(admin.StackedInline):
	model = RatingModel


@admin.register(ProductDescribeModel)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'price' ,'image', 'get_category')
	inlines = [RatingInLines,]


@admin.register(BasketModel)
class BasketAdmin(admin.ModelAdmin):
	list_display = ('get_username', '__str__', 'id', )
	list_filter = ('product_describe__title', 'user')


@admin.register(ProductModel)
class ProductModel(admin.ModelAdmin):
	list_display = ('product_id', 'article')

@admin.register(OrderModel)
class OrderModel(admin.ModelAdmin):
	list_display = ('id', 'user', 'confirmation')
	list_filter = ('user', 'confirmation')

@admin.register(ProductOrderModel)
class ProductOrderModel(admin.ModelAdmin):
	list_display = ('product', 'order')

# admin.site.register(OrderModel)
admin.site.register(CategoryModel)
admin.site.register(RatingModel)
admin.site.register(MarkModel)

# admin.site.register(ProductModel)
# admin.site.register(ProductOrderModel)


 
