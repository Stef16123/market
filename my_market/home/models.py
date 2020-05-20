from django.db import models
from django.core.exceptions import ValidationError

from PIL import Image as img_p

# users/models.py
from users.models import CustomUser 
# Create your models here.

class CategoryModel(models.Model):
	title = models.CharField(max_length=70, unique=True)
	slug = models.SlugField(max_length=200, unique=True)

	def __str__(self):
		return self.title

	

# Основная информация о модели
class ProductModel(models.Model):
	product_id = models.AutoField(primary_key=True)
	article = models.IntegerField(unique=True)
	count_products = models.IntegerField(default=1)


	def __str__(self):
		return str(self.article)

# Описание модели
class ProductDescribeModel(models.Model):
	title = models.CharField(max_length=70)
	slug = models.SlugField(max_length=200, unique=True)
	price = models.IntegerField(default=0)
	image = models.ImageField(upload_to="images/", blank=True)
	body = models.TextField(max_length=1000)
	category = models.ManyToManyField(CategoryModel, related_name='item', blank=True)
	product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)


	def __str__(self):
		return self.title

# ф-я для того что бы показать список прикрепленных категорий  продукта в админ панеле
	def get_category(self):
		return "\n".join([c.title for c  in self.category.all()])

# Проверка загружаемой картинки на разрешение х на х, ограничение на загружаемые данные в settings.py
	def clean(self, *args, **kwargs):
		if self.image:
			im = img_p.open(self.image)
			if (im.size[0] <= 564) or (im.size[1] <= 564):
				super(ItemModel, self).save(*args, **kwargs)
			else:
				raise ValidationError('Недопустимое разрешение или размер картинки')
		else:
			super(Item, self).save(*args, **kwargs)

# Корзина, которая должна хранить id пользователя и номер товара
class BasketModel(models.Model):
	user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
	product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE, blank=True)