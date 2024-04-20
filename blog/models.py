import readtime as readtime
from ckeditor_uploader.fields import RichTextUploadingField
#from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
from atmacacode.settings import AUTH_USER_MODEL
# Create your models here.
from customers.models import Customer

User = AUTH_USER_MODEL

class Blog(models.Model):

    CATEGORY = (
        ('1','Genel'),
        ('2','HTML/Css'),
        ('3','Javasciprt'),
        ('4','Python'),
        ('5','Django'),
        ('6','Yapay Zeka'),
        ('7','Teknoloji'),
    )

    user = models.ForeignKey(User, default=1, null=True, verbose_name='Yazar',on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY, null=True, max_length=20, verbose_name="Kategori")
    category_slug = models.SlugField(max_length=1000, unique=False, null=True)
    image = models.ImageField(upload_to='static/img/blog/', blank=True, verbose_name="Blog Resmi")
    title = models.CharField(max_length=200, null=True, verbose_name='Başlık')
    content = RichTextUploadingField()
    keywords = models.CharField(max_length=100, verbose_name="Anahtar Kelime")
    created_at = models.DateField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateField(auto_now=True, verbose_name="Güncelleme Tarihi")
    blog_views = models.IntegerField(default=0, null=True, blank=True)
    is_main_slider = models.BooleanField(default=False, null=True, verbose_name="Ana Slider")
    mainslider_choice_date = models.DateTimeField(auto_now=False, null=True, verbose_name="Ana Slider Seçim Tarihi")
    is_main_choice = models.BooleanField(default=False, null=True)
    main_choice_date = models.DateTimeField(auto_now=False, verbose_name="Seçim Tarihi")
    is_other_choice = models.BooleanField(default=False, null=True)
    other_choice_date = models.DateTimeField(auto_now=False, verbose_name="Seçim Tarihi")
    is_avalabile = models.BooleanField(default=True)
    slug = models.SlugField(max_length=1000, unique=False, null=True)

    def __str__(self):
        return "%s %s" % (self.user, self.title)

    def get_blog_photos(self):
        if self.image:
            return self.image.url
        else:
            return None

    def get_absolute_url(self):
        return reverse('blog_details',args=[self.slug])

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(unidecode(value), allow_unicode=True)
        super().save(*args, **kwargs)

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def countReview(self):
        reviews = ReviewRating.objects.filter(blog=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    class Meta:
        verbose_name = "Blog Gönderisi"
        verbose_name_plural = "Blog Gönderileri"
        ordering = ['created_at', ]


class ReviewRating(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    rating = models.FloatField(blank=True,null=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yorum ve Oylama Sistemi"
        verbose_name_plural = "Yorum ve Oylama Sistemi"

