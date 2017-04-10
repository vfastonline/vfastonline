from django.contrib import admin
from vcourse.models import Path, Program, Course, Video, UserPath
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','name','vtime','score','scorepeople','course','createtime')
    search_fields = ('name', 'createtime',)

admin.site.register(Path)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Video, VideoAdmin)
admin.site.register(UserPath)
