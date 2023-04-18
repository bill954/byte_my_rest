from django.contrib.auth.admin import UserAdmin
from users.models import User, UserProfile
from django.contrib import admin

class UserProfileInLine(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInLine,)
    fieldsets = UserAdmin.fieldsets + (
        (("Custom fields"), {"fields": ("user_type",)}),
    )

admin.site.register(User, CustomUserAdmin)