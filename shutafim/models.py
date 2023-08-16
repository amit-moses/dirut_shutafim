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
    type = models.IntegerField(default=0)
    update = models.DateTimeField(default=timezone.now)

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
    
    def get_first_img(self):
        if self.imagedata_set.all(): return self.imagedata_set.all()[0].myurl
        else: return 'https://firebasestorage.googleapis.com/v0/b/diro-ac902.appspot.com/o/no-image-icon-23500.jpg?alt=media&token=a1d5a015-bf2e-489d-988a-6e143a76b8be'
    
    def toJSON(self):
      return {"id": self.id, 
              "city": self.city,
              "street": self.street,
              "details": self.short_details(),
              "title": self.short_title(),
              "image": self.get_first_img()}

    def delete_1_image(self, im):
        bucket = storage.bucket()
        if im.internal:
            path = im.myurl.replace('https://storage.googleapis.com/diro-ac902.appspot.com/','')
            blob = bucket.blob(path)
            blob.delete()
        im.delete()
        
    def updateImages_1(self,existimg):
        # oldimg_lst = [oldimg.myurl for oldimg in self.imagedata_set.all()]
        for oldimg in self.imagedata_set.all():
            if oldimg.myurl not in existimg:
                self.delete_1_image(oldimg)

    def make_random_name(self):
        options = 'abcdefg12345hij6789r'
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
        for im in self.imagedata_set.all():
            self.delete_1_image(im)
    
    def set_update(self):
        self.update = timezone.now()
        self.save()
    
    def is_update(self):
        return timezone.now() - self.update < datetime.timedelta(hours=24)

class ImageData(models.Model): 
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    myurl = models.CharField(max_length=250)
    internal = models.BooleanField(default=True)
        
    def index(self):
        counter = 0
        for img in self.apartment.imagedata_set.order_by('id').all():
            if img == self: 
                return counter
            else: counter +=1
        return counter
    
    def __str__(self):
        return self.myurl
    
class Messages(models.Model):
    user_to = models.ForeignKey(User, on_delete=models.CASCADE) 
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    mes_content = models.CharField(null=False, max_length=500)
    mes_from = models.CharField(null=False, max_length=100)
    mes_contact = models.CharField(null=False, max_length=100)
    mes_read = models.BooleanField(default=False)

    def read_set(self):
        if self.mes_read: return False
        else:
            self.mes_read = True
            self.save()
            return True
    
    def get_date_format(self):
        return self.pub_date.strftime('%d/%m/%Y %H:%M')
    
    def get_new_mes(self):
        return len(self.user_to.messages_set.filter(mes_read = False).all())
    
    def get_all_mes(self):
        return self.user_to.messages_set.order_by('-id')
    
    def __str__(self):
        return self.mes_from