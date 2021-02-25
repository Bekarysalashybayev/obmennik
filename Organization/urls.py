from django.urls import path

from .views import *

urlpatterns = [
    path('userinfo/', UserInfoView.as_view(), name='GetUserInfo'),
    path('base/', get_base_html, name='get_base_html'),
    path('organization/svedeniye/', get_org_sved_html, name='get_org_sved_html'),
    path('organization-valuta-accounts/', OrganizationValutaAccountView.as_view(), name='organization_valuta_accounts'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('currency/', CurrencyView.as_view(), name='currency'),
    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('clients/', clients_html, name='clients_html'),
    path('clients/valuta/account', valut_clients_html, name='valut_clients_html'),
    path('banks/', banks_html, name='banks_html'),
    path('contracts/', dogovor_html, name='dogovor_html'),
    path('operations/', operations_html, name='operations_html'),
    path('curs_valuta/', curs_valuta_html, name='curs_valuta_html'),
    path('employees_info/', employees_info_html, name='employees_info'),
]
