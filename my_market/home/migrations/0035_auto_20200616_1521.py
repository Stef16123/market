# Generated by Django 3.0.6 on 2020-06-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_auto_20200616_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
    ]