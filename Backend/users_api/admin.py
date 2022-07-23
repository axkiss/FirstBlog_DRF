from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'group', 'is_staff')
    list_per_page = 25

    @admin.display(description='FULL NAME')
    def full_name(self, obj):
        return obj.get_full_name()

    @admin.display(description='GROUP')
    def group(self, obj):
        return obj.get_group()
