from django import forms
from .models import Product
from django.forms import ModelForm

class ProductForms(ModelForm):
    price = forms.FloatField(widget=forms.NumberInput(attrs={'min':0,'max':9999}))
    class Meta:
        model = Product
        fields = ('category','image','title','description','price','qte')
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class ProductImageForm(forms.Form):
	more_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
	more_images.required = False