from django.template import defaultfilters
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from unidecode import unidecode
from atmacacode.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL
# Create your models here.

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, null=True, blank=True)
    site_title = models.CharField(max_length=100, null=True, blank=True)
    site_description = models.TextField(null=True, blank=True)
    site_author = models.CharField(max_length=100, null=True, blank=True)
    site_keywords = models.CharField(max_length=125, null=True, blank=True)
    site_logo = models.ImageField(upload_to='img/logo', null=True, blank=True)
    site_email = models.EmailField(max_length=254, null=True, blank=True)
    site_whatsapp = models.CharField(max_length=100, null=True, blank=True)
    instagram_link = models.CharField(max_length=150,null=True, blank=True)
    linkedin_link = models.CharField(max_length=150, null=True, blank=True)
    facebook_link = models.CharField(max_length=150, null=True, blank=True)
    youtube_link = models.CharField(max_length=150, null=True, blank=True)
    udemy_link = models.CharField(max_length=150, null=True, blank=True)

    def get_logo(self):
        if self.site_logo:
            return self.site_logo.url
        return None

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
    description = models.CharField(max_length=255, verbose_name="Açıklama", null=True, blank=False)
    text = CKEditor5Field('Yazı', config_name='extends', null=True)
    image = models.ImageField(upload_to='static/img/blog/', blank=True, verbose_name="Kapak")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Gösterim Sayısı", null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True, default="Yayınla")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def get_user(self):
        return self.user

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

class BlogUserIp(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Blog", null=True)
    ip = models.CharField(max_length=100, verbose_name="Kullanıcı IP Adres", null=True, blank=True)

class Education(models.Model):
    name = models.CharField(max_length=300, verbose_name="Eğitim Adı")
    status = models.BooleanField(default=False, verbose_name="Yayın Durumu")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def student_oferring_count(self):
        return self.studentEducation.filter(is_approved=False).count()
    def student_registred_count(self):
        return self.studentEducation.filter(is_approved=True).count()

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            slug = defaultfilters.slugify(unidecode(self.name))
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exits = Education.objects.get(slug=slug)
                    if slug_exits:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Education.DoesNotExist:
                    self.slug = slug
                    break
        super(Education, self).save(*args, **kwargs)