from django.contrib import admin

from .models import *

admin.site.register(
    [Bank, Valuta, Client, ClientValutaAccount, Organization, OrganizationValutaAccount,
     Contract, OperationCategory, Operation, Sotrudnik, CursValuta, Session]
)