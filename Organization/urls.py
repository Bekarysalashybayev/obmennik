from django.urls import path

from .views import *

urlpatterns = [
    path('userinfo/', UserInfoView.as_view(), name='GetUserInfo'),
    path('pdf/', some_view, name='GetUserInfo'),
    path('base/', get_base_html, name='get_base_html'),
    path('organization/svedeniye/', get_org_sved_html, name='get_org_sved_html'),
]
