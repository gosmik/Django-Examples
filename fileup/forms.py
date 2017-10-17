from django import forms

from fileup.models import Document
from django.db import models

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

