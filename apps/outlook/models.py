from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class OutlookAccount(models.Model):
    email_address = models.CharField(max_length=128, null=True, blank=True)
    access_token = models.CharField(max_length=2048, null=True, blank=True)
    refresh_token = models.CharField(max_length=2048, null=True, blank=True)


class Email(models.Model):
    outlook_id = models.CharField(max_length=256, null=True)
    sender = models.CharField(max_length=64, null=True)
    receiver = ArrayField(models.CharField(max_length=128))
    cc = ArrayField(models.CharField(max_length=128))
    bcc = ArrayField(models.CharField(max_length=128))
    subject = models.CharField(max_length=64, null=True)
    preview = models.CharField(max_length=64, null=True)
    body = models.TextField(null=True)
