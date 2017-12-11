from django.conf.urls import url

from summarize.views import summarize, write_form, show_form, summarize_form, translate_form,delete,modification,updateData

urlpatterns = [
    url(r'^sum/$', summarize),
    url(r'^write_form/$', write_form),
    url(r'^show_form/$',show_form),
    url(r'^summarize_form/$',summarize_form),
    url(r'^translate_form/$',translate_form),
    url(r'^summarize_translate_form/$',translate_form),
    url(r'^del/$',delete),
    url(r'^modify/$',modification),
    url(r'^updateData/$',updateData),
]
