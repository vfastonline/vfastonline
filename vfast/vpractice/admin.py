from django.contrib import admin
from vpractice.models import Timu, Question, QRcomment, Replay, Attention, RepaType

# Register your models here.
class TimuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answer', 'tips', 'A', 'B', 'C', 'D', 'E', 'F', 'sequence')
    search_fields = ('title', )


class ReplayAdmin(admin.ModelAdmin):
    list_display = ('question', 'replay_user', 'like', 'dislike','score', 'createtime')


admin.site.register(Timu, TimuAdmin)
admin.site.register(Question)
admin.site.register(QRcomment)
admin.site.register(Replay, ReplayAdmin)
admin.site.register(Attention)
admin.site.register(RepaType)


