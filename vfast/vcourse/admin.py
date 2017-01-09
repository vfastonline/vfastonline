from django.contrib import admin
from vcourse.models import Path, CourseType, Course, CourseClass, Video
# Register your models here.

admin.site.register(Path)
admin.site.register(CourseClass)
admin.site.register(Course)
admin.site.register(CourseType)
admin.site.register(Video)
