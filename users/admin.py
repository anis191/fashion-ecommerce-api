from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_deleted",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_deleted",
        "groups",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )
    ordering = ("email",)
    readonly_fields = (
        "last_login",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password",
            )
        }),
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
            )
        }),
        ("Status", {
            "fields": (
                "is_active",
                "is_staff",
                "is_deleted",
                "deleted_at",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "phone_number",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "is_superuser",
            ),
        }),
    )

admin.site.register(Address)