# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from uploader.models import UploadForm,Upload
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def home(request):
    if request.method=="POST":
        img = UploadForm(request.POST, request.FILES)
        print("img.Meta.model.pic: "+img.Meta.model.pic)
        if img.is_valid():
            img.save()
            return HttpResponseRedirect(reverse('imageupload'))
    else:
        img=UploadForm()
    images=Upload.objects.all()
    return render(request,'home.html',{'form':img,'images':images})