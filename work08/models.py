from django.db import models

class Memo(models.Model):
    title = models.CharField(max_length=100, default="no title")
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='memo_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title