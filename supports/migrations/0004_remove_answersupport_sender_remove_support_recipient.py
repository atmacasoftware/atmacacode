# Generated by Django 4.0.4 on 2022-07-15 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supports', '0003_supportroom_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answersupport',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='support',
            name='recipient',
        ),
    ]
