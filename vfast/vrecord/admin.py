from django.contrib import admin
from vrecord.models import Score, WatchRecord, WatchCourse

# Register your models here.

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'technology', 'createtime']


class WatchcourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'createtime']


class WatchRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'course', 'video_process', 'status', 'createtime']


# admin.site.register(Score, ScoreAdmin)
# admin.site.register(WatchRecord, WatchRecordAdmin)
# admin.site.register(WatchCourse, WatchcourseAdmin)