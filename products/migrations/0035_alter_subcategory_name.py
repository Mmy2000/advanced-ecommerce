# Generated by Django 4.2.10 on 2024-07-01 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0034_category_image_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='subcategory name'),
        ),
    ]
