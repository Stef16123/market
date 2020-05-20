from django.urls import path
from .views import *


urlpatterns = [
    path('home/', home, name='home_url'),
    path('category/<str:slug>/', search_category, name='category_url'),
    path('home/<str:slug>/', product_detail , name='product_detail_url'),
    # path('home/basket/><str:id>', basket, name='basket_url'),
]
