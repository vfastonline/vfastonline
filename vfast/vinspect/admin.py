from django.contrib import admin

from vfast.settings import tinymce_js
from vinspect.models import Inspect, InspectOption


class InspectOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'A', 'B', 'C', 'D')

    class Media:
        js = tinymce_js


admin.site.register(Inspect)
admin.site.register(InspectOption, InspectOptionAdmin)
