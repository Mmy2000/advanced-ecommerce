# Generated by Django 4.2.10 on 2024-06-22 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_remove_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='PRDBrand',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
