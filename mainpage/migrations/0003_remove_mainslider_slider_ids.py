# Generated by Django 5.0.4 on 2024-06-06 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_remove_mainslider_shape1_remove_mainslider_shape10_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainslider',
            name='slider_ids',
        ),
    ]
