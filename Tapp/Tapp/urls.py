"""Tapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user.views import login_view, refresh_token_view
from django.conf import settings
from django.conf.urls.static import static
from user_app.views import UserPersonalLink

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_app.urls')),
    path('login/', login_view, name='token_obtain_pair'),
    path('<str:pk>', UserPersonalLink.as_view(), name='Profile'),
    path('token/refresh/', refresh_token_view, name='token_refresh'),
    # path("<str:pk>", )
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('user', include("userMLM.urls")),
    path('openapi/', get_schema_view(        
        title="TappClub",
        description="APIs for Tapp",
        version="1.0.0"
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='doc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('docs2/', TemplateView.as_view(
        template_name='docv2.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path(
    "api-auth/", include("rest_framework.urls")
    ),  

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
