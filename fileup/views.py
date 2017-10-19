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
            if soup.find(id="priceblock_ourprice") is not None:
                price = soup.find(id="priceblock_ourprice").string

            ProductUrl = itemUrl

            for review in soup.findAll('div', id=lambda x: x and x.startswith('customer_review-')):
                insReviewModel = ReviewModel()
                insReviewModel.ProductUrl = itemUrl
                insReviewModel.Reviewstarcount = float(review.find(class_='a-icon-alt').string.split()[0])
                insReviewModel.Reviewsubject = review.find(class_='a-size-base').string
                insReviewModel.Reviewcontent =review.find(class_='a-expander-content').string
                insReviewModel.Reviewwordcount = len(str(insReviewModel.Reviewcontent).split())
                insReviewModel.Reviewdate = review.find(class_='review-date').string
                for attached in review.findAll('div', id=lambda x: x and x.startswith('video-block-')):
                    insReviewModel.Attachedimagecount +=1
                for attached in review.findAll('img', class_='review-image-tile'):
                    insReviewModel.Attachedimagecount += 1
                insReviewModel.HowManyLikedReview = int(review.find(class_='review-votes').string.split()[0])



                writeReviewDataToCsv(resultFileName,insReviewModel)
            # ProductUrl
            # Reviewstarcount  = soup.find(id="priceblock_ourprice").string
            # Reviewsubject
            # Review content
            # Reviewword count
            # Review date
            # Attached image count
            # HowManyLikedReview
            # UsefulnessScore

def writeReviewDataToCsv(_resultFileName,_ReviewModel):
    with open(_resultFileName, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow([_ReviewModel.ProductUrl,
                            _ReviewModel.Reviewstarcount,
                            _ReviewModel.Reviewsubject,
                            _ReviewModel.Reviewcontent,
                            _ReviewModel.Reviewwordcount,
                            _ReviewModel.Reviewdate,
                            _ReviewModel.Attachedimagecount,
                            _ReviewModel.HowManyLikedReview])