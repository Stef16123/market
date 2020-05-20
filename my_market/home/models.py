from django.db import models
from django.core.exceptions import ValidationError

from PIL import Image as img_p

# Create your models here.

class CategoryModel(models.Model):
	title = models.CharField(max_length=70, unique=True)
	slug = models.SlugField(max_length=200, unique=True)

	def __str__(self):
		return self.title

	
class ItemModel(models.Model):
	title = models.CharField(max_length=70)
	slug = models.SlugField(max_length=200, unique=True)
	price = models.IntegerField(default=0)
	image = models.ImageField(upload_to="images/", blank=True)
	body = models.TextField(max_length=1000)
	category = models.ManyToManyField(CategoryModel, related_name='item', blank=True)

	def __str__(self):
		return self.title

	def get_category(self):
		return "\n".join([c.title for c  in self.category.all()])

	def clean(self, *args, **kwargs):
		if self.image:
			im = img_p.open(self.image)
			if (im.size[0] <= 564) or (im.size[1] <= 564):
				super(ItemModel, self).save(*args, **kwargs)
			else:
				raise ValidationError('Недопустимое разрешение или размер картинки')
		else:
			super(Item, self).save(*args, **kwargs)


