from django.shortcuts import render, redirect
# Create your views here.
import requests
from speechToText.forms import *
from summarize.models import post
import httplib2
import os
import sys

#from apiclient.discovery import build_from_document
#from apiclient.errors import HttpError
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.file import Storage
#from oauth2client.tools import argparser, run_flow


def speechToText(request):
    if (request.user.is_anonymous()):
        template = get_template('logout.html')
        context = {}
        return HttpResponse(template.render(context))
    else:
        template = get_template('index.html')
        context={}
        return HttpResponse(template.render(context))

def punctuation(request):
    global request_data;
    global record_title;

    if request.is_ajax():
        request_data = request.GET['speech_result']
        record_title = request.GET['record_title']
    else:
        print('whynot')
    data = [
        ('text', request_data),
    ]

    result = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)

    template = get_template('showPunctuation.html')
    context = {'punctuation':result.text}
    p, created = post.objects.get_or_create(title=record_title,body=result.text,author=request.user)

    return HttpResponse(template.render(context))

def youtube_url(request):
    template = get_template('youtube_url.html')
    context={}
    return HttpResponse(template.render(context))


    #return HttpResponse("<script src='{src}'></script>".format(
    #    src = staticfiles.static('/speechToText/templates/app.js')))

def get_youtube(request):
    global request_url;

    if request.is_ajax():
        request_url = request.GET['youtube_url']
    else:
        print('whynot')
    data = [
        ('text', request_url),
    ]

    #result = requests.post('http://downsub.com/', url=request_url)

    template = get_template('showPunctuation.html')
    context = {}

    return HttpResponse(template.render(context))

def get_caption(request):
    global whole_url;

    if request.is_ajax():
        whole_url = request.GET['whole_url']
    else:
        print('whynot')


    #caption="https: // www.googleapis.com / youtube / v3 / captions?part = snippet & videoId ="+ +"& key =AIzaSyDXIew-yhZ7bjV5-O0BzN_I-WyqZQqvmxU"
    #print(caption)

    link="http://video.google.com/timedtext?lang=en&v="+whole_url.split("?v=")[1].split("&")[0]+"&track=asr"
    content_html_pre = requests.get(link)
    content_html=content_html_pre.text
    #print(content_html.split("</script>")[1])
    srt_content=content_html.split("<transcript>")[1]
    srt_content=srt_content.replace("&amp;#39;","'")
    srt_content = srt_content.replace("&amp;quot;", "\"")

    final_script=''
    while len(srt_content) != 0:
        start=srt_content.find(">")
        end=srt_content.find("</text>")
        final_script +=srt_content[start+1:end]
        final_script += " "
        srt_content=srt_content[end+7:]

    title_tmp="Youtube_id_is"+whole_url.split("?v=")[1].split("&")[0]

    if post.objects.filter(title=title_tmp).count() == 0:
        restaurant = post.objects.create(title=title_tmp, body=final_script, author=request.user)

    #p,created=post.objects.get_or_create(title=title_tmp, body=final_script, author=request.user)


    template = get_template('showYoutube.html')
    context = {'youtube_caption':final_script,'youtube_id':whole_url.split("?v=")[1].split("&")[0]}

    return HttpResponse(template.render(context))

def record(request):
    if (request.user.is_anonymous()):
        template = get_template('recording/index_rec.html')
        context = {}
        return HttpResponse(template.render(context))
    else:
        template = get_template('recording/index_rec.html')
        context={}
        return HttpResponse(template.render(context))
