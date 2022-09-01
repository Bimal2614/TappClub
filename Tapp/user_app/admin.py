from django.contrib.auth.models import Group
from django.contrib import admin

from .models import Profile, SocialMedia, referral, ForgotPass, saveContect, Membership , History, WNineForm
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['user', 'user_name', 'is_business']

class referralAdmin(admin.ModelAdmin):
    list_display= ['user_referrer', 'user_referee', 'level']

class SocialMidiaAdmin(admin.ModelAdmin):

    list_display = ['platform']

# class VarifyProfileAdmin(admin.ModelAdmin):

#     list_display = ['user']

class ForgotPasswordAdmin(admin.ModelAdmin):

    list_display = ['user', 'is_varified']

class saveContectAdmin(admin.ModelAdmin):

    list_display = ['user_id', 'profile_id']

class MembershipAdmin(admin.ModelAdmin):

    list_display = ['valid_till']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(SocialMedia)
admin.site.register(referral)
admin.site.register(ForgotPass)
admin.site.register(saveContect)
admin.site.register(Membership)
admin.site.unregister(Group)
admin.site.register(History)
admin.site.register(WNineForm)

 