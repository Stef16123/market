from django.db import models
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse

# from django.shortcuts import reverse
#Библиотека для обработки изображений
from PIL import Image as img_p
# users/models.py
# Импорт пользовательского юзера
from users.models import CustomUser 

# Функции, которые невозможно отнести к конкретной модели здесь:

"""Получить пагинацию для товаров"""
def get_paginate(page_number, products):
	paginator = Paginator(products, 5)
	page_products = paginator.get_page(page_number)
	return paginator, page_products


# Create your models here.


"""Информация о категории"""
class CategoryModel(models.Model):
	title = models.CharField(max_length=70, unique=True)
	slug = models.SlugField(max_length=200, unique=True)

	def __str__(self):
		return self.title

	"""Поиск товаров по категории"""
	def search_by_category(self, slug, page_number, form):
		products_category = self.objects.get(slug__iexact=slug)
		products = products_category.product_describe.all()
		paginator, page_products = get_paginate(page_number, products)
		categoryes = self.objects.all()
		context = {
		'categoryes_list' : categoryes,
		'products' : page_products,
		'products_category' : products_category,
		'paginator' : paginator,
		'form' : form,
		}
		return context

	

"""Основная информация о модели"""
class ProductModel(models.Model):
	product_id = models.AutoField(primary_key=True)
	article = models.IntegerField(unique=True)
	count_products = models.IntegerField(default=0)


	def __str__(self):
		return str(self.article)

"""Описание модели"""
class ProductDescribeModel(models.Model):
	title = models.CharField(max_length=70)
	slug = models.SlugField(max_length=200, unique=True)
	price = models.IntegerField(default=0)
	image = models.ImageField(upload_to="images/", blank=True)
	body = models.TextField(max_length=1000)
	category = models.ManyToManyField(CategoryModel, related_name='product_describe', blank=True)
	product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
	pub_date =  models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title

# ф-я для того что бы показать список прикрепленных категорий  продукта в админ панеле
	def get_category(self):
		return "\n".join([c.title for c  in self.category.all()])

# Проверка загружаемой картинки на разрешение х на х, ограничение на загружаемые данные в settings.py (надо переделать!)
	def clean(self, *args, **kwargs):
		if self.image and img_p.open(self.image).size > (564,564):
				raise ValidationError('Недопустимое разрешение картинки')
		super(ProductDescribeModel, self).save(*args, **kwargs)

	"""Получить информацию о товаре"""
	def get_product(self,slug):
		describe = self.objects.get(slug__iexact=slug)
		product_id = describe.product.product_id
		context = {
		'product_describe': describe,
		'product_id' : product_id,
		}
		return context

	"""Поиск товара/ов"""
	# def search_products(self)






# Корзина, которая должна хранить id пользователя и номер товара
class BasketModel(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
	product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True)
	product_describe = models.ForeignKey(ProductDescribeModel, on_delete=models.CASCADE, blank=True, default=None)
	
# ф-я для получения в админ панеле имени пользователя
	def get_username(self):
		return self.user.username

	def __str__(self):
		return self.product_describe.title


	"""Вычисление суммы лежащих в корзине товаров"""
	def sum_basket(self, user):
		basket_list = self.objects.filter(user=user)
		sum_product = 0
		for product in basket_list:
			sum_product += product.product_describe.price
		context = {'basket_list' : basket_list, 'sum_product' : sum_product}
		return context

	"""Добавление товара в корзину"""
	def add_to_basket(self, slug, product_id, user):
		product = ProductModel.objects.get(product_id = product_id)
		describe = ProductDescribeModel.objects.get(product=product_id)

		# Надо переделать 
		if product.count_products > 0:
			user_basket = self.objects.create( user=user, product=product, product_describe=describe)
			
			product.count_products -= 1
			user_basket.save()
			product.save()
			return "Товар успешно добавлен в корзину"
		return "Товара нет на складе"

	def delete_basket(self,user_id):
		user_basket = BasketModel.objects.filter(user_id=user_id)
		user_basket.delete()


class OrderModel(models.Model):
	# order_number = models.IntegerField()
	phone_number = models.CharField(max_length=11)
	confirmation = models.BooleanField(default=False)
	user = models.CharField(max_length=70)
	# products_id = 
	# basket = models.ForeignKey(BasketModel, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)


	# def get_order_number(self):
	def get_order(self,request):
		if request.POST:
					
			phone_number = request.POST.get('phone')
			user = request.user.username
			user_id = request.user.id
			order  = self.objects.create( user=user, phone_number = phone_number)
			order.save()

			user_basket = BasketModel.objects.filter(user_id=user_id)

			for i in user_basket:
				products_order = ProductOrderModel.objects.create( product=i.product_id, order=order)
				products_order.save()

			user_basket.delete()
			return HttpResponse('Наши операторы уже занимаются подтверждением заказа, ожидайте звонка на ваш телефон')
		return HttpResponse('У нас технические шоколадки')

class ProductOrderModel(models.Model):
	# product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True)
	product = models.IntegerField(default=0)
	order =  models.ForeignKey(OrderModel, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return str(self.product)

	# def if_confirmate(self, order_id):
	# 	product_id = self.basket.product_id
	# 	order = self.objects.get(order_id) 
	# 	if 

# def add_to_basket(self, slug, product_id, user):
# 		describe = ProductDescribeModel.objects.get(product=product_id)
# 		# Надо переделать 
# 		if product.count_products > 0:
# 			user_basket = self.objects.create( user=user, product=product, product_describe=describe)
# 			product.count_products -= 1
# 			user_basket.save()
# 			product.save()
# 			return "Товар успешно добавлен в корзину"
# 		return "Товара нет на складе"
