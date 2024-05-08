from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'global/home.html'

class Error404View(TemplateView):
    template_name = 'Cliente/Error_404.html'

class Error505View(TemplateView):
    template_name = 'Cliente/Error_404.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()
        def view(request):
            r = v(request)
            r.render()
            return r
        return view
