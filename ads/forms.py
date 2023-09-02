from django import forms
from .models import Ad, Review


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'text', 'category', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
