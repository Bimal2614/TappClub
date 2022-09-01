import datetime
# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import UserSerializer
from .utils import generate_access_token, generate_refresh_token
from user_app.models import Membership
 
@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    User = get_user_model()
    email = str(request.data.get('email')).lower()
    password = request.data.get('password')

    response = Response()
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')
    # print(email)
    user = User.objects.filter(email=email).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    # print(user)
    # if not user.is_verified:
    #     raise exceptions.AuthenticationFailed('user not Varified')
    if not user.is_superuser:
        if not Membership.objects.get(user=user).validate_till >= datetime.date.today():
            raise exceptions.AuthenticationFailed('user not Paid')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')
    
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'refreshtoken': refresh_token,
        'user': serialized_user,
    }
 
    return response


import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from .utils import generate_access_token


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = get_user_model()
    refresh_token = request.data.get('refresh')    
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})
