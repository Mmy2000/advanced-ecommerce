# Generated by Django 4.2.10 on 2024-06-21 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_alter_variation_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
    ]