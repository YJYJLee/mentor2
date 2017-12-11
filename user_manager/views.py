from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.template.loader import get_template
from user_manager.forms import LoginForm, JoinForm


def login(request):
    template = get_template('login.html')
    context = {'login_form':LoginForm(),'is_login':request.user.is_authenticated.value}
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def login_validate(request):
    login_form_data = LoginForm(request.POST)

    if login_form_data.is_valid():
        user = auth.authenticate(request, username=login_form_data.cleaned_data['id'],password=login_form_data.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                auth.login(request,user)

                return redirect('/')
        else:
            return  HttpResponse('invalid user or password')

    return HttpResponse('unknown error')

def join_page(request):
    if request.method == 'POST':
        form_data = JoinForm(request.POST)

        if form_data.is_valid():
            pass1 = form_data.cleaned_data['password']
            pass2 = form_data.cleaned_data['password_check']
            if pass1 == pass2:
                username = form_data.cleaned_data['id']
                password = form_data.cleaned_data['password']
                User.objects.create_user(username=username,password=password)

                return redirect('/user/login/')
            else:
                return redirect('/user/join/')
        else:
            return redirect('/user/join/')
    else:
        form_data = JoinForm()

    template = get_template('join.html')
    context = {'join_form':JoinForm(),'is_login':request.user.is_authenticated.value}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def init(request):
    return redirect('/home/')

def home(request):
    template = get_template('home.html')
    context = {'is_login':request.user.is_authenticated.value}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def logout_view(request):
    if(request.user.is_anonymous()):
        template = get_template('logout_form.html')
        context={}
        return HttpResponse(template.render(context))
    else:
        logout(request)
        return redirect('/user/login/')