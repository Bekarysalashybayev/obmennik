from django.contrib import admin

from .models import *
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.register(
    [Bank, Valuta, Client, ClientValutaAccount, Organization, OrganizationValutaAccount,
     Contract, Operation, Sotrudnik, CursValuta, Session]
)
