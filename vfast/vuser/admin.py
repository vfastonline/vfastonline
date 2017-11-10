from django.contrib import admin
from vuser.models import User, DailyTask, PtoP, Userplan
from vfast.settings import tinymce_js


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname', 'phone', 'sex', 'city', 'totalscore', 'realname', 'intro', 'role')
    search_fields = ('email',)

    class Media:
        js = tinymce_js


class UserplanAdmin(admin.ModelAdmin):
    class Media:
        js = tinymce_js


class PtoPAdmin(admin.ModelAdmin):
    list_display = ('follow', 'followed')


class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'video_name', 'createtime', 'video_id', 'vtype', 'vtime')


admin.site.register(User, UserAdmin)
admin.site.register(Userplan, UserplanAdmin)
# admin.site.register(DailyTask, DailyTaskAdmin)
# admin.site.register(PtoP, PtoPAdmin)
