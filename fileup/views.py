from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse

from fileup.DataModel import ReviewModel
from .forms import UploadFileForm
import csv
import requests
from bs4 import BeautifulSoup
import array

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],form.cleaned_data['file'].name)
            print("*****filename***"+form.cleaned_data['file'].name)
            return HttpResponseRedirect('/fileup/uploaded')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(datafile,filename):
    resultFileName = "result"+filename

    with open(filename,'wb') as destination:
        for chunk in datafile.chunks():
            destination.write(chunk)

    with open(filename, 'r+' ,newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            itemUrl= "https://www.amazon.com/dp/"+row[0]
            print("Amazon url: "+itemUrl)
            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
            result = requests.get(itemUrl,headers=header)
            print("status code :"+str(result.status_code))
            c = result.content
            soup = BeautifulSoup(c, "html.parser")
            price = soup.find(id="priceblock_ourprice").string
            print(price,price)
            ProductUrl = itemUrl

            insReviewModel = ReviewModel()

            Reviewsubjects = []
            for review in soup.findAll('div', id=lambda x: x and x.startswith('customer_review-')):
                Reviewsubjects.append(review.find(class_='a-size-base').string)
                insReviewModel.ProductUrl = itemUrl
                insReviewModel.Reviewsubject = review.find(class_='a-size-base').string
            print(insReviewModel)
            writeReviewDataToCsv(resultFileName,insReviewModel)
            # Reviewstarcount  = soup.find(id="priceblock_ourprice").string
            # Reviewsubject
            # Review content
            # Reviewword count
            # Review date
            # Attached image count
            # Howmanypeoplehavefoundreviewuseful
            # UsefulnessScore

def writeReviewDataToCsv(_resultFileName,_ReviewModel):
    with open(_resultFileName, 'w+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([_ReviewModel.ProductUrl,_ReviewModel.Reviewsubject])