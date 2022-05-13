from django.db import models
from atmacacode.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL
# Create your models here.

class AdminUser(models.Model):
    authorizedperson = models.OneToOneField(User, verbose_name='Yetkili Kişi', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='İsim')
    last_name = models.CharField(max_length=60, verbose_name='Soyisim')
    phone = models.CharField(max_length=15, verbose_name='Telefon Numarası')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=100)
    address = models.TextField(max_length=300, verbose_name='Adres', null=True)
    is_admin = models.BooleanField(default=True, null=True)
    photo = models.ImageField(upload_to='static/img/admin_photo/', null=True, blank=True, verbose_name='Yönetici Fotoğrafı')
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_exist = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name = "Yönetici"
        verbose_name_plural = "Yöneticiler"

    def __str__(self):
        return f"{self.authorizedperson.username}"

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