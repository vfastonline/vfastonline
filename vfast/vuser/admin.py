from django.contrib import admin
from vuser.models import User, DailyTask, PtoP

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'sex', 'city', 'totalscore','realname', 'intro', 'role')
    search_fields = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(DailyTask)
admin.site.register(PtoP)
