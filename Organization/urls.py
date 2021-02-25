from django.urls import path

from .views import *

urlpatterns = [
    path('userinfo/', UserInfoView.as_view(), name='GetUserInfo'),
    path('pdf/', some_view, name='GetUserInfo'),
    path('base/', get_base_html, name='get_base_html'),
    path('organization/svedeniye/', get_org_sved_html, name='get_org_sved_html'),
    path('clients/', clients_html, name='clients_html'),
    path('clients/valuta/account', valut_clients_html, name='valut_clients_html'),
    path('banks/', banks_html, name='banks_html'),
    path('contracts/', dogovor_html, name='dogovor_html'),
]
