from django.contrib import admin
from .models import User, Profile
from botapp.models import BotUser


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline, )
    list_display = ('first_name', 'last_name', 'phone_number', 'is_staff', 'is_active', 'is_superuser')
    list_select_related = ('profile', )
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined', )


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
    