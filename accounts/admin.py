from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile
from rest_framework_simplejwt.tokens import RefreshToken


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active','is_admin')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined' , 'refresh_token', 'access_token')
    ordering = ('-date_joined',)

    def refresh_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)

    def access_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    refresh_token.short_description = ('Refresh ')
    access_token.short_description = ('Access ')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, AccountAdmin)
admin.site.register(Profile)