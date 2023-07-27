from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Apartment(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(null=False, max_length=100)
    street = models.CharField(max_length=100)
    rent_price = models.IntegerField(default=0)
    floor = models.IntegerField(default=0)
    partners = models.IntegerField(default=0)
    gender = models.IntegerField(default=0)
    entry_date = models.DateField(default=datetime.date.today)
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
    
class ImageData(models.Model): 
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    myurl = models.CharField(max_length=250)

    def __str__(self):
        return self.myurl
    
    

    