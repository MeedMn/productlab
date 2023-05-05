from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.product.models import Product

# Create your models here.
class NewsLetter(models.Model):
    email = models.EmailField(max_length=255)
    def _str_(self):
        return self.email
    
@receiver(post_save, sender=Product)
def hear_signal(sender , instance , **kwargs):
    if (kwargs.get("created")) :
        seller = instance.seller
        seller.save()
        from_email = settings.DEFAULT_EMAIL_FROM
        to_emails = []
        for subscriber in NewsLetter.objects.all():
            to_emails.append(str(subscriber.email))
            print(subscriber.email)

        subject1 = 'New artwork published!'
        text_content1 = 'New artwork added'
        html_content1 = render_to_string('new_artwork_newsletter.html', {'product': instance})
        msg1 = EmailMultiAlternatives(subject1, text_content1, from_email, bcc=to_emails)
        msg1.attach_alternative(html_content1, 'text/html')
        msg1.send()
    return 