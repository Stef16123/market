from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect

from users.models import CustomUser
from .models import CategoryModel, ProductDescribeModel,  BasketModel, ProductModel, get_paginate, OrderModel
from .forms import SearchProductsForm

"""Поиск товаров"""
def search_products(request):
	categoryes = CategoryModel.objects.all()
	page_number = request.GET.get('page',1)
	form = SearchProductsForm(request.GET)
	if form.is_valid():
		title = request.GET.get('title')
		from_money = request.GET.get('from_money')
		if from_money == '':
			from_money = 0
		up_to_money = request.GET.get('up_to_money')
		if up_to_money == '':
			up_to_money = 9999999
		

		products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-pub_date')
		paginator, page_products = get_paginate(page_number,products)
		context = {
		'categoryes_list' : categoryes,
		'products' : page_products,
		'paginator' : paginator,
		'form' : form,
		}
		context['last_question'] = '?csrfmiddlewaretoken=%s&from_money=%s&up_to_money=%s&title=%s&' % (
			request.GET.get('csrfmiddlewaretoken'), 
			request.GET.get('from_money'),  
			request.GET.get('up_to_money'), 
			request.GET.get('title'))

		return render(request, 'home/index.html', context)


def home(request):
	products = ProductDescribeModel.objects.all()
	form = SearchProductsForm() 
	categoryes = CategoryModel.objects.all()
	page_number = request.GET.get('page',1)
	paginator, page_products = get_paginate(page_number,products)
	context = {
	'categoryes_list' : categoryes,
	'products' : page_products,
	'paginator' : paginator,
	'form' : form,
	}
	context['last_question'] = '?'

	return render(request, 'home/index.html', context)




"""Товары по каталогу""" 
def products_by_category(request, slug):
	#Сделать поиск
	form = SearchProductsForm(request.GET)
	page_number = request.GET.get('page')
	context = CategoryModel.search_by_category(CategoryModel, slug, page_number, form)
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

"""Отображение формы для ввода номера телефона"""
def phone_for_order(request):
	return render(request, 'home/order.html')

"""Оформление заказа заказа"""
def products_on_order(request):
	return OrderModel.get_order(OrderModel, request)

def clear_basket(request):
	user_id = request.user.id
	BasketModel.delete_basket(BasketModel,user_id)
	return redirect('basket_url')