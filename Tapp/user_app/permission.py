from rest_framework import permissions
from .models import Membership
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()
class IsPaid(permissions.IsAuthenticated):

    def has_permission(self,request, view):
        if Membership.objects.get(user=request.user).validate_till >= datetime.date.today():
            return True
        return False
