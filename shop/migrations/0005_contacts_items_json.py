# Generated by Django 3.0.6 on 2020-06-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='items_json',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
