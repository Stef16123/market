# from django import forms

# from .models import Item
# from PIL import Image as img_p

# class ItemForm(forms.ModelForm):
# 	class Meta:
# 		model = Item
# 		fields = ['title', 'slug', 'price', 'image', 'body', 'category']

# 	def clean(self):
# 		if Item.image:
# 			im = img_p.open(self.image)
# 			if (im.size[0] <= 500) or (im.size[1] <= 500):
# 				super(Item, self).save(*args, **kwargs)
# 			else:
# 				raise forms.ValidationError('Недопустимое разрешение или размер картинки')
# 		else:
# 			super(Item, self).save(*args, **kwargs)


