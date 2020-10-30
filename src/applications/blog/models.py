from delorean import now
from django.db import models


class Post(models.Model):
    # xxx = models.TextField(unique=True)
    title = models.TextField(unique=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=lambda: now().datetime)
    visible = models.BooleanField(default=True)

    def __str__(self):
        msg = f"'{self.title}', visible? {self.visible}"
        return msg
