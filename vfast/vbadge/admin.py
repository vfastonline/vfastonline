from django.contrib import admin
from badge.models import UserBadge, Badge
# Register your models here.

admin.site.register(UserBadge)
admin.site.register(Badge)