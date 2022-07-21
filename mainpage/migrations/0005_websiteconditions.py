# Generated by Django 4.0.4 on 2022-07-21 13:22

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_priceoffer_remove_mainslider_large_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSiteConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Başlık')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Site Kullanım Şartları',
                'verbose_name_plural': 'Site Kullanım Şartları',
            },
        ),
    ]
