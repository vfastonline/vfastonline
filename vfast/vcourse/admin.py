from django.contrib import admin
from vcourse.models import Path, Technology, Course, Video, UserPath, Section
# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','name','vtime','score','scorepeople','course','createtime')
    search_fields = ('name', 'createtime',)

class PathAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'intrv', 'jobscount', 'pathimg', 'totaltime', 'createtime', 'color' )
    search_fields = ('name', )

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'totaltime', 'difficult', 'pubstatus', 'teach', 'tech', 'tag')
    search_fields = ('name',)

class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'desc')
    search_fields = ('name', )


admin.site.register(Path, PathAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UserPath)
admin.site.register(Section)
