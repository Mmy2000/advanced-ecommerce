# Generated by Django 4.2.10 on 2024-06-22 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0007_alter_contact_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='auther',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]