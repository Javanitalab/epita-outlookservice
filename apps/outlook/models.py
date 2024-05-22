from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.


class OutlookAccount(models.Model):
    email_address = models.CharField(max_length=128, null=True, blank=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)


class Email(models.Model):
    outlook_id = models.CharField(max_length=256, null=True)
    sender = models.CharField(max_length=128, null=True)
    receiver = ArrayField(models.CharField(max_length=128), null=True)
    cc = ArrayField(models.CharField(max_length=128), null=True)
    bcc = ArrayField(models.CharField(max_length=128), null=True)
    subject = models.CharField(max_length=512, null=True)
    preview = models.TextField( null=True)
    body = models.TextField(null=True)
