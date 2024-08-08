from django.template import defaultfilters
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from unidecode import unidecode

from user_accounts.models import User

# Create your models here.

class SubscriptionType(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    detail = CKEditor5Field("Detay", config_name='extends', null=True)

    class Meta:
        verbose_name = "Abonelik Tipleri"
        verbose_name_plural = "Abonelik Tipleri"

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Müşteri Adı", blank=False, null=True)
    last_name = models.CharField(max_length=100, verbose_name="Müşteri Soyadı", blank=False, null=True)
    email = models.EmailField(max_length=100, verbose_name="Müşteri E-Posta", blank=False, null=True)
    mobile = models.CharField(max_length=100, verbose_name="Müşteri Telefonu", blank=False, null=True)
    subscription_type = models.ForeignKey(SubscriptionType, verbose_name="Abonelik Tipi", on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Başlangıç Tarihi")
    end_date = models.DateTimeField(auto_now_add=False, verbose_name="Bitiş Tarihi", blank=True, null=True)

    class Meta:
        verbose_name = "Müşteriler"
        verbose_name_plural = "Müşteriler"

    def __str__(self):
        return self.first_name + self.last_name

class MarketPlaces(models.Model):
    name = models.CharField(max_length=100, verbose_name="Pazaryeri")
    slug = models.SlugField(max_length=100, verbose_name="Slug", null=True)
    is_active = models.BooleanField(default=False, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Pazaryerleri"
        verbose_name_plural = "Pazaryerleri"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = MarketPlaces.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except MarketPlaces.DoesNotExist:
                    self.slug = slug
                    break
        super(MarketPlaces, self).save(*args, **kwargs)

class SupportedTypes(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tip Adı", blank=False, null=True)
    image = models.ImageField(upload_to="backend/img/ecommerce", verbose_name="XML Resmi")
    slug = models.SlugField(max_length=100, verbose_name="Slug", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Desteklenen Tipler"
        verbose_name_plural = "Desteklenen Tipler"

    def __str__(self):
        return self.name

    def get_image(self):
        return self.image.url

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = SupportedTypes.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except SupportedTypes.DoesNotExist:
                    self.slug = slug
                    break
        super(SupportedTypes, self).save(*args, **kwargs)

class Announcement(models.Model):
    name = models.CharField(max_length=100, verbose_name="Duyuru Adı", blank=False, null=True)
    image = models.ImageField(upload_to="backend/img/announcement", verbose_name="Duyuru Resmi")
    detail = CKEditor5Field("Detay", config_name='extends', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Duyurular"
        verbose_name_plural = "Duyurular"

    def __str__(self):
        return self.name

class AnnouncementReadIp(models.Model):
    announcement = models.ForeignKey(Announcement, verbose_name="Duyurular", on_delete=models.CASCADE, null=True, blank=False)
    ip = models.CharField(max_length=100, verbose_name="IP", blank=False, null=True)
    read_date = models.DateTimeField(auto_now_add=True)