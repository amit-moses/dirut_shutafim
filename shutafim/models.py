from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from firebase_admin import credentials,initialize_app, storage
from django.conf import settings
import random


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
    title = models.CharField(max_length=24, default='')
    kosher = models.IntegerField(default=0)
    agree_mail = models.BooleanField(default=True)

    def __str__(self):
        if self.street: return self.city + ', ' + self.street
        return self.city
    
    def get_url(self):
        return f'{settings.MY_URL}apr/{self.id}'
    
    def short_title(self):
      my_title = self.title
      if len(my_title)> 22: my_title = my_title[:22]+'...'
      elif not my_title: my_title = '  '
      return my_title
    
    def short_details(self):
      my_content = self.details
      if len(my_content)> 25: my_content = my_content[:25]+'...'
      elif not my_content: my_content = '  '
      return my_content
    
    def get_date_format(self):
        return self.entry_date.strftime('%d/%m/%Y')
    def toJSON(self):
      return {"id": self.id, 
              "city": self.city , 
              "street": self.street, 
              "rent_price": self.rent_price, 
              "floor": self.floor,
              "partners": self.partners,
              "gender": self.gender,
              "entry_date": self.entry_date.strftime('%Y-%m-%d'),
              "details": self.short_details(),
              "title": self.short_title(),
              "kosher": self.kosher,
              "image": self.imagedata_set.all()[0].myurl}

    
    def updateImages_1(self,existimg):
        bucket = storage.bucket()
        oldimg_lst = [oldimg.myurl for oldimg in self.imagedata_set.all()]
        for oldimg in oldimg_lst:
            if oldimg not in existimg:
                path = oldimg.replace('https://storage.googleapis.com/diro-ac902.appspot.com/','')
                blob = bucket.blob(path)
                blob.delete()
                self.imagedata_set.filter(myurl__icontains = path).delete()

    def make_random_name(self):
        options = 'abcdefg12345hij6789'
        newId = [options[random.randint(0, len(options)-1)] for k in range(6)]
        return ''.join(newId)
    

    def uploadImages(self,newimg):
        bucket = storage.bucket()
        for kk in range(len(newimg)):
            path = f'ad{self.id}_{self.make_random_name()}'
            while self.imagedata_set.filter(myurl__icontains = path).all():
                path = f'ad{self.id}_{self.make_random_name()}'
            blob = bucket.blob(path)
            blob.upload_from_file(newimg[kk],content_type='image/jpg')
            blob.make_public()
            url_img = blob.public_url
            if url_img: self.imagedata_set.create(myurl = url_img)

    def updateImages(self,newimg, existimg):
        self.updateImages_1(existimg)
        self.uploadImages(newimg)

    def deleteAllImages(self):
        bucket = storage.bucket()
        for im in self.imagedata_set.all():
            path = im.myurl.replace('https://storage.googleapis.com/diro-ac902.appspot.com/','')
            blob = bucket.blob(path)
            blob.delete()
            im.delete()
    
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