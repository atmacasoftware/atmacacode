# Generated by Django 5.0.4 on 2024-08-07 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_marketplaces_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplaces',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Aktif mi?'),
        ),
    ]
