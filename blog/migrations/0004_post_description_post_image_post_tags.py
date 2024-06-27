# Generated by Django 4.2.10 on 2024-06-27 00:56

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('blog', '0003_alter_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(default='', max_length=100000, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='', upload_to='post/', verbose_name='image'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags'),
        ),
    ]