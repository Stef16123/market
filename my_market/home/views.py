from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from users.models import CustomUser
from .models import CategoryModel, ProductDescribeModel,  BasketModel, ProductModel

# Create your views here.


"""Отрисовка домашней страницы (список категорий, товаров)"""
def home(request):
	categoryes = CategoryModel.objects.all()
	products = ProductDescribeModel.objects.all()
	paginator = Paginator(products, 1)
	page_number = request.GET.get('page')
	page_products = paginator.get_page(page_number)

	context = {
	'categoryes_list' : categoryes,
	'products' : page_products,
	'paginator' : paginator,
	}
	return render(request, 'home/index.html', context)

"""Поиск товаров по каталогу""" 
def products_by_category(request, slug):
	products_category = CategoryModel.objects.get(slug__iexact=slug)
	products = products_category.product_describe.all()
	paginator = Paginator(products, 1)
	page_number = request.GET.get('page')
	page_products = paginator.get_page(page_number)
	categoryes = CategoryModel.objects.all()
	context = {
	'categoryes_list' : categoryes,
	'products' : page_products,
	'products_category' : products_category,
	}
	return render(request, 'home/index.html', context)

"""Страница  с подробностями о товаре"""
def product_detail(request, slug):
	describe = ProductDescribeModel.objects.get(slug__iexact=slug)
	product_id = describe.product.product_id
	context = {
	'product_describe': describe,
	'product_id' : product_id,
	}
	return render(request, 'home/product_detail.html', context)

"""ф-я добавляет товар в корзину, проверяет юзера и товар"""
def add_basket(request, slug, product_id):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		product = ProductModel.objects.get(product_id = product_id)
		describe = ProductDescribeModel.objects.get(product=product_id)
		user_basket = BasketModel.objects.create( user=user, product=product, product_describe=describe)
		# Надо переделать
		if product.count_products > 0:
			product.count_products -= 1
			user_basket.save()
			product.save()
			return HttpResponse("Товар успешно добавлен в корзину")
		return HttpResponse("Товара нет на складе")# надо добавить валид еррор
	return HttpResponse("Прежде чем добавить товар в корзину, войдите в свою учетную запись")# надо добавить валид еррор

"""Страница с корзиной"""
def basket(request):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		basket_list = BasketModel.objects.filter(user=user)
		sum_product = 0
		for product in basket_list:
			sum_product += product.product_describe.price
		context = {'basket_list' : basket_list, 'sum_product' : sum_product}
		return render(request, 'home/basket.html', context)
	return HttpResponse("Войдите в свою учетную запись")