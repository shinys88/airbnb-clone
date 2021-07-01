from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# @admin.register(models.User)
# class UserAdmin(admin.ModelAdmin):
# """Custom User Admin"""
# list_display = ("username", "email", "gender", "language", "currency", "superhost")
# list_filter = (
#     "language",
#     "currency",
#     "superhost",
# )


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )
