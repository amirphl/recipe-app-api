from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core import models
from django.contrib.auth import get_user_model


class UserAdm(UserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']


admin.site.register(get_user_model(), UserAdm)
