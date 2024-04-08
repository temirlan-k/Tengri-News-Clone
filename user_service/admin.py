from django.contrib import admin
from .models import Subscription, EmailConfirmation


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "get_categories", "timestamp", "is_active")
    list_filter = ("timestamp", "is_active")
    search_fields = ("user__email", "categories__name")

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Categories"


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("user", "token")
    search_fields = ("user__email", "token")


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
