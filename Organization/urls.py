from django.conf.urls import url
from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import logout
from .views import *

# def logout_view(request):
#     logout(request)
#     return redirect()


urlpatterns = [
    path('login-page/', login_page, name="login_page"),
    path('login/', login, name="login"),
    path('logout/', login, name="logout"),
    path('userinfo/', UserInfoView.as_view(), name='GetUserInfo'),
    path('base/', get_base_html, name='get_base_html'),
    path('organization/svedeniye/', get_org_sved_html, name='get_org_sved_html'),
    path('organization-valuta-accounts/', organization_valuta_account, name='organization_valuta_accounts'),
    path('employees/', employess, name='employees'),
    path('currency/', currency, name='currency'),
    path('sessions/', session, name='sessions'),
    path('clients/', clients_html, name='clients_html'),
    path('clients/valuta/account', valut_clients_html, name='valut_clients_html'),
    path('banks/', banks_html, name='banks_html'),
    path('contracts/', dogovor_html, name='dogovor_html'),
    path('operations/', operations_html, name='operations_html'),
    path('curs_valuta/', curs_valuta_html, name='curs_valuta_html'),
    path('employees_info/', employees_info_html, name='employees_info'),
    path('operation_pokupki/<id>', operation_pokupki, name='operation_pokupki'),
]
