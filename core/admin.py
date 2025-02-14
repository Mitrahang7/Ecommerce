from django.contrib import admin
from .models import Category,Product,Customer

admin.site.register(Category)
admin.site.register(Product)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone', 'address')
admin.site.register(Customer, CustomerAdmin)