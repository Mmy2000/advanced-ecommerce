from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name','phone_number', 'last_name', 'username', 'last_login', 'date_joined', 'is_active','is_admin')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined' )
    ordering = ('-date_joined',)



    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user' , 'full_name' , 'full_address'  )
    list_filter = ( 'user' ,)

admin.site.register(User, AccountAdmin)
admin.site.register(Profile , ProfileAdmin)