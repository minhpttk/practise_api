from django.contrib import admin
from .models import Employee
from django.utils.safestring import mark_safe
# Register your models here.


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'date_of_birth', 'gender', 'display_profile_picture']

    def display_profile_picture(self, obj):
        return mark_safe('<img src="{0}" width="50px" height="50px" />'.format(obj.profile_picture.url))
    display_profile_picture.short_description = 'Profile Picture'
