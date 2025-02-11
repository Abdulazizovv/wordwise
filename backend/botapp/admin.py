from django.contrib import admin

from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'username')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at', )


admin.site.register(BotUser, BotUserAdmin)
