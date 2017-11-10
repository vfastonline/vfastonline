# encoding: utf8
from django.contrib import admin

from vcourse.models import Path, Technology, Course, Video, Section, Faq, Skill
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
    list_display = ('video', 'question', 'answer', 'language')

    class Media:
        js = tinymce_js


class SectionAdmin(admin.ModelAdmin):
    class Media:
        js = tinymce_js


admin.site.register(Path, PathAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Skill)
