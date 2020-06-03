from django.urls import path
from .views import *


urlpatterns = [
    path('home/', home, name='home_url'),
    path('home/basket/', get_basket, name='basket_url'),
    path('home/search/', search_products, name='search_url'),
    path('category/<str:slug>/', products_by_category, name='category_url'),
    # path('category/<str:slug>/search/', search_by_category, name='category_url'),

    path('home/<str:slug>/', product_detail , name='product_detail_url'),
    path('home/<str:slug>/add_basket/<str:product_id>/', get_message, name='add_basket_url'),
   
]
