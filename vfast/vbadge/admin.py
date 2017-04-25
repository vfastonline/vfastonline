from django.contrib import admin
from vbadge.models import UserBadge, Badge
# Register your models here.

class BadgeModel(admin.ModelAdmin):
    list_display = ('id', 'badgename', 'badgeurl', 'createtime','course_id')
    search_fields = ('badgename',)

admin.site.register(UserBadge)
admin.site.register(Badge, BadgeModel)