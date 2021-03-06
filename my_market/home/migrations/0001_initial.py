# Generated by Django 3.1.1 on 2020-09-16 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum_in_basket', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CouponModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.FloatField(default=1)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('confirmation', models.BooleanField(default=False)),
                ('user', models.CharField(max_length=70)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('surname', models.CharField(default='', max_length=100)),
                ('adress', models.CharField(default='', max_length=200)),
                ('cost', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDescribeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('price', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('body', models.TextField(max_length=1000)),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('popular', models.IntegerField(default=0)),
                ('category', models.ManyToManyField(blank=True, related_name='product_describe', to='home.CategoryModel')),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.IntegerField(unique=True)),
                ('count_products', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RatingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('voites', models.IntegerField(default=1)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='home.productdescribemodel')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.ordermodel')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_order', to='home.productmodel')),
            ],
        ),
        migrations.AddField(
            model_name='productdescribemodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.productmodel'),
        ),
        migrations.CreateModel(
            name='ProductBasketModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.productmodel')),
                ('product_basket', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.basketmodel')),
                ('product_describe', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='home.productdescribemodel')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarkModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.productdescribemodel')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mark', to='home.ratingmodel')),
            ],
        ),
    ]
