import datetime
from datetime import datetime

from django.template import defaultfilters
from django.utils import timezone
import random

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from unidecode import unidecode

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

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = BlogCategory.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except BlogCategory.DoesNotExist:
                    self.slug = slug
                    break
        super(BlogCategory, self).save(*args, **kwargs)


class Blog(models.Model):
    STATUS = (
        ("Yayınla", "Yayınla"),
        ("Taslak", "Taslak"),
        ("Askıya Al", "Askıya Al")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yazar", null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name="Kategori", null=True)
    name = models.CharField(max_length=255, verbose_name="Başlık", null=True, blank=False)
    text = CKEditor5Field('Yazı', config_name='extends', null=True)
    image = models.ImageField(upload_to='static/img/blog/', blank=True, verbose_name="Kapak")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Gösterim Sayısı", null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True, default="Yayınla")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Blog.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Blog.DoesNotExist:
                    self.slug = slug
                    break
        super(Blog, self).save(*args, **kwargs)
