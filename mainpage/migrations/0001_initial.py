# Generated by Django 4.0.4 on 2022-07-24 07:18

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='İsminiz')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('content', models.TextField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'İletişim',
                'verbose_name_plural': 'İletişimler',
            },
        ),
        migrations.CreateModel(
            name='MainSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slider_title', models.CharField(max_length=150, null=True, verbose_name='Slider Başlık')),
                ('sub_title', models.CharField(max_length=255, null=True, verbose_name='Alt Başlık')),
                ('text', models.CharField(max_length=300, null=True, verbose_name='Text')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='1. Fotoğraf (424 x 502)')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='2. Fotoğraf (376 x 376)')),
                ('details_img', models.ImageField(blank=True, null=True, upload_to='img/detay/', verbose_name='Detay Fotoğraf (872 x 510)')),
                ('shape1', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='1. Shape')),
                ('shape2', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='2. Shape')),
                ('shape3', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='3. Shape')),
                ('shape4', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='4. Shape')),
                ('shape5', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='5. Shape')),
                ('shape6', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='6. Shape')),
                ('shape7', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='7. Shape')),
                ('shape8', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='8. Shape')),
                ('shape9', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='9. Shape')),
                ('shape10', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='10. Shape')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slider_ids', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Ana Slider',
                'verbose_name_plural': 'Ana Slider',
            },
        ),
        migrations.CreateModel(
            name='PriceOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='İsim')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email')),
                ('content', models.TextField(max_length=2000, verbose_name='Mesaj')),
            ],
            options={
                'verbose_name': 'Fiyat Teklif Mesaj',
                'verbose_name_plural': 'Fiyat Teklif Mesajları',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('is_subscribe', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Abonelik',
                'verbose_name_plural': 'Abonelikler',
            },
        ),
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
        migrations.CreateModel(
            name='WebSiteCookies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie_provider', models.CharField(max_length=500, null=True, verbose_name='Cookie Sağlayıcısı')),
                ('cookie_name', models.CharField(max_length=500, null=True, verbose_name='Cookie İsmi')),
                ('cookie_aim', models.CharField(max_length=500, null=True, verbose_name='Cookie Amacı')),
                ('cookie_type', models.CharField(max_length=500, null=True, verbose_name='Cookie Tipi')),
                ('create_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Çerezler',
                'verbose_name_plural': 'Çerezler',
            },
        ),
        migrations.CreateModel(
            name='WebSiteKVKK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Başlık')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'KVKK Aydınlatma Metni',
                'verbose_name_plural': 'KVKK Aydınlatma Metni',
            },
        ),
        migrations.CreateModel(
            name='WebSiteMemberContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Başlık')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_at', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Üyelik Sözleşmesi',
                'verbose_name_plural': 'Üyelik Sözleşmesi',
            },
        ),
        migrations.CreateModel(
            name='WebSitePrivacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Başlık')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_at', models.DateTimeField()),
                ('data_country', models.CharField(max_length=5000, null=True, verbose_name='Verinin İşlendiği Ülkeler')),
                ('data_officer', models.CharField(max_length=255, null=True, verbose_name='Veri Sorumlusu')),
                ('data_officer_address', models.CharField(max_length=500, null=True, verbose_name='Veri Sorumlusu Adresi')),
            ],
            options={
                'verbose_name': 'Gizlilik Politikası',
                'verbose_name_plural': 'Gizlilik Politikası',
            },
        ),
    ]
