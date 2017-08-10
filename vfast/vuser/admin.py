from django.contrib import admin
from vuser.models import User, DailyTask, PtoP

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname', 'sex', 'city', 'totalscore','realname', 'intro', 'role')
    search_fields = ('email',)


class PtoPAdmin(admin.ModelAdmin):
    list_display = ('follow', 'followed')


class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'video_name',  'createtime', 'video_id', 'vtype', 'vtime')

# admin.site.register(User, UserAdmin)
# admin.site.register(DailyTask, DailyTaskAdmin)
# admin.site.register(PtoP, PtoPAdmin)

