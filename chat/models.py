from django.db import models
from django.urls import reverse


class Chat(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)
    address = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    channel = models.CharField(max_length=50)
    send_to = models.CharField(max_length=50)
    title = models.CharField(null=True, blank=True, max_length=25)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return f"{self.title}-{self.content[0:20]}"

    def get_absolute_url(self):
        return reverse("chat:detail", kwargs={"uid": self.uid})

    class Meta:
        ordering = ["-timestamp", ]
