from django.contrib import admin
from vcourse.models import Path, TypeFunc, TypeProgram, Course, Video
# Register your models here.

admin.site.register(Path)
admin.site.register(TypeFunc)
admin.site.register(Course)
admin.site.register(TypeProgram)
admin.site.register(Video)
