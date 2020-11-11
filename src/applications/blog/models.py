from delorean import now
from django.db import models
from django.urls import reverse_lazy

created_at_default = now().datetime


class Post(models.Model):
    # xxx = models.TextField(unique=True)
    title = models.CharField(unique=True, max_length=100)
    content = models.CharField(null=True, blank=True, max_length=5000)
    created_at = models.DateTimeField(default=created_at_default)
    visible = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": self.pk})

    def __str__(self):
        msg = f"'{self.title}', visible? {self.visible}"
        return msg

    class Meta:
        ordering = ["-created_at", "title", "pk"]
