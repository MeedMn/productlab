import uuid 
from turtle import title
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django_resized import ResizedImageField
from base64 import *
import datetime, random
from qrcode import *
from django.core.validators import MaxValueValidator, MinValueValidator
from apps.seller.models import Seller

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return self.title

def random_int():
    return random.randint(0, 999999)
 
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2,validators=[MaxValueValidator(10000),MinValueValidator(1)])
    date_added = models.DateTimeField(default=datetime.datetime.now , blank=True)
    image = models.ImageField(upload_to='uploads/', blank=False, null=False)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=False)
    code_ref = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=5,decimal_places=2,null=True)
    qte = models.IntegerField(default=10)
    ordering = models.IntegerField(default=random_int)
    
    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return self.title

    def generate_ref(self):
        productName_bytes = self.title.encode()
        base64_bytes = b64encode(productName_bytes)
        base64_string = base64_bytes.decode()
        self.code_ref = base64_string[:10]

    def make_thumbnail(self,image,size=(370,340)):
        img = Image.open(image)
        src_img = img.convert('RGB')
        src_img.thumbnail(size)
        thumb_io = BytesIO()
        src_img.save(thumb_io, 'JPEG',quality=85)
        thumbnail = File(thumb_io,name=image.name)
        return thumbnail

    def get_Thumbnail(self):
        if self.thumbnail :
            return self.thumbnail.url
        else:
            if self.image :
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            
            
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def make_thumbnail(self,image,size=(300, 200)):
        img = Image.open(image)
        src_img = img.convert('RGB')
        src_img.thumbnail(size)
        thumb_io = BytesIO()
        src_img.save(thumb_io, 'JPEG',quality=85)
        thumbnail = File(thumb_io,name=image.name)
        return thumbnail

    def get_Thumbnail(self):
        if self.thumbnail :
            return self.thumbnail.url
        else:
            if self.image :
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

class Comment(models.Model):
    user1 = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=datetime.datetime.now , blank=True)
    
    class Meta: 
        ordering = ('-date_created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.user1, self.product.title)