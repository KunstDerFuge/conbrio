import glob
import os

from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template('frontend/base.html')
    return HttpResponse(template.render({}, request))


def app(request):
    try:
        print(os.listdir())
        os.chdir(os.path.join('conbrio-frontend', 'build'))
        js_chunks = glob.glob(os.path.join('static', 'js', '*.js'))
        template = loader.get_template('frontend/app.html')
        return HttpResponse(template.render({'js_chunks': js_chunks}, request))
    finally:
        os.chdir(os.path.join('..', '..'))

