from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils.http import is_safe_url, urlunquote
from django.http import HttpResponseRedirect

from django.core.exceptions import ValidationError

from users.models import CustomUser
from .models import CategoryModel, ProductDescribeModel,  ProductBasketModel, ProductModel, get_paginate, OrderModel, ProductOrderModel, MarkModel,RatingModel, CouponModel
from .forms import SearchProductsForm, CouponForm, OrderForm


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

		if request.GET.get('maxrating') == 'on':
			products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-rating__rating')
		else:
			products = ProductDescribeModel.objects.filter(title__icontains=title).filter(price__gte=from_money, price__lte=up_to_money).order_by('-pub_date')

		if request.GET.get('stock') == 'on':
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
		
		context['count_to_order'] = 1

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
	'count_to_order' : 1,
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
	context['count_to_order'] = 1
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
		products = ProductDescribeModel.objects.filter(title__icontains=title, category__slug=slug).filter(price__gte=from_money, price__lte=up_to_money).order_by('-pub_date')
		if request.GET.get('popular') == 'on':
			products = ProductDescribeModel.objects.filter(title__icontains=title, category__slug=slug, popular__gt=0).filter(price__gte=from_money, price__lte=up_to_money).order_by('-popular')

		if request.GET.get('maxrating') == 'on':
			products = products.order_by('-rating__rating')

		paginator, page_products = get_paginate(page_number,products)
		context = {
		'categoryes_list' : categoryes,
		'products' : page_products,
		'paginator' : paginator,
		'form' : form,
		'products_category' : products_category,
		'count_to_order' : 1,
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
	products_on_stock = context['product_describe'].product.count_products
	count_to_order = get_count(request, slug, products_on_stock)
	context['count_to_order'] = count_to_order
	# last_question = question



	# if request.GET.get('last_question'):
	# context['last_question'] = last_question
	# return HttpResponse(request.session['product_info'][slug])
	return render(request, 'home/product_detail.html', context)

def product_mark(request,slug):
	old_mark = False
	mark = request.POST.get('rating', False)
	if mark:
		mark = int(mark)
		if request.session.get(slug, False):
			old_mark = request.session[slug]
		request.session[slug] = mark
		MarkModel.create_or_update_mark(MarkModel, slug, mark, old_mark)
		RatingModel.change_rating(RatingModel, slug)
	return redirect('/home/%s' % (slug))



"""добавление товара и вывод сообщения после добавления в корзину"""
def get_message(request, slug, product_id, count_to_order):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		return HttpResponse(ProductBasketModel.add_to_basket(ProductBasketModel, slug, request, product_id, user, int(count_to_order)))
	return HttpResponse("Прежде чем добавить товар в корзину, войдите в свою учетную запись")# надо добавить валид еррор

"""Отобразить корзину"""
def get_basket(request,coupon=1):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		if request.session.get('coupon_value', False):
			coupon = request.session.get('coupon_value')
		# 	coupon = request.POST.get('coupon')
		# else:
		# 	coupon = 1
		context = ProductBasketModel.sum_basket(ProductBasketModel,user, coupon)
		request.session['sum_product'] = context['sum_product']
		return render(request, 'home/basket.html', context)
	return HttpResponse("Войдите в свою учетную запись")

"""Отображение формы для ввода номера телефона"""
def phone_for_order(request):
	form = OrderForm()
	# sum_product = request.POST.get('sum', False)
	sum_product = request.session['sum_product']
	context = { 'form' : form, 'sum_product' : sum_product}
	return render(request, 'home/order.html', context)

"""Оформление заказа заказа"""
def products_on_order(request):
	if request.POST.get('condition')  == 'on':
		return OrderModel.get_order(OrderModel, request)
	raise ValidationError('Заполните все формы и подвердите заказ')

"""Очистка корзины"""
def clear_basket(request):
	user_id = request.user.id
	ProductBasketModel.delete_basket(ProductBasketModel,user_id)
	return redirect('basket_url')

"""Убрать позицию с корзины"""
def delete_product_basket(request,slug):
	if request.user.id:
		user_id = request.user.id
		ProductBasketModel.delete_product(ProductBasketModel, user_id, slug)
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


def change_count_basket(request, slug):
	user = CustomUser.objects.get(id = request.user.id)
	user_basket = ProductBasketModel.objects.get(user=user, product_describe__slug__iexact=slug)
	if request.POST.get('minus', False) == '0':
		if user_basket.count > 1:
			user_basket.count -= 1
			user_basket.save()
	if request.POST.get('plus', False) == '1':
		if user_basket.count < user_basket.product.count_products:
			user_basket.count += 1
			user_basket.save()
	return redirect('basket_url')
# def back(request, slug):
# 	referer = request.META.get("HTTP_REFERER")
# 	# check that next is safe
# 	if not is_safe_url(referer,  allowed_hosts=request.get_host()):
# 		referer = 'home/'
# 	return redirect(referer)

def back_url(request):
	if request.GET.get('back', False):
		return redirect(request.GET.get('back'))
	return HttpResponse('SUKABLYAT')


def get_count(request, slug, products_on_stock):
	if not request.session.get('product_info'):

		request.session['product_info'] = { slug : 1 }
	if not slug in request.session.get('product_info'):
		key = { slug : 1 }
		# product_info = { slug : count_to_order }
		request.session['product_info'].update(key)
		# request.session['product_info'][slug] = 0

		# request.session['count_to_order'] = 0
	if request.POST.get('minus', False) == '0':
		if request.session.get('product_info')[slug] > 1:
			request.session['product_info'][slug] -= 1
			request.session.save()
	if request.POST.get('plus', False) == '1':
		if request.session['product_info'][slug] < products_on_stock:
			request.session['product_info'][slug] += 1
			request.session.save()
	return request.session['product_info'][slug]


def get_coupon_form(request):
	form = CouponForm()
	context = {'form' : form}
	return render(request, 'home/basket_coupon.html', context)

def check_coupon(request):
	if request.POST.get('name'):
		coupon_name = request.POST.get('name')
		# status_coupon = is_coupon(coupon)
		if CouponModel.is_coupon(CouponModel,coupon_name):
			coupon = CouponModel.is_coupon(CouponModel,coupon_name)
			request.session['coupon_value'] = coupon.value
			request.session.save()
			# coupon =  int(coupon)
			return redirect('basket_url')
			# return get_basket(request, coupon.value)
		return HttpResponse('Неккоректный купон')
	return HttpResponse('Вы не ввели купон')

