from django.contrib import admin
from vinform.models import InformTask, InformType, Inform

# Register your models here.


class InformTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class InformTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubtime', 'color', 'desc', 'url', 'status')

class InformAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'user', 'color', 'desc', 'url')

admin.site.register(Inform, InformAdmin)
admin.site.register(InformTask, InformTaskAdmin)
admin.site.register(InformType, InformTypeAdmin)
