from django import forms
from views import *

resultText="hello"

class stt(forms.Form):
    body = forms.CharField(label="body",widget=forms.Textarea)


class WriteForm(forms.Form):

    title = forms.CharField(label="title",max_length=1024)
    #print(global_var.punctuation_result)
    #global gloglo
    #x=getGlobal.x
    global resultText

    if resultText:
        body = forms.CharField(label="body", initial=resultText, widget=forms.Textarea)
    else:
        body = forms.CharField(label="body", widget=forms.Textarea)
