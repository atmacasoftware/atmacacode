from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
# Create your models here.
from django.urls import reverse

from customers.models import Customer


class Services(models.Model):
    service_name = models.CharField(max_length=500, verbose_name="Hizmet Adı", null=True)
    service_price = models.CharField(max_length=255, verbose_name="Hizmet Ücreti", null=True,blank=True)
    service_img = models.ImageField(upload_to='img/hizmetler/', blank=True, verbose_name="Hizmet Resimleri")
    slug = models.SlugField(max_length=1000, unique=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_avalabile = models.BooleanField(default=True)
    is_complated = models.BooleanField(default=False)

    class Meta:
        db_table = "product_product"
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        if self.service_name != '':
            return self.service_name
        else:
            return "Hizmet"

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def get_service_image(self):
        if self.service_img:
            return self.service_img.url
        else:
            return None

    def get_added_like_customer(self):
        return self.like_service.values_list('customer_id', flat=True)

    def get_added_dislike_customer(self):
        return self.dislike_service.values_list('customer_id', flat=True)

    def get_like_count(self):
        like_count = self.like_service.count()
        if like_count > 0:
            return like_count
        return 0

    def get_dislike_count(self):
        dislike_count = self.dislike_service.count()
        if dislike_count > 0:
            return dislike_count
        return 0

    def save(self, *args, **kwargs):
        value = self.service_name
        self.slug = slugify(unidecode(value), allow_unicode=True)
        super().save(*args, **kwargs)

class ReviewRatingService(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=200, blank=True)
    rating = models.FloatField(blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yorum ve Oylama Sistemi"
        verbose_name_plural = "Yorum ve Oylama Sistemi"

    def __str__(self):
        return self.subject


class LikeProduct(models.Model):
    customer = models.ForeignKey(Customer, null=True, related_name='like_service', on_delete=models.CASCADE)
    service = models.ForeignKey(Services, null=True, blank=True, on_delete=models.CASCADE, related_name='like_service')
    comment = models.ForeignKey(ReviewRatingService, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Beğenilen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer, self.service)

    def user_liked_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.service
        sender = like.customer

    def user_unlike_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.service
        sender = like.customer


class DisLikeProduct(models.Model):
    customer = models.ForeignKey(Customer, null=True, related_name='dislike_service', on_delete=models.CASCADE)
    service = models.ForeignKey(Services, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='dislike_service')
    comment = models.ForeignKey(ReviewRatingService, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Beğenilmeyen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer, self.service)

    def user_disliked_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.service
        sender = like.customer

    def user_undislike_product(sender, instance, *args, **kwargs):
        like = instance
        product = like.service
        sender = like.customer


class Favorite(models.Model):
    customer = models.ForeignKey(Customer, null=True, related_name='favorite_service', on_delete=models.CASCADE)
    service = models.ForeignKey(Services, null=True, blank=True, on_delete=models.CASCADE,
                                related_name="favorite_service")

    class Meta:
        verbose_name_plural = 'Favorilere Eklenen Ürünler'

    def __str__(self):
        return "%s %s" % (self.customer, self.service)

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ürün Adı", null=True, blank=False)


