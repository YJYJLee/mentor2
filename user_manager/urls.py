from django.conf.urls import url

from user_manager.views import login, logout_view, login_validate, join_page

urlpatterns = [
    url(r'^login/$', login),
    url(r'^logout/$', logout_view),
    url(r'^login/validate/$', login_validate),
    url(r'^join/$', join_page),
]