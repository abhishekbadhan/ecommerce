# Generated by Django 3.0.6 on 2020-06-24 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacts',
            name='product_date',
        ),
    ]
