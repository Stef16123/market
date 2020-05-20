from django.shortcuts import render

from .models import CategoryModel, ItemModel

# Create your views here.



def home(request):
	categoryes = CategoryModel.objects.all()
	items = ItemModel.objects.all()
	context = {
	'categoryes_list' : categoryes,
	'items_list' : items,
	}
	return render(request, 'home/index.html', context)

def search_category(request, slug):
	srch_cat = CategoryModel.objects.get(slug__iexact=slug)
	items = srch_cat.item.all()
	categoryes = CategoryModel.objects.all()
	context = {
	'categoryes_list' : categoryes,
	'items_list' : items,
	'srch_cat' : srch_cat,
	}
	return render(request, 'home/index.html', context)


def item_detail(request, slug):
	item_detail = ItemModel.objects.get(slug__iexact=slug)
	context = {'item': item_detail}
	return render(request, 'home/item_detail.html', context)
