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
      images = {k.myurl for k in self.imagedata_set.all()}
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
              "image": str(images)}
    

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


    def contain(self, str_value, lst):
        for linr in lst:
            if str_value in linr: return True
        return False
    
    def updateImages(self, newimg, existimg):
        multilong = len(self.imagedata_set.all())
        bucket = storage.bucket()
        for kk in range(multilong):
            if not self.contain(f'ad_{str(self.id)}_{kk}.jpg', existimg):
                blob = bucket.blob(f'ad_{str(self.id)}_{kk}.jpg')
                if newimg:             
                    blob.upload_from_file(newimg.pop())
                else: 
                    deletelst = self.imagedata_set.filter(myurl__icontains = f'ad_{str(self.id)}_{kk}.jpg')
                    if deletelst:
                        for item in deletelst: item.delete()
                    blob.delete()
        
        while(newimg and multilong<6):
            blob = bucket.blob(f'ad_{str(self.id)}_{multilong}.jpg')
            blob.upload_from_file(newimg.pop())
            blob.make_public()
            url_img = blob.public_url
            if url_img: self.imagedata_set.create(myurl = url_img)
            multilong+=1





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
    
    

    