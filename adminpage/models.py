import datetime
from datetime import datetime
from django.utils import timezone
import random

from django.db import models
from atmacacode.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


# Create your models here.

class AdminUser(models.Model):
    user = models.OneToOneField(User, verbose_name='Yetkili Kişi', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='İsim')
    last_name = models.CharField(max_length=60, verbose_name='Soyisim')
    phone = models.CharField(max_length=15, verbose_name='Telefon Numarası')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=100)
    address = models.TextField(max_length=300, verbose_name='Adres', null=True)
    is_admin = models.BooleanField(default=True, null=True)
    photo = models.ImageField(upload_to='static/img/admin_photo/', null=True, blank=True,
                              verbose_name='Yönetici Fotoğrafı')
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_exist = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = "Yönetici"
        verbose_name_plural = "Yöneticiler"

    def __str__(self):
        return f"{self.user}"

    def get_profil_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return "/static/img/empty_standart.png"

    @staticmethod
    def get_admin_by_email(email):
        try:
            return AdminUser.objects.get(email=email)
        except:
            return False


class Task(models.Model):
    user = models.ForeignKey(User, verbose_name='Yetkili Kişi', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=500, null=True, blank=False, verbose_name="Müşteri İsmi")
    customer_email = models.EmailField(max_length=250, null=True, blank=True, verbose_name="Müşteri Email")
    customer_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Müşteri Telefon")
    task_name = models.CharField(max_length=500, null=True, blank=False, verbose_name="Görev Adı")
    task_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, default=0.0,
                                     verbose_name="Görev Ücreti")
    task_start_date = models.DateField()
    estimated_deliver_date = models.DateField()
    is_exist = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Görev"
        verbose_name_plural = "Görevler"

    def __str__(self):
        return f"{self.customer_name + '-' + self.task_name}"

    def duration(self):
        return self.estimated_deliver_date - self.task_start_date


class Note(models.Model):
    user = models.ForeignKey(User, verbose_name='Yetkili Kişi', on_delete=models.CASCADE)
    note_title = models.CharField(max_length=100, null=True, blank=False, verbose_name="Not Başlık")
    note_content = models.TextField(verbose_name="Not İçerik", null=True, blank=True, max_length=10000)
    task_start_date = models.DateField(auto_now=True)
    is_exist = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Not"
        verbose_name_plural = "Notlar"

    def __str__(self):
        return f"{self.user + '-' + self.note_title}"

