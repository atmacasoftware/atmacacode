# Generated by Django 5.0.4 on 2024-06-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_accounts', '0005_user_is_contract_user_is_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='İş Ünvanı'),
        ),
    ]
