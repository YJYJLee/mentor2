from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^speechToText/$', views.speechToText),
    url(r'^$', views.speechToText, name='speechToText'),
    url(r'^pun/$', views.punctuation,name='pun'),
    url(r'^youtube_url/$', views.youtube_url, name='youtube_url'),
    url(r'^youtube_url/get_youtube$', views.get_youtube, name='youtube_url'),
    url(r'^youtube_url/get_caption$', views.get_caption),
    url(r'^record/$', views.record),
]