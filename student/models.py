from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from atmacacode.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL
from adminpage.models import Education

# Create your models here.

class StudentEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Öğrenci")
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name="studentEducation")
    email = models.CharField(verbose_name="Kayıtlı E-Posta", max_length=255, null=True, blank=False)
    is_approved = models.BooleanField(default=False, verbose_name="Onay Durumu")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class StudentAnnouncements(models.Model):
    title = models.CharField(max_length=255, verbose_name="Duyuru Başlığı")
    text = CKEditor5Field('İçerik', config_name='extends', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class StudentQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Öğrenci")
    education = models.ForeignKey(Education, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500, verbose_name="Soru Başlığı")
    content = CKEditor5Field('Yazı', config_name='extends', null=True)
    is_answered = models.BooleanField(default=False, verbose_name="Onay Durumu")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)