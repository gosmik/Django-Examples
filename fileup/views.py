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
            # print("*****filename***"+form.cleaned_data['file'].name)
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
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            itemUrl= "https://www.amazon.com/dp/"+row[0]
            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
            result = requests.get(itemUrl,headers=header)
            # print("status code :"+str(result.status_code))
            c = result.content
            soup = BeautifulSoup(c, "html.parser")
            # TO-DO Here there will be html or null check
            price = soup.find(id="priceblock_ourprice").string
            ProductUrl = itemUrl

            insReviewModel = ReviewModel()

            for review in soup.findAll('div', id=lambda x: x and x.startswith('customer_review-')):
                insReviewModel.ProductUrl = itemUrl
                insReviewModel.Reviewstarcount = float(review.find(class_='a-icon-alt').string.split()[0])
                insReviewModel.Reviewsubject = review.find(class_='a-size-base').string
                insReviewModel.Reviewcontent =review.find(class_='a-expander-content').string
                insReviewModel.Reviewdate = review.find(class_='review-date').string

                print("review: " + str(review))
                print("Reviewcontent: "+str(insReviewModel.Reviewcontent))
                count = len(str(insReviewModel.Reviewcontent).split())
                writeReviewDataToCsv(resultFileName,insReviewModel)
            # ProductUrl
            # Reviewstarcount  = soup.find(id="priceblock_ourprice").string
            # Reviewsubject
            # Review content
            # Reviewword count
            # Review date
            # Attached image count
            # Howmanypeoplehavefoundreviewuseful
            # UsefulnessScore

def writeReviewDataToCsv(_resultFileName,_ReviewModel):
    with open(_resultFileName, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([_ReviewModel.ProductUrl,_ReviewModel.Reviewsubject,_ReviewModel.Reviewstarcount,_ReviewModel.Reviewcontent,_ReviewModel.Reviewwordcount])