# Generated by Django 4.2.13 on 2024-05-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlookaccount',
            name='access_token',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outlookaccount',
            name='refresh_token',
            field=models.TextField(blank=True, null=True),
        ),
    ]
