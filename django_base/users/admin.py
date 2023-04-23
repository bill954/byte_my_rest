from django.contrib.auth.admin import UserAdmin
from users.models import User, UserProfile, UserDocumentation
from django.contrib import admin

@admin.register(UserDocumentation)
class UserDocumentationAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'document_identifier', 'status')

class UserProfileInLine(admin.StackedInline):
    model = UserProfile

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInLine,)
    fieldsets = UserAdmin.fieldsets + (
        (("Custom fields"), {"fields": ("user_type",)}),
    )

admin.site.register(User, CustomUserAdmin)