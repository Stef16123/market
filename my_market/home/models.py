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
from django.db.models import Q

# Функции, которые невозможно отнести к конкретной модели здесь:

"""Получить пагинацию для товаров"""
def get_paginate(page_number, products):
	paginator = Paginator(products, 2)
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
	def list_by_category(self, slug, page_number, form):
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

	

"""Основная информация о товаре"""
class ProductModel(models.Model):
	product_id = models.AutoField(primary_key=True)
	article = models.IntegerField(unique=True)
	count_products = models.IntegerField(default=0)


	def __str__(self):
		return str(self.article)

"""Описание товара"""
class ProductDescribeModel(models.Model):
	title = models.CharField(max_length=70)
	slug = models.SlugField(max_length=200, unique=True)
	price = models.IntegerField(default=0)
	image = models.ImageField(upload_to="images/", blank=True)
	body = models.TextField(max_length=1000)
	category = models.ManyToManyField(CategoryModel, related_name='product_describe', blank=True)
	product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
	pub_date =  models.DateField(auto_now_add=True)
	popular = models.IntegerField(default=0)
	# tmp_count = models.IntegerField(default=1)


	def __str__(self):
		return self.title

# ф-я для того что бы показать список прикрепленных категорий  продукта в админ панеле
	def get_category(self):
		return "\n".join([c.title for c  in self.category.all()])

# Проверка загружаемой картинки на разрешение х на х, ограничение на загружаемые данные в settings.py (надо переделать!)
	# def clean(self, *args, **kwargs):
	# 	if self.image and img_p.open(self.image).size > (564,564):
	# 			raise ValidationError('Недопустимое разрешение картинки')
	# 	super(ProductDescribeModel, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		# custom_clean()
		if self.image and img_p.open(self.image).size > (564,564):
				raise ValidationError('Недопустимое разрешение картинки')
		self.full_clean()
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

	# def if_popular(self):
	# 	ProductBasketModel.objects.all()
	# 	ProductBasketModel.objects.get()
	# 	if product_describe

	# def get_back(self,request):
	# 	referer = request.META.get("HTTP_REFERER")
	# # check that next is safe
	# 	if not is_safe_url(referer,  allowed_hosts=request.get_host()):
	# 		referer = 'home/'
	# 	return redirect(referer)



"""Рейтинг товара"""
class RatingModel(models.Model):
	product = models.OneToOneField(ProductDescribeModel, on_delete=models.CASCADE, related_name="rating")
	rating = models.IntegerField()
	voites = models.IntegerField(default=1)

	
	def change_rating(self, slug):
		product = ProductDescribeModel.objects.get(slug__iexact=slug)
		rating = RatingModel.objects.get(product__slug__iexact=slug)
		voites = RatingModel.objects.filter(mark__product=product).count()
		rating.voites = voites
		rating.rating = (MarkModel.sum_marks(MarkModel,slug))/rating.voites

		# raiting = RatingModel.objects.create(product=)
		rating.save()

	def __str__(self):
		return str(self.product)




"""Модель оценки товара пользователм"""
class MarkModel(models.Model):
	mark = models.IntegerField(default=0)
	# token = models.CharField(max_length=250)
	product = models.ForeignKey(ProductDescribeModel, on_delete=models.CASCADE)
	rating = models.ForeignKey(RatingModel, on_delete=models.CASCADE, related_name="mark")



	def create_or_update_mark(self, slug, mark, old_mark):
		product = ProductDescribeModel.objects.get(slug__iexact=slug)
		rating = RatingModel.objects.get(product=product)
		if old_mark:
			mark_tmp = MarkModel.objects.filter(product__slug__iexact=slug, mark=old_mark).first()
			mark_tmp = MarkModel.objects.filter(mark=old_mark).first()
			print(f' Вотафак {old_mark}')

			print(f' Вотафак {mark_tmp}')
			# mark_tmp.mark = mark
			# mark_tmp.save()
			mark_tmp.delete()
		# else:
		mark_tmp =  MarkModel.objects.create(mark=mark, product=product, rating=rating)
		mark_tmp.save()



	def sum_marks(self, slug):
		marks = MarkModel.objects.filter(product__slug__iexact=slug)
		sum_marks = 0
		for mark in marks:
			sum_marks += mark.mark
		print(f' марка {marks}')
		print(f' марка {sum_marks}')
		
		return sum_marks



	def __str__(self):
		return str(self.product)



class BasketModel(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
	sum_in_basket =  models.IntegerField(default=0)

"""Корзина"""
class ProductBasketModel(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
	product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True)
	product_describe = models.ForeignKey(ProductDescribeModel, on_delete=models.CASCADE, blank=True, default=None)
	count = models.IntegerField(default=1)
	product_basket = models.ForeignKey(BasketModel, on_delete=models.CASCADE, blank=True) 
	# cost = models.IntegerField(default=1)

# ф-я для получения в админ панеле имени пользователя
	def get_username(self):
		return self.user.username

	def __str__(self):
		return self.product_describe.title


	"""Вычисление суммы лежащих в корзине товаров"""
	def sum_basket(self, user, coupon):
		basket_list = self.objects.filter(user=user)
		basket = BasketModel.objects.filter(user=user).first()
		sum_product = 0
		if basket:
			# basket = BasketModel.objects.get(user=user)
			for product in basket_list:
				sum_product += product.product_describe.price * product.count * coupon
			basket.sum_in_basket = sum_product
			basket.save()
		context = {'basket_list' : basket_list, 'sum_product' : sum_product}
		return context

	"""Добавление товара в корзину"""
	def add_to_basket(self, request, slug, product_id, user, count_to_order):
		product = ProductModel.objects.get(product_id = product_id)
		describe = ProductDescribeModel.objects.get(product=product_id)
		# if self.objects.filter(user=user, product_describe__slug__iexact=slug).first():
		if self.objects.filter(user=user, product_id=product_id).first():

			user_basket = self.objects.filter(user=user, product_id=product_id).first()
			# update_sum = self.sum_basket(self, user, 1)
			# request.session['sum_product'] = context['sum_product']
			# raise ValidationError(type(count_to_order))
			# user_basket.count = 
			# tmp_count = abs(count_to_order - user_basket.count) 
			user_basket.count = count_to_order
			user_basket.save()
			# if request.session.get('coupon_value', False):
			# 	user_basket.product_basket.sum_in_basket += describe.price * tmp_count * request.session.get('coupon_value')
			# else:
			# 	user_basket.product_basket.sum_in_basket += describe.price * tmp_count 
		else:
			print(self.objects.filter(user=user, product_id=product_id))
			# print(f'юзер {user}, {product_id}')
			basket = BasketModel.objects.create( user=user)
			basket.save()
			user_basket = self.objects.create( user=user, product=product, product_describe=describe, count=count_to_order, product_basket=basket )
			user_basket.save()
			
		describe.popular += 1
		describe.save()
		return "Товар успешно добавлен в корзину"

	def delete_basket(self,user_id):
		user_baskets = self.objects.filter(user_id=user_id)
		basket = BasketModel.objects.filter(user_id=user_id)
		for user_basket in user_baskets:
			user_basket.product_describe.popular -= 1
			user_basket.product_describe.save()
		user_baskets.delete()
		basket.delete()

	def delete_product(self, user_id, slug):
		user_baskets = self.objects.get(user_id=user_id, product_describe__slug__iexact=slug)
		user_baskets.delete()




"""Модель, описывающая заказ"""
class OrderModel(models.Model):
	phone_number = models.CharField(max_length=11)
	confirmation = models.BooleanField(default=False)
	user = models.CharField(max_length=70)
	first_name = models.CharField(max_length=100, default='')
	last_name = models.CharField(max_length=100, default='')
	surname = models.CharField(max_length=100, default='')
	adress = models.CharField(max_length=200, default='')
	cost = models.IntegerField(default=0)


	def __str__(self):
		return str(self.id)

	def save(self, *args, **kwargs):
		if self.confirmation == True:
			ProductOrderModel.change_count(ProductOrderModel,self.id)
		super(OrderModel, self).save(*args, **kwargs)

	"""Создание заказа"""
	def get_order(self,request):
		if request.POST:
			phone_number = request.POST.get('phone_number')
			first_name = request.POST.get('first_name')
			last_name = request.POST.get('last_name')
			surname = request.POST.get('surname')
			adress = request.POST.get('adress')
			cost = request.session['sum_product']
			user = request.user.username
			user_id = request.user.id
			order  = self.objects.create( user=user, phone_number = phone_number,first_name=first_name,last_name=last_name, surname=surname , adress=adress, cost=cost  )
			order.save()
			user_basket = ProductBasketModel.objects.filter(user_id=user_id)
			for i in user_basket:
				product = i.product
				products_order = ProductOrderModel.objects.create( product=product, order=order)
				products_order.save()
			user_basket.delete()
			return HttpResponse('Наши операторы уже занимаются подтверждением заказа, ожидайте звонка на ваш телефон')
		return HttpResponse('У нас технические шоколадки')



"""Модель описывающая товар на который оформлен заказ"""
class ProductOrderModel(models.Model):
	product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True, related_name='product_order')
	order =  models.ForeignKey(OrderModel, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return str(self.product)

	"""Изменение колличества товара на складе при подтверждении заказа"""
	def change_count(self, order_id):
		order_id = OrderModel.objects.get(id=order_id)
		products = ProductModel.objects.filter(product_order__order=order_id)
		count =  ProductModel.objects.filter(product_order__order=order_id).count()
		for i in range(0,count):
			product = ProductModel.objects.filter(product_order__order=order_id)[i]
			product.count_products -= 1
			product.save()


class CouponModel(models.Model):
	name = models.CharField(max_length=100)
	value = models.FloatField(default=1)
	active = models.BooleanField(default=True)

	def is_coupon(self, name):
		coupon = self.objects.filter(name=name).first()
		if coupon:
			if coupon.active:
				return coupon
			# return False
		return False



