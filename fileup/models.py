from __future__ import unicode_literals
from django.db import models
from django import forms

# Create your models here.
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Upload(models.Model):
    pic = models.FileField(upload_to="images/")
    upload_date = models.DateTimeField(auto_now_add=True)

# FileUpload form class.
class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('pic',)