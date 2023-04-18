import csv
import os
from django.core.files import File
import requests
from apps.product.models import Category, Product
from apps.seller.models import Seller
from PIL import Image
from io import BytesIO
from django.core.validators import MaxValueValidator, MinValueValidator
import random
import datetime


def save_product(row):
    category, created = Category.objects.get_or_create(title=row['category'], slug=row['category'].lower())
    seller = Seller.objects.filter(name="ProductLab01")
    product = Product.objects.create(
        category=category,
        seller=seller[0],
        title=row['title'],
        slug=row['title'].lower().replace(" ", "-"),
        description="Good Product",
        price=row['price'],
        image=None,
        code_ref=row['code_ref'],
        rating=row['rating']
    )
    if row['image']:
        img_url = row['image']
        img_name = os.path.basename(img_url)
        img_ext = os.path.splitext(img_name)[1]
        img_filename = f"{product.id}{img_ext}"
        img_data = requests.get(img_url).content

        with open(f"C:/Users/menfa/Desktop/ProductLab/productlab/media/{img_filename}", 'wb') as f:
            f.write(img_data)

        with open(f"C:/Users/menfa/Desktop/ProductLab/productlab/media/{img_filename}", 'rb') as f:
            product.image.save(img_filename, File(f), save=True)

        product.save()

    if product.image:
        thumbnail = product.make_thumbnail(product.image)
        product.thumbnail.save(thumbnail.name, thumbnail, save=True)
        product.save()

    return product


with open('C:\\Users\\menfa\\Desktop\\ProductLab\\productlab\\apps\\product\\products.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        save_product(row)