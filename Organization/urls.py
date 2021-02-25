from django.urls import path

from .views import *

urlpatterns = [
    path('userinfo/', UserInfoView.as_view(), name='GetUserInfo'),
    path('pdf/', some_view, name='GetUserInfo'),
]
