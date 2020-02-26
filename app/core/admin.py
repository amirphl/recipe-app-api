from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from core import models


class UserAdm(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (  # a section, None is title
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )


# 'last_logout', todo
# edit page ?

admin.site.register(get_user_model(), UserAdm)
admin.site.register(models.Tag)
