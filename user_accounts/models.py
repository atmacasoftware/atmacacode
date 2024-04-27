from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, UserManager
from django.db import models


# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)


class User(AbstractUser, PermissionsMixin):

    GENDER = (
        ("Erkek", "Erkek"),
        ("Kadın/Kız", "Kadın/Kız"),
        ("Unisex", "Unisex"),
    )

    email = models.EmailField(db_index=True, unique=True, max_length=255, verbose_name="E-Posta")
    username = models.CharField(max_length=100, unique=False, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=255, verbose_name="Ad")
    last_name = models.CharField(max_length=255, verbose_name="Soyad")
    image = models.ImageField(upload_to='static/img/user/', blank=True, null=True, verbose_name="Profil Resmi")
    mobile = models.CharField(max_length=50, verbose_name="Telefon Numarası", blank=True)
    address = models.CharField(max_length=500, blank=True, verbose_name="Adres")
    birthday = models.DateField(blank=True, null=True, verbose_name="Doğum Tarihi")
    gender = models.CharField(choices=GENDER, max_length=50, verbose_name="Cinsiyet", default="Erkek")
    github = models.CharField(max_length=255, blank=True, null=True, verbose_name="Github Linki")
    linkedin = models.CharField(max_length=255, blank=True, null=True, verbose_name="Linkedin Linki")
    bio = models.CharField(blank=True, null=True, verbose_name="Bio", max_length=255)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    is_customer = models.BooleanField(default=False, verbose_name="Müşteri")
    is_staff = models.BooleanField(default=True, verbose_name="Personel")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    is_superuser = models.BooleanField(default=False, verbose_name="Admin")
    is_activated = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"
