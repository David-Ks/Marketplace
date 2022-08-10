from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Review
from shop.models import CheckOut


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'phone',
                ),
            },
        ),
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rate', 'for_view')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(CheckOut)