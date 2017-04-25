#!encoding:utf-8
from django.contrib import admin
from vperm.models import Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'rolename')

admin.site.register(Role, RoleAdmin)