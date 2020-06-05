from django.urls import path
from .views import *


urlpatterns = [
    path('test/', test, name='test_url'),
    path('home/', home, name='home_url'),
    path('home/basket/', get_basket, name='basket_url'),
    path('home/basket/clear', clear_basket, name='clear_basket_url'),

    path('home/basket/phone-for-order', phone_for_order, name='phone_for_order_url'),
     path('home/basket/phone-for-order/order', products_on_order, name='products_on_order_url'), 
    path('home/search/', search_products, name='search_url'),
    path('category/<str:slug>/', products_by_category, name='category_url'),
    # path('category/<str:slug>/search/', search_by_category, name='category_url'),

    path('home/<str:slug>/', product_detail , name='product_detail_url'),
    path('home/<str:slug>/add_basket/<str:product_id>/', get_message, name='add_basket_url'),
    
]
