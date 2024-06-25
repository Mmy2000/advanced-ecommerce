# Generated by Django 4.2.10 on 2024-06-25 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0010_about_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='this title is display in slider in home page', max_length=150)),
                ('image', models.ImageField(help_text='this image is display in slider in home page', upload_to='homeImages/')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_image', to='settings.settings')),
            ],
            options={
                'verbose_name': 'Home Images',
                'verbose_name_plural': 'Home Images',
            },
        ),
    ]
