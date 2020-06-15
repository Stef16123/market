from django.urls import path
from .views import *


urlpatterns = [
    path('test/', test, name='test_url'),
    path('home/', home, name='home_url'),
    path('home/basket/', get_basket, name='basket_url'),
    path('home/basket/clear', clear_basket, name='clear_basket_url'),
    path('home/basket/coupon', get_coupon_form, name='get_coupon_form_url'),
    path('home/basket/coupon/check', check_coupon, name='check_coupon_url'),

    path('home/basket/delete/<str:slug>/', delete_product_basket, name='delete_product_basket_url'),
    path('home/basket/change_count_basket/<str:slug>/', change_count_basket, name='change_count_basket_url'),

    
    path('home/basket/phone-for-order', phone_for_order, name='phone_for_order_url'),
     path('home/basket/phone-for-order/order', products_on_order, name='products_on_order_url'), 

    path('home/search/', search_products, name='search_url'),
    path('category/<str:slug>/', products_by_category, name='products_by_category_url'),
    path('category/<str:slug>/search/', search_by_category, name='search_by_category_url'),
    path('home/back/', back_url , name='back_url'),   
     
    path('home/count', get_count, name='get_count_url'),

    path('home/<str:slug>/', product_detail , name='product_detail_url'),


    path('home/<str:slug>/changemark', product_mark , name='product_mark_url'),

    path('home/<str:slug>/add_basket/<str:product_id>/<str:count_to_order>', get_message, name='add_basket_url'),
    
]
