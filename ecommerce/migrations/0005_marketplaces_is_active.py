# Generated by Django 5.0.4 on 2024-08-07 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_alter_customer_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplaces',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Aktif mi?'),
        ),
    ]
