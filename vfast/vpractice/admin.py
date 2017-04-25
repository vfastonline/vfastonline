from django.contrib import admin
from vpractice.models import Timu, Question, QRcomment, Replay, Attention

# Register your models here.
class TimuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'answer', 'tips', 'A', 'B', 'C', 'D', 'E', 'F', 'sequence')
    search_fields = ('title', )


admin.site.register(Timu, TimuAdmin)
admin.site.register(Question)
admin.site.register(QRcomment)
admin.site.register(Replay)
admin.site.register(Attention)