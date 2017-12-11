from django import forms
from .models import post

class WriteForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title','body']