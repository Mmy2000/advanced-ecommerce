# Generated by Django 4.2.10 on 2024-06-23 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0009_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Carts', 'verbose_name_plural': 'Carts'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Cart Item', 'verbose_name_plural': 'Cart Item'},
        ),
    ]
