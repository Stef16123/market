from django.shortcuts import render

from .models import CategoryModel, ProductDescribeModel

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
	context = {'product': product_detail}
	return render(request, 'home/product_detail.html', context)

def basket(request):
	pass