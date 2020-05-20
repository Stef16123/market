from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['username', 'id', 'email']
	# Установить кастомные поля для изменения
	# fieldsets = (
	# 	(None, {'fields': ('email', 'password')}),
	# 	('Personal info', {'fields': ('bio',)}),
	# 	('Permissions', {'fields': ('',)}),
	# )
admin.site.register(CustomUser, CustomUserAdmin)