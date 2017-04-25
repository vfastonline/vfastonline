from django.contrib import admin
from vrecord.models import Score, WatchRecord, WatchCourse

# Register your models here.
admin.site.register(Score)
admin.site.register(WatchRecord)
admin.site.register(WatchCourse)