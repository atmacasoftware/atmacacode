from django.db import models


# Create your models here.

class MainSlider(models.Model):
    large_image = models.ImageField(upload_to='img/', verbose_name='Büyük Resim')
    small_image = models.ImageField(upload_to='img/', verbose_name='Küçük Resim')
    slider_title = models.CharField(max_length=100, verbose_name='Slider Başlık')
    content = models.CharField(max_length=250, verbose_name='Slider İçerik', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slider_ids = models.IntegerField(default=0)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Ana Slider"
        verbose_name_plural = "Ana Slider"

    def get_large_photo(self):
        if self.large_image:
            return self.large_image.url
        else:
            return None

    def get_small_photo(self):
        if self.large_image:
            return self.small_image.url
        else:
            return None

class Contact(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name="İsminiz")
    email = models.EmailField(blank=False, null=True)
    phone = models.CharField(max_length=11, blank=False, null=True)
    content = models.TextField(blank=False, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "İletişim"
        verbose_name_plural = "İletişimler"


    def __str__(self):
        return f"{self.name}-{self.email}"

class Subscribe(models.Model):
    email = models.EmailField(blank=False, null=True)
    is_subscribe = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Abonelik"
        verbose_name_plural = "Abonelikler"

    def __str__(self):
        return f"{self.email}"
