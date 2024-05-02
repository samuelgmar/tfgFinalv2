from django.contrib import admin
from apps.Global.models import UsuarioAdminstracion, LotteryAdministration,Order, SliderImage
# Register your models here.
admin.site.register(UsuarioAdminstracion)
admin.site.register(LotteryAdministration)
admin.site.register(Order)
admin.site.register(SliderImage)
