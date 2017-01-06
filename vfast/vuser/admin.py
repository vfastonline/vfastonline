from django.contrib import admin
from vuser.models import User, Badge, UserBadge

# Register your models here.
admin.site.register(User)
admin.site.register(UserBadge)
admin.site.register(Badge)