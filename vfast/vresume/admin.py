from django.contrib import admin

from vresume.models import *


class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        "years_of_service",
        "education",
        "expect_salary_low",
        "expect_salary_high",
        "work_status",
        "company",
        "position",
        "my_advantage",
    )
    search_fields = ('years_of_service', "education")


class CareerObjectiveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        "position",
        "expect_salary_low",
        "expect_salary_high",
        "city",
        "industry",
    )
    search_fields = ('position',)


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        "company",
        "position",
        "start_time",
        "end_time",
        "content",
    )
    search_fields = ('company',)


class ProjectExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        "project_name",
        "role",
        "url",
        "start_time",
        "end_time",
        "description",
    )
    search_fields = ('project_name',)


class EducationExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        "school",
        "discipline",
        "education",
        "start_time",
        "end_time",
        "experience_at_school",
    )
    search_fields = ('school',)


admin.site.register(Resume, ResumeAdmin)
admin.site.register(CareerObjective, CareerObjectiveAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(ProjectExperience, ProjectExperienceAdmin)
admin.site.register(EducationExperience, EducationExperienceAdmin)
