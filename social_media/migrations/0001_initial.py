# Generated by Django 4.0.4 on 2022-07-15 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instagram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500, null=True, verbose_name='URL Bağlantısı')),
                ('image', models.ImageField(blank=True, upload_to='img/instgram/', verbose_name='Instagram Gönderileri')),
            ],
            options={
                'verbose_name': 'Instagram Gönderisi',
                'verbose_name_plural': 'Instagram Gönderileri',
            },
        ),
    ]
