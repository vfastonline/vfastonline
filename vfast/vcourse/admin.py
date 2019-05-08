# encoding: utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from django.contrib import admin

from vcourse.models import *
from vfast.settings import tinymce_js


# Register your models here.

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'section', 'vtime', 'score', 'scorepeople', 'course', 'createtime', 'sequence')
    search_fields = ('name', 'createtime',)
    ordering = ('-course', 'sequence')

    class Media:
        js = tinymce_js


class PathAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'intrv', 'jobscount', 'pathimg', 'totaltime', 'createtime', 'color')
    search_fields = ('name',)
    filter_horizontal = ('course',)
    readonly_fields = ('p_sequence',)

    class Media:
        js = tinymce_js


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'totaltime', 'difficult', 'pubstatus', 'teach', 'tech', 'tag')
    search_fields = ('name',)

    class Media:
        js = tinymce_js


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'desc')
    search_fields = ('name',)

    class Media:
        js = tinymce_js


class UserPathAdmin(admin.ModelAdmin):
    list_display = ('user', 'path')


class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'question', 'answer', 'language')
    search_fields = ('video', 'question',)

    class Media:
        js = tinymce_js


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'name', 'weight')
    search_fields = ('path', 'name',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc', 'course', 'skill')
    search_fields = ('title', 'course',)

    class Media:
        js = tinymce_js


class PathCourseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'path', 'course', 'sequence_number')
    search_fields = ('path__name', 'course__name')


admin.site.register(Path, PathAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(PathCourseOrder, PathCourseOrderAdmin)
