# Generated by Django 4.2.10 on 2024-06-30 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0014_alter_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='offer',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='offer'),
        ),
    ]
