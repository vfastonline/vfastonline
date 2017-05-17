from django.contrib import admin
from vinform.models import InformTask, InformType, Inform

# Register your models here.


class InformTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class InformTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubtime', 'color', 'desc', 'url',)

admin.site.register(Inform)
admin.site.register(InformTask, InformTaskAdmin)
admin.site.register(InformType, InformTypeAdmin)
