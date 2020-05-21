from django.shortcuts import render
from django.http import HttpResponse

from users.models import CustomUser
from .models import CategoryModel, ProductDescribeModel,  BasketModel, ProductModel

# Create your views here.



def home(request):
	categoryes = CategoryModel.objects.all()
	products = ProductDescribeModel.objects.all()
	context = {
	'categoryes_list' : categoryes,
	'products' : products,
	}
	return render(request, 'home/index.html', context)

def search_category(request, slug):
	srch_cat = CategoryModel.objects.get(slug__iexact=slug)
	products = srch_cat.item.all()
	categoryes = CategoryModel.objects.all()
	context = {
	'categoryes_list' : categoryes,
	'products' : products,
	'srch_cat' : srch_cat,
	}
	return render(request, 'home/index.html', context)


def product_detail(request, slug):
	product_detail = ProductDescribeModel.objects.get(slug__iexact=slug)
	product_id = product_detail.product.product_id
	context = {
	'product_describe': product_detail,
	'product_id' : product_id,
	}
	return render(request, 'home/product_detail.html', context)

def add_basket(request, slug, prd_id):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		product = ProductModel.objects.get(product_id = prd_id)
		describe = ProductDescribeModel.objects.get(product=prd_id)
		user_basket = BasketModel.objects.create( user=user, product=product, product_describe=describe)
		if product.count_products > 0:
			product.count_products = product.count_products - 1
			user_basket.save()
			product.save()
			return HttpResponse("Товар успешно добавлен в корзину")
		else:
			return HttpResponse("Товара нет на складе")# надо добавить валид еррор
	else:
		return HttpResponse("Прежде чем добавить товар в корзину, войдите в свою учетную запись")# надо добавить валид еррор

def basket(request):
	if request.user.id:
		user = CustomUser.objects.get(id = request.user.id)
		basket_list = BasketModel.objects.filter(user=user)

		sum_p = 0
		for prod in basket_list:
			sum_p += prod.product_describe.price

		context = {'basket_list' : basket_list, 'sum_p' : sum_p}
		return render(request, 'home/basket.html', context)
	else:
		return HttpResponse("Войдите в свою учетную запись")