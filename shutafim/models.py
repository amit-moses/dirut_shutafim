from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
import firebase_admin
from firebase_admin import credentials,initialize_app, storage


class Apartment(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE) 
    city = models.CharField(null=False, max_length=100)#
    street = models.CharField(max_length=100)#
    rent_price = models.IntegerField(default=0)#
    floor = models.IntegerField(default=0)#
    partners = models.IntegerField(default=0)#
    gender = models.IntegerField(default=0)#
    entry_date = models.DateField(default=datetime.date.today)#
    details = models.CharField(max_length=500, default='')
    title = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.city + ', ' + self.street+ ', ' + str(self.publisher)
    
    def toJSON(self):
      return {"id": self.id, 
              "city": self.city , 
              "street": self.street, 
              "rent_price": self.rent_price, 
              "floor": self.floor,
              "partners": self.partners,
              "gender": self.gender,
              "entry_date": self.entry_date.strftime('%Y-%m-%d'),
              "details": self.details,
              "title": self.title,
              "image": self.imagedata_set.all()[0].myurl}
    

    def uploadImages(self,imglst, starting=0):
        bucket = storage.bucket()
        for kk in range(starting,len(imglst)):
            blob = bucket.blob(f'ad_{str(self.id)}_{kk}.jpg')
            blob.upload_from_file(imglst[kk])
            # Opt : if you want to make public access from the URL
            blob.make_public()
            url_img = blob.public_url
            if url_img: self.imagedata_set.create(myurl = url_img)
            print("your file url", url_img)

    
    def updateImages(self,newimg, existimg):
        try:
            bucket = storage.bucket()
            oldimg_lst = [oldimg.myurl for oldimg in self.imagedata_set.all()]
            for oldimg in oldimg_lst:
                if oldimg not in existimg:
                    path = oldimg.replace('https://storage.googleapis.com/dirot-5d085.appspot.com/','')
                    blob = bucket.blob(path)
                    blob.delete()
                    self.imagedata_set.filter(myurl__icontains = path).delete()
                
        finally:
            bucket = storage.bucket()
            myindex, starter = 0,0
            while myindex<6 and starter<len(newimg):
                path = f'ad_{str(self.id)}_{myindex}.jpg'
                if len(self.imagedata_set.filter(myurl__icontains = path).all()) == 0:
                    blob = bucket.blob(path)
                    blob.upload_from_file(newimg[starter])
                    blob.make_public()
                    url_img = blob.public_url
                    print(url_img, 'en li mosag')
                    if url_img: 
                        self.imagedata_set.create(myurl = url_img)
                    starter+=1
                myindex+=1

    def deleteAllImages(self):
        bucket = storage.bucket()
        kk=0
        for im in self.imagedata_set.all():
            blob = bucket.blob(f'ad_{str(self.id)}_{kk}.jpg')
            blob.delete()
            im.delete()
            kk+=1
    
class ImageData(models.Model): 
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    myurl = models.CharField(max_length=250)
        
    def index(self):
        counter = 0
        for img in self.apartment.imagedata_set.order_by('id').all():
            if img == self: 
                return counter
            else: counter +=1
        return counter
    
    def __str__(self):
        return self.myurl
    
    

    