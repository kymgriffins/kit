# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


def index(request):
    with open('index.html', 'r') as f:
        html_content = f.read()
    return HttpResponse(html_content)