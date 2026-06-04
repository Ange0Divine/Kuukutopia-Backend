from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, StockManager, Customer

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'gender', 'phone_number']
    list_filter = ['role', 'gender']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('gender', 'phone_number', 'address', 'role')}),
    )

@admin.register(StockManager)
class StockManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'current_location']
