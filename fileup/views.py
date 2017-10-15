from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import pprint
import csv

# Imaginary function to handle an uploaded file.

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("****request******"+str(request))
            handle_uploaded_file(request.FILES['file'],form.cleaned_data['title'])
            return HttpResponseRedirect('/fileup/#')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(datafile,title):
    data = []
    with open(title+'.csv', 'wb+') as destination:
        for chunk in datafile.chunks():
            destination.write(chunk)

    with open(title+'.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

    # with open('dest.csv', 'rt') as sd:
    #     r = csv.DictReader(sd)
    #     for line in r:
    #         data.append(line)

