# Generated by Django 3.0.6 on 2020-06-05 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20200605_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productordermodel',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='home.ProductModel'),
        ),
    ]