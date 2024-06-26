# Generated by Django 5.0.4 on 2024-06-06 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0006_education'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100)),
                ('site_title', models.CharField(max_length=100)),
                ('site_description', models.TextField()),
                ('site_author', models.CharField(max_length=100)),
                ('site_keywords', models.CharField(max_length=125)),
                ('site_logo', models.ImageField(upload_to='img/logo')),
                ('site_email', models.EmailField(max_length=254)),
                ('instagram_link', models.CharField(max_length=150)),
                ('linkedin_link', models.CharField(max_length=150)),
                ('facebook_link', models.CharField(max_length=150)),
                ('youtube_link', models.CharField(max_length=150)),
                ('udemy_link', models.CharField(max_length=150)),
            ],
        ),
    ]
