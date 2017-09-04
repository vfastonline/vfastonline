from django.contrib import admin
from vinspect.models import Inspect, InspectOption
# Register your models here.


class InspectOptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'A', 'B', 'C', 'D')


admin.site.register(Inspect)
admin.site.register(InspectOption, InspectOptionAdmin)