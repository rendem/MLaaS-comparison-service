from django.db import models


class Mlcmp(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(max_length=555, blank=True)

    def __str__(self):
        """A string presentation of the model."""
        return self.result
