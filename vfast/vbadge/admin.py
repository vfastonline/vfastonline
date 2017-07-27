from django.contrib import admin
from vbadge.models import UserBadge, Badge
# Register your models here.

class BadgeModel(admin.ModelAdmin):
    list_display = ('id', 'badgename', 'badgeurl', 'createtime','course_id')
    search_fields = ('badgename',)

class UserBadgeModel(admin.ModelAdmin):
    list_display = ('id', 'badge')

admin.site.register(UserBadge, UserBadgeModel)
admin.site.register(Badge, BadgeModel)