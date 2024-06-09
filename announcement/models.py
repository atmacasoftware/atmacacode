from django.db import models
from atmacacode.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL


class Announcement(models.Model):

    TYPE_CHOICES = (
        ('Soru', 'Soru'),
        ('Kayıt Onay', 'Kayıt Onay'),
        ('İş Teklifi', 'İş Teklifi')
    )

    users = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True, verbose_name="Duyuru Başlık")
    content = models.TextField(verbose_name="Duyuru İçeriği")
    importance = models.CharField(max_length=255, null=True, verbose_name="Duyuru Önceliği")
    type_choices = models.CharField(choices=TYPE_CHOICES, null=True, verbose_name="Duyuru Tipi", max_length=50)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"

    def __str__(self):
        return f"{self.title}"

    def passing_time(self):
        from datetime import datetime, timezone
        import math
        now = datetime.now(timezone.utc)
        pass_time = now - self.created_at
        passing = None

        if pass_time.days > 0 and pass_time.days < 31:
            passing = f"{pass_time.days} gn."

        elif pass_time.days < 1:
            if pass_time.seconds / 60 < 60:
                passing = f"{math.floor(pass_time.seconds / 60)} dk."
            elif pass_time.seconds / 60 > 59:
                passing = f"{math.floor(pass_time.seconds / 3600)} sa."
        return passing
