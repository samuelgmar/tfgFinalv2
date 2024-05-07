from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'global/home.html'

class Error404View(TemplateView):
    template_name = 'global/error_404.html'

