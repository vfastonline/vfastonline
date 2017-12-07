from django.contrib import admin
from vpractice.models import Timu, Question, QRcomment, Replay, Attention, RepaType
from vfast.settings import tinymce_js


class TimuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answer', 'tips', 'A', 'B', 'C', 'D', 'E', 'F', 'sequence')
    search_fields = ('title',)


class ReplayAdmin(admin.ModelAdmin):
    list_display = ('question', 'replay_user', 'like', 'dislike', 'score', 'createtime')

    class Media:
        js = tinymce_js


class QuestionAdmin(admin.ModelAdmin):
    class Media:
        js = tinymce_js


admin.site.register(Timu, TimuAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Replay, ReplayAdmin)
# admin.site.register(QRcomment)
# admin.site.register(Attention)
# admin.site.register(RepaType)
