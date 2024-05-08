from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'global/home.html'

class Error404View(TemplateView):
    template_name = 'Cliente/Error_404.html'
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Registra el error en el logger
            logger.exception("Error 404: %s", e)
            # Re-lanza la excepción para que Django maneje el error como de costumbre
            raise

class Error505View(TemplateView):
    template_name = 'Cliente/Error_404.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()
        def view(request):
            try:
                r = v(request)
                r.render()
                return r
            except Exception as e:
                # Registra el error en el logger
                logger.exception("Error 505: %s", e)
                # Re-lanza la excepción para que Django maneje el error como de costumbre
                raise
        return view 
