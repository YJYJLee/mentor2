from django import forms


class LoginForm(forms.Form):
    id = forms.CharField(label="ID",max_length=12)
    password = forms.CharField(label="PASSWORD" ,max_length=12)

class JoinForm(forms.Form):
    id = forms.CharField(label="ID",max_length=12)
    password = forms.CharField(label="PASSWORD" ,max_length=12,widget=forms.PasswordInput)
    password_check = forms.CharField(label="PASSWORD(again)",min_length=6,max_length=12,required=True,
                                     widget=forms.PasswordInput)
