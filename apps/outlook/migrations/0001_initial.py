# Generated by Django 4.2.13 on 2024-05-15 18:24

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outlook_id', models.CharField(max_length=256, null=True)),
                ('sender', models.CharField(max_length=64, null=True)),
                ('receiver', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None)),
                ('cc', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None)),
                ('bcc', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None)),
                ('subject', models.CharField(max_length=64, null=True)),
                ('preview', models.CharField(max_length=64, null=True)),
                ('body', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OutlookAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(blank=True, max_length=128, null=True)),
                ('access_token', models.CharField(blank=True, max_length=2048, null=True)),
                ('refresh_token', models.CharField(blank=True, max_length=2048, null=True)),
            ],
        ),
    ]
