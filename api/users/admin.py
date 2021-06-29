from django.contrib import admin

from api.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", )

admin.site.register(User)
