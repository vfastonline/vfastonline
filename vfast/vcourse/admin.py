from django.contrib import admin
from vcourse.models import Path, Program, Course, Video
# Register your models here.

admin.site.register(Path)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Video)
