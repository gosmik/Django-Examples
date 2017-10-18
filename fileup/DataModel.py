
class ReviewModel:

    def __init__(self):
        self.ProductUrl = ""
        self.Reviewstarcount = 0
        self.Reviewsubject = ""
        self.Reviewcontent = ""
        self.Reviewwordcount = 0
        self.Reviewdate =""
        self.Attachedimagecount =0
        self.Howmanypeoplehavefoundreviewuseful = 0
        self.UsefulnessScore = 0

    def __str__(self):
        return self.ProductUrl+\
               ","+str(self.Reviewstarcount)+ \
               ","+self.Reviewsubject+ \
               ","+self.Reviewcontent+ \
               ","+str(self.Reviewwordcount)+ \
               ","+self.Reviewdate+self.Reviewdate+ \
               ","+str(self.Attachedimagecount)+ \
               ","+str(self.Howmanypeoplehavefoundreviewuseful)+ \
               ","+str(self.UsefulnessScore)

