from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'full_name',
        'phone',
        'is_active',
        'date_joined',

    )
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                "full_name",
                "email",
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','email', 'full_name', 'phone',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': (
             "pupils",
                "full_name",
                "phone",
                "avatar",
         )}
         ),
        ('Permissions', {'fields': ('is_staff','is_support', 'is_superuser', 'groups',)}),)


admin.site.register(User,UserAdmin)
admin.site.register(Pupil)






