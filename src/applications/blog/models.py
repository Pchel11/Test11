from delorean import now
from django.db import models
from django.urls import reverse_lazy

created_at_default = now().datetime


class Post(models.Model):

    # xxx = models.TextField(unique=True)
    title = models.CharField(null=False, default="xxx", max_length=1000)
    content = models.CharField(null=True, blank=True, max_length=5000)
    created_at = models.DateTimeField(default=created_at_default)
    visible = models.BooleanField(default=True)
    author = models.CharField(max_length=100, null=False, default="test")

    def get_absolute_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": self.pk})

    def __str__(self):
        visible = "\N{FIRE}" if self.visible else "\N{SLEEPING SYMBOL}"
        msg = f'[{self.pk}] "{self.title}" {visible}'
        return msg

    class Meta:
        ordering = ["-created_at", "title", "pk"]
