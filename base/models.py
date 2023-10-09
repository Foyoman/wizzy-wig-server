from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    temp_id = models.BigIntegerField(null=True, blank=True) 
    title = models.CharField(default="Untitled", max_length=30)
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    is_folder = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # If the File object has already been saved (i.e., it has an ID), 
        # clear the temp_id on subsequent save operations.
        if self.pk:
            self.temp_id = None
        super(File, self).save(*args, **kwargs)