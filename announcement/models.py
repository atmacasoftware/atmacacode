from django.db import models
from atmacacode.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL


class Announcement(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True, verbose_name="Duyuru Başlık")
    content = models.TextField(verbose_name="Duyuru İçeriği")
    importance = models.CharField(max_length=255, null=True, verbose_name="Duyuru Önceliği")
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"

    def __str__(self):
        return f"{self.title}"
