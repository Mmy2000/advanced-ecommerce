# Generated by Django 4.2.10 on 2024-06-25 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_delete_coupon_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Categories', 'verbose_name_plural': 'Categories'},
        ),
    ]
