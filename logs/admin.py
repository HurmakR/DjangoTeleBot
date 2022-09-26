from django.contrib import admin

# Register your models here.
from .models import Log, Parts, Cat, Model, Partprice

admin.site.register(Log)
admin.site.register(Parts)
admin.site.register(Cat)
admin.site.register(Model)
admin.site.register(Partprice)