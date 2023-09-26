from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import LentaUser


class UserAdmin(UserAdmin):
    model = LentaUser
    list_display = ('id', 'email', 'username')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')
    ordering = ('username',)


admin.site.register(LentaUser, UserAdmin)
