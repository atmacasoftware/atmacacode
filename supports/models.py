from django.db import models
from atmacacode.settings import AUTH_USER_MODEL
from django.db.models import Max

from customers.models import Customer
from user_accounts.models import User
from datetime import datetime

User = AUTH_USER_MODEL
import random


# Create your models here.

class SupportRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Oda"
        verbose_name_plural = "Destek Odaları"

class Support(models.Model):
    room = models.ForeignKey(SupportRoom, on_delete=models.CASCADE,null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    body = models.TextField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Destek"
        verbose_name_plural = "Destek Talepleri"


class AnswerSupport(models.Model):
    room = models.ForeignKey(SupportRoom, on_delete=models.CASCADE, null=True)
    support = models.ForeignKey(Support, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alıcı")
    body = models.TextField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Destek Cevabı"
        verbose_name_plural = "Destek Cevapları"
