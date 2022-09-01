from django.urls import path

from .views import (AddProfile, registration_view, 
                    GetProfile, forgot_password, 
                    varify_forgot_password, SocialMediaView, UserPersonalLink, 
                    SaveContectView, Office, SocialMediaV,
                    MembershipView, HistoryView, formVie
                    )

urlpatterns = [
    path('registration/', registration_view, name='registration'),
    # path('profile/', AllProfile.as_view(), name='all-profile'),
    # path('personal/profile/<int:pk>', ProfileView.as_view(), name='profile-detail'),
    path('addProfile/', AddProfile.as_view(), name="add profile"),
    path('profile/', GetProfile.as_view(), name = 'get-profile'),
    # path('varify/<slug>', varify, name="varify profile"),
    path('forgotpassword/', forgot_password.as_view(), name="forgot password"),
    path('verify_forgot_password/<slug>', varify_forgot_password, name="varify_forgot_password"),
    path('addSocialMedia/', SocialMediaView.as_view()),
    path('socialmedia/<int:pk>', SocialMediaV.as_view()),
    path('savecontect/', SaveContectView.as_view(), name ='saveContect'),
    path('membership/', MembershipView.as_view(), name='membership'),
    path('history/', HistoryView.as_view()),
    path('office/', Office.as_view()),
    path('wnine/', formVie.as_view(), name = "W9 form")
    # # path('/user/<str:username>', User)
    ] 
  
    # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NjA3MzU3NzQsImlhdCI6MTY2MDEzMDk3NH0.fSJ2hNUBm8SFTLu2rN8UccvmioQ871kVf8g2Kb_f3ok
