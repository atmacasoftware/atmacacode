from django.db import models

# Create your models here.

class Instagram(models.Model):
    url = models.CharField(max_length=500, null=True, verbose_name="URL Bağlantısı")
    image = models.ImageField(upload_to='img/instgram/', blank=True, verbose_name="Instagram Gönderileri")

    class Meta:
        verbose_name = "Instagram Gönderisi"
        verbose_name_plural = "Instagram Gönderileri"

    def get_instagram_image(self):
        if self.image:
            return self.image.url
        else:
            return None