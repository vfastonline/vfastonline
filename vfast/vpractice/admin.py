from django.contrib import admin
from vpractice.models import Timu, Question, QRcomment, Replay, Attention

# Register your models here.
admin.site.register(Timu)
admin.site.register(Question)
admin.site.register(QRcomment)
admin.site.register(Replay)
admin.site.register(Attention)