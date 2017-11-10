from django.contrib import admin
from vinform.models import InformTask, InformType, Inform
from vfast.settings import tinymce_js


class InformTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class InformTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'pubtime', 'color', 'desc', 'url', 'status')


class InformAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'user', 'color', 'desc', 'url')

    class Media:
        js = tinymce_js


admin.site.register(Inform, InformAdmin)
admin.site.register(InformTask, InformTaskAdmin)
admin.site.register(InformType, InformTypeAdmin)
