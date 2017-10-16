from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import pprint
import csv
from .forms import NameForm
import requests
from bs4 import BeautifulSoup

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
            myurl= "https://www.amazon.com/dp/"+row[0]
            print("Amazon url: "+myurl)
            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
            result = requests.get(myurl,headers=header)
            print("status code :"+str(result.status_code))
            c = result.content
            soup = BeautifulSoup(c, "html.parser")
            # samples = soup.find_all(lambda tag: tag.name == 'span')
            samples = soup.find(id="priceblock_ourprice").string
            print(samples)
            # print(soup.find("span", {"id": "priceblock_ourprice"}))

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

