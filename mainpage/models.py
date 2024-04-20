from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
# Create your models here.

class MainSlider(models.Model):
    slider_title = models.CharField(max_length=150, verbose_name='Slider Başlık', null=True)
    sub_title = models.CharField(max_length=255, verbose_name='Alt Başlık', null=True)
    text = models.CharField(max_length=300, verbose_name='Text', null=True)
    image1 = models.ImageField(upload_to='img/', verbose_name='1. Fotoğraf (424 x 502)', null=True, blank=True)
    image2 = models.ImageField(upload_to='img/', verbose_name='2. Fotoğraf (376 x 376)', null=True, blank=True)
    details_img = models.ImageField(upload_to='img/detay/', verbose_name='Detay Fotoğraf (872 x 510)', null=True,
                                    blank=True)
    shape1 = models.ImageField(upload_to='img/', verbose_name='1. Shape', null=True, blank=True)
    shape2 = models.ImageField(upload_to='img/', verbose_name='2. Shape', null=True, blank=True)
    shape3 = models.ImageField(upload_to='img/', verbose_name='3. Shape', null=True, blank=True)
    shape4 = models.ImageField(upload_to='img/', verbose_name='4. Shape', null=True, blank=True)
    shape5 = models.ImageField(upload_to='img/', verbose_name='5. Shape', null=True, blank=True)
    shape6 = models.ImageField(upload_to='img/', verbose_name='6. Shape', null=True, blank=True)
    shape7 = models.ImageField(upload_to='img/', verbose_name='7. Shape', null=True, blank=True)
    shape8 = models.ImageField(upload_to='img/', verbose_name='8. Shape', null=True, blank=True)
    shape9 = models.ImageField(upload_to='img/', verbose_name='9. Shape', null=True, blank=True)
    shape10 = models.ImageField(upload_to='img/', verbose_name='10. Shape', null=True, blank=True)
    content = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slider_ids = models.IntegerField(default=0)
    slug = models.SlugField(max_length=1000, unique=False, null=True)

    class Meta:
        verbose_name = "Ana Slider"
        verbose_name_plural = "Ana Slider"

    def save(self, *args, **kwargs):
        value = self.slider_title
        self.slug = slugify(unidecode(value), allow_unicode=True)
        super().save(*args, **kwargs)

    def get_image1(self):
        if self.image1:
            return self.image1.url
        else:
            return None

    def get_image2(self):
        if self.image2:
            return self.image2.url
        else:
            return None

    def get_detail(self):
        if self.details_img:
            return self.details_img.url
        else:
            return None

    def get_shape1(self):
        if self.shape1:
            return self.shape1.url
        else:
            return None

    def get_shape2(self):
        if self.shape2:
            return self.shape2.url
        else:
            return None

    def get_shape3(self):
        if self.shape3:
            return self.shape3.url
        else:
            return None

    def get_shape4(self):
        if self.shape4:
            return self.shape4.url
        else:
            return None

    def get_shape5(self):
        if self.shape5:
            return self.shape5.url
        else:
            return None

    def get_shape6(self):
        if self.shape6:
            return self.shape6.url
        else:
            return None

    def get_shape7(self):
        if self.shape7:
            return self.shape7.url
        else:
            return None

    def get_shape8(self):
        if self.shape8:
            return self.shape8.url
        else:
            return None

    def get_shape9(self):
        if self.shape9:
            return self.shape9.url
        else:
            return None

    def get_shape10(self):
        if self.shape10:
            return self.shape10.url
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


class PriceOffer(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False, verbose_name="İsim")
    email = models.EmailField(unique=True, blank=False, null=True, verbose_name="Email")
    content = models.TextField(verbose_name="Mesaj", max_length=2000)

    class Meta:
        verbose_name = "Fiyat Teklif Mesaj"
        verbose_name_plural = "Fiyat Teklif Mesajları"

    def __str__(self):
        return f"{self.name}-{self.email}"


class WebSiteMemberContract(models.Model):
    title = models.CharField(max_length=255, null=True, blank=False, verbose_name="Başlık")
    content = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = "Üyelik Sözleşmesi"
        verbose_name_plural = "Üyelik Sözleşmesi"

    def __str__(self):
        return f"{self.title}-{self.create_at}"

class WebSiteConditions(models.Model):
    title = models.CharField(max_length=255, null=True, blank=False, verbose_name="Başlık")
    content = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = "Site Kullanım Şartları"
        verbose_name_plural = "Site Kullanım Şartları"

    def __str__(self):
        return f"{self.title}-{self.create_at}"

class WebSitePrivacy(models.Model):
    title = models.CharField(max_length=255, null=True, blank=False, verbose_name="Başlık")
    content = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=False)
    data_country = models.CharField(max_length=5000, null=True, blank=False, verbose_name="Verinin İşlendiği Ülkeler")
    data_officer = models.CharField(max_length=255, null=True, blank=False, verbose_name="Veri Sorumlusu")
    data_officer_address = models.CharField(max_length=500, null=True, blank=False, verbose_name="Veri Sorumlusu Adresi")

    class Meta:
        verbose_name = "Gizlilik Politikası"
        verbose_name_plural = "Gizlilik Politikası"

    def __str__(self):
        return f"{self.title}-{self.create_at}"


class WebSiteCookies(models.Model):
    cookie_provider = models.CharField(max_length=500, null=True, blank=False, verbose_name="Cookie Sağlayıcısı")
    cookie_name = models.CharField(max_length=500, null=True, blank=False, verbose_name="Cookie İsmi")
    cookie_aim = models.CharField(max_length=500, null=True, blank=False, verbose_name="Cookie Amacı")
    cookie_type = models.CharField(max_length=500, null=True, blank=False, verbose_name="Cookie Tipi")
    create_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = "Çerezler"
        verbose_name_plural = "Çerezler"

    def __str__(self):
        return f"{self.cookie_provider}-{self.cookie_name}-{self.cookie_type}"

class WebSiteKVKK(models.Model):
    title = models.CharField(max_length=255, null=True, blank=False, verbose_name="Başlık")
    content = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=False)


    class Meta:
        verbose_name = "KVKK Aydınlatma Metni"
        verbose_name_plural = "KVKK Aydınlatma Metni"

    def __str__(self):
        return f"{self.title}-{self.create_at}"



