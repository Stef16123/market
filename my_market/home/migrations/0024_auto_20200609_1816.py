# Generated by Django 3.0.6 on 2020-06-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20200609_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermarkmodel',
            name='token',
            field=models.CharField(max_length=250),
        ),
    ]