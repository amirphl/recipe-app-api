from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _


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


# 'last_logout', todo

admin.site.register(get_user_model(), UserAdm)
