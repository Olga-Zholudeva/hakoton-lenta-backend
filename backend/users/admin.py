from django.contrib import admin

from users.models import LentaUser


@admin.register(LentaUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')
    ordering = ('username',)
