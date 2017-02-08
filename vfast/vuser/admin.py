from django.contrib import admin
from vuser.models import User, Role, Company

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Company)
