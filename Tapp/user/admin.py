from django.contrib import admin
from .models import NewUser

class NewUserAdmin(admin.ModelAdmin):

    list_display = ['email', 'id']

admin.site.site_header = "Tapp_Club"
# Register your models here.
admin.site.register(NewUser, NewUserAdmin)
