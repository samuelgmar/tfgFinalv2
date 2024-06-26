from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.Cliente.views import CustomPasswordResetDoneView
from apps.Global.views import Error404View, Error505View
from django.conf.urls import handler404, handler500
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    #General panel
    path('', include(('apps.Global.urls','LotoGlobal'))),
    path('forgot_password_sent_admin/', auth_views.PasswordResetDoneView.as_view(template_name="Administracion/reset_password_sent.html"), name='password_reset_done'),
    path('forgot_password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="Administracion/resetPasswordComplete.html"), name='password_reset_complete'),
    #Creador app control
    path('admin/admin/', admin.site.urls),
    #Administracion panel
    path('admin/<str:nombre_administracion>/', include(('apps.Administracion.urls', 'LotoAdministracion'))),
    #Cliente panel
    path('<str:nombre_administracion>/', include(('apps.Cliente.urls','LotoCliente'))),
    #cookies
    path("cookies/", include("cookie_consent.urls")),
]


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


handler404 = Error404View.as_view()
handler500 = Error505View.as_error_view()
