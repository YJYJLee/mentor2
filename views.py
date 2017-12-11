from django.http import HttpResponse
from django.template.context_processors import csrf
from django.template.loader import get_template


def home(request):
    template = get_template("home.html")
    context = {'is_login': request.user.is_authenticated.value}
    context.update(csrf(request))
    return HttpResponse(template.render(context))


def about(request):
    template = get_template('about.html')
    context = {'is_login': request.user.is_authenticated.value}
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def logout_check(request):
    template = get_template('logout.html')
    context={}
    return HttpResponse(template.render(context))