# Generated by Django 4.0.4 on 2022-07-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_name',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
