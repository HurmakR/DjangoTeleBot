from django.contrib import admin

# Register your models here.
from .models import Log, Parts, Cat, Model, Partprice

class ModelAdmin(admin.ModelAdmin):
    search_fields = ['modelname', 'modelcat__category', ]
    ordering = ['modelname']

class PartpriceAdmin(admin.ModelAdmin):
    search_fields = ['idmodel__modelname', 'idpart__partname', ]
    ordering = ['idmodel__modelname']


admin.site.register(Log)
admin.site.register(Parts)
admin.site.register(Cat)
admin.site.register(Model, ModelAdmin)
admin.site.register(Partprice, PartpriceAdmin)
