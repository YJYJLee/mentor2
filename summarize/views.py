from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.template.context_processors import csrf

from summarize.forms import *
from summarize.models import post
from summarize.textrank import summarize_text

import os
import sys
import urllib.request

def summarize(request):
    if(request.user.is_anonymous()):
        template = get_template('logout.html')
        context={}
        return HttpResponse(template.render(context))
    else:
        template = get_template('summarize.html')
        user_id = request.user
        target = post.objects.filter(author=user_id)
        page_data = Paginator(target,5)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            posts = page_data.page(page)
        except PageNotAnInteger:
            posts = page_data.page(1)
        except EmptyPage:
            posts = page_data.page(page_data.num_pages)

        context = {'post_list': posts,'current_page':int(page),'total_page':range(1,page_data.num_pages+1)}
        context.update(csrf(request))
        return HttpResponse(template.render(context))


def write_form(request):
    template = get_template('writeBoard.html')
    br = WriteForm(request.POST)

    if br.is_valid():
        title = br.cleaned_data['title']
        body = br.cleaned_data['body']
        post.objects.get_or_create(title=title, body=body, author=request.user)
        return redirect("/summarize/sum/")

    context = {'write':WriteForm}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def show_form(request):
    global target
    template = get_template('showBoard.html')
    title = request.GET['title']
    target = post.objects.get(title=title,author=request.user)
    context={'title':target.title, 'body':target.body, 'author':target.author}
    return HttpResponse(template.render(context))

def summarize_form(request):
    global target
    template = get_template('showSummarize.html')
    rate = request.GET['rate']
    context = {}
    rate = int(rate)/100
    sum_text = summarize_text(target.body,rate)
    context={'summarize_text':sum_text,'title':target.title,'rate':rate}
    print(target.title)
    return HttpResponse(template.render(context))

def delete(request):
    global target
    template = get_template('summarize.html')
    target.delete()

    user_id = request.user
    targets = post.objects.filter(author=user_id)
    page_data = Paginator(targets, 5)
    page = request.GET.get('page')
    if page is None:
        page = 1
    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    context = {'post_list': posts, 'current_page': int(page), 'total_page': range(1, page_data.num_pages + 1)}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def translate_form(request):
    global target
    client_id = "JHmTYLs6FZL0Xojw47G4"
    client_secret = "DDuq_NfUIe"
    encText = urllib.parse.quote(target.body)
    translate_data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)


    response = urllib.request.urlopen(request, data=translate_data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    pre_translated = response_body.decode('utf-8')


    template = get_template('showTranslation.html')
    context = {'title':target.title,'translation': pre_translated.split("translatedText\":""\"")[1].split("\"}}}")[0]}

    #p, created = post.objects.get_or_create(title=target.title+"_kor", body=pre_translated.split("translatedText\":""\"")[1].split("\"}}}")[0], author=target.author)

    return HttpResponse(template.render(context))

def modification(request):
    global target
    template = get_template('modify.html')
    if request.method=="POST":
        write = WriteForm(request.POST,instance=target)
    else:
        write = WriteForm(instance=target)
    context={'write':write}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def updateData(request):
    template = get_template('summarize.html')
    br = WriteForm(request.POST)
    if br.is_valid():
        title = br.cleaned_data['title']
        body = br.cleaned_data['body']
        post.objects.filter(title=title, author=request.user).update(body=body)
    return redirect("/summarize/sum/")


def summarize_translate_form(request):
    global target
    client_id = "JHmTYLs6FZL0Xojw47G4"
    client_secret = "DDuq_NfUIe"
    encText = urllib.parse.quote(target.body)
    translate_data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)


    response = urllib.request.urlopen(request, data=translate_data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    pre_translated = response_body.decode('utf-8')
    pre_translated = pre_translated.split("translatedText\":""\"")[1].split("\"}}}")[0]

    template = get_template('showTranslation.html')
    context = {'title':target.title,'translation': pre_translated.replace("\\n"," ")}

    #p, created = post.objects.get_or_create(title=target.title+"_kor", body=pre_translated.split("translatedText\":""\"")[1].split("\"}}}")[0], author=target.author)

    return HttpResponse(template.render(context))