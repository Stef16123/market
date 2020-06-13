from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils.http import is_safe_url, urlunquote
from django.http import HttpResponseRedirect


from users.models import CustomUser
from .models import CategoryModel, ProductDescribeModel,  BasketModel, ProductModel, get_paginate, OrderModel, ProductOrderModel, MarkModel,RatingModel
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

		if request.GET.get('maxrating'):
			products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-rating__rating')
		else:
			products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-pub_date')

		if request.GET.get('stock'):
			products = products.filter(product__count_products__gt=0)
			
		paginator, page_products = get_paginate(page_number,products)
		context = {
		'categoryes_list' : categoryes,
		'products' : page_products,
		'paginator' : paginator,
		'form' : form,
		}
		context['last_question'] = '?csrfmiddlewaretoken=%s&from_money=%s&up_to_money=%s&title=%s&stock=%s&maxrating=%s&' % (
			request.GET.get('csrfmiddlewaretoken'), 
			request.GET.get('from_money'),  
			request.GET.get('up_to_money'), 
			request.GET.get('title'),
			request.GET.get('stock'),
			request.GET.get('maxrating'))

		return render(request, 'home/index.html', context)

"""Домашняя страница"""
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
	form = SearchProductsForm(request.GET)
	page_number = request.GET.get('page')
	context = CategoryModel.list_by_category(CategoryModel, slug, page_number, form)
	# context['last_question'] = 'category/%s' % (context['products_category'].slug)
	context['last_question'] = '?'
	return render(request, 'home/category.html', context)

def search_by_category(request,slug):
	categoryes = CategoryModel.objects.all()
	products_category = CategoryModel.objects.get(slug__iexact=slug)
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
		# response.GET.get('products_category')
		products = ProductDescribeModel.objects.filter(title__icontains=title, category__slug=slug).filter(price__gte=from_money, price__lte=up_to_money).order_by('-pub_date')

		# if request.GET.get('maxrating'):
		# 	products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-rating__rating')
		# else:
		# 	products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-pub_date')

		if request.GET.get('popular'):
			products = ProductDescribeModel.objects.filter(title__icontains=title, category__slug=slug, popular__gt=0).filter(price__gte=from_money, price__lte=up_to_money).order_by('-popular')

		if request.GET.get('maxrating'):
			products = products.order_by('-rating__rating')

		paginator, page_products = get_paginate(page_number,products)
		context = {
		'categoryes_list' : categoryes,
		'products' : page_products,
		'paginator' : paginator,
		'form' : form,
		'products_category' : products_category,
		}
		context['last_question'] = '?csrfmiddlewaretoken=%s&from_money=%s&up_to_money=%s&title=%s&popular=%s&maxrating=%s&' % (
			request.GET.get('csrfmiddlewaretoken'), 
			request.GET.get('from_money'),  
			request.GET.get('up_to_money'), 
			request.GET.get('title'),
			request.GET.get('popular'),
			request.GET.get('maxrating')
			)
		return render(request, 'home/category.html', context)

"""Страница  с подробностями о товаре"""
def product_detail(request, slug):
	context = ProductDescribeModel.get_product(ProductDescribeModel,slug)
	referer = request.headers['Referer']
	context['referer'] = referer
	# if request.GET.get('last_question'):
	# context['last_question'] = last_question


	return render(request, 'home/product_detail.html', context)

def product_mark(request,slug):
	old_mark = False
	mark = int(request.POST.get('rating'))
	if request.session.get(slug, False):
		old_mark = request.session[slug]
	request.session[slug] = mark
	MarkModel.create_or_update_mark(MarkModel, slug, mark, old_mark)
	RatingModel.change_rating(RatingModel, slug)
	return redirect('/home/%s' % (slug))



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

"""Очистка корзины"""
def clear_basket(request):
	user_id = request.user.id
	BasketModel.delete_basket(BasketModel,user_id)
	return redirect('basket_url')


# def back(request):
# 	back = request.META.get('HTTP_REFERER')
# 	if back:
# 		back = urlunquote(back) # Раскодировка
# 	if not is_safe_url(url=back, allowed_hosts=request.get_host()):
# 		back = 'home/'
# 	return HttpResponseRedirect(back)

def test(request):
	ser_mark = UserMarkModel.objects.filter(token='233333').first() # Костыль
	return HttpResponse(ser_mark) 



# def back(request, slug):
# 	referer = request.META.get("HTTP_REFERER")
# 	# check that next is safe
# 	if not is_safe_url(referer,  allowed_hosts=request.get_host()):
# 		referer = 'home/'
# 	return redirect(referer)

def back(request, last_question):
	# context = {}
	# context['last_question'] = '?'

	# if request.GET.get('csrfmiddlewaretoken'):
	# 	context['last_question'] += 'csrfmiddlewaretoken=%s' % (request.GET.get('csrfmiddlewaretoken'))
	# if request.GET.get('from_money'):
	# 	context['last_question'] += 'from_money=%s' % (request.GET.get('from_money'))
	# if request.GET.get('up_to_money'):
	# 	context['last_question'] += 'up_to_money=%s' % (request.GET.get('up_to_money'))
	# if request.GET.get('title'):
	# 	context['last_question'] += 'title=%s' % (request.GET.get('title'))
	# if request.GET.get('popular'):
	# 	context['last_question'] += 'popular=%s' % (request.GET.get('popular'))
	# if request.GET.get('stock'):
	# 	context['last_question'] += 'stock=%s' % (request.GET.get('stock'))
	# if request.GET.get('maxrating'):
	# 	context['last_question'] += 'maxrating=%s' % (request.GET.get('maxrating'))
	# context['last_question'] += '&'
	# if request.GET.get('page'):
		# last_question += 'page=%s' % (request.GET.get('page'))
	# return redirect(last_question)
	# return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	# referer = request.headers['Referer']
	return redirect(last_question)
	# context['last_question'] = '?csrfmiddlewaretoken=%s&from_money=%s&up_to_money=%s&title=%s&popular=%s&maxrating=%s&' % (
	# 		request.GET.get('csrfmiddlewaretoken'), 
	# 		request.GET.get('from_money'),  
	# 		request.GET.get('up_to_money'), 
	# 		request.GET.get('title'),
	# 		request.GET.get('popular'),
	# 		request.GET.get('maxrating')
	# 		)request.GET.get('stock'),

	# {{last_question}}page={{products.previous_page_number}}