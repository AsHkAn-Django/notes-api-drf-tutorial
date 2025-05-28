from django.db import models
from django.conf import settings


class Note(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title