from django.contrib import admin
from vbadge.models import UserBadge, Badge
# Register your models here.

class BadgeModel(admin.ModelAdmin):
    list_display = ('id', 'badgename', 'createtime','course_id', 'path_id', 'large_url', 'small_url')
    search_fields = ('badgename',)

class UserBadgeModel(admin.ModelAdmin):
    list_display = ('id',  'badge')

admin.site.register(UserBadge, UserBadgeModel)
admin.site.register(Badge, BadgeModel)