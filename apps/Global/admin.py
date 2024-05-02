from django.contrib import admin
from apps.Global.models import RedSocial,cart, Usuario, Product, Category, Pack, contactoUs
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Pack)
admin.site.register(contactoUs)
admin.site.register(cart)
admin.site.register(RedSocial)