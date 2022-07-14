from django.db import models

# Create your models here.
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=500, null=True, blank=False)
    status = models.CharField(max_length=255, default="Sipariş Oluşturuldu.")
    order_detail = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=False)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"

    def __str__(self):
        return f"{self.customer}"