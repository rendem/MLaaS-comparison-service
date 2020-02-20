from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile


class Mlcmp(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(max_length=555, blank=True)

    def __str__(self):
        """A string presentation of the model."""
        return self.result
