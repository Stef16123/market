from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from users.models import CustomUser
from .models import CategoryModel, ProductDescribeModel,  BasketModel, ProductModel, get_paginate


def home(request):
	categoryes = CategoryModel.objects.all()
	products = ProductDescribeModel.objects.all()
	page_number = request.GET.get('page',1)
	paginator, page_products = get_paginate(page_number,products)
	context = {
	'categoryes_list' : categoryes,
	'products' : page_products,
	'paginator' : paginator,
	}
	return render(request, 'home/index.html', context)


"""Товары по каталогу""" 
def products_by_category(request, slug):
	page_number = request.GET.get('page')
	context = CategoryModel.search_by_category(CategoryModel, slug, page_number)
	return render(request, 'home/index.html', context)

"""Страница  с подробностями о товаре"""
def product_detail(request, slug):
	context = ProductDescribeModel.get_product(ProductDescribeModel,slug)
	return render(request, 'home/product_detail.html', context)

"""добавление товара и вывод сообщения после добавления в корзину"""
def get_message(request, slug, product_id):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		return HttpResponse(BasketModel.add_to_basket(BasketModel,slug, product_id, user))
	return HttpResponse("Прежде чем добавить товар в корзину, войдите в свою учетную запись")# надо добавить валид еррор

"""Отобразить корзину"""
def get_basket(request):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		context = BasketModel.sum_basket(BasketModel,user)
		return render(request, 'home/basket.html', context)
	return HttpResponse("Войдите в свою учетную запись")