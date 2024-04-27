# Generated by Django 5.0.4 on 2024-04-27 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpage', '0004_blog_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogUserIp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=100, null=True, verbose_name='Kullanıcı IP Adres')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminpage.blog', verbose_name='Blog')),
            ],
        ),
    ]
