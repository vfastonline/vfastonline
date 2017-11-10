from django.contrib import admin

from vcompany.models import Company
from vfast.settings import tinymce_js


class CompanyModel(admin.ModelAdmin):
    class Media:
        js = tinymce_js


admin.site.register(Company, CompanyModel)
