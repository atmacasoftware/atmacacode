from django.db import models

# Create your models here.
from atmacacode.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user = models.OneToOneField(User, verbose_name='Müşteri', on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"

    def register(self):
        self.save()

    def __str__(self):
        return self.email

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    def user_full_name(self):
        customer = self.get_customer_by_email()
        if customer.get_full_name():
            return customer.get_full_name()
        return None