from django.urls import path
from .views import *


urlpatterns = [
    path('home/', home, name='home_url'),
    path('category/<str:slug>/', search_category, name='category_url'),
    path('home/<str:slug>/', item_detail , name='item_detail_url'),
]
