from django.db import models
from atmacacode.settings import AUTH_USER_MODEL
User = AUTH_USER_MODEL
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.PROTECT)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.PROTECT)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)

    def __str__(self):
        return "%s - %s" % (self.sender, self.receiver)
