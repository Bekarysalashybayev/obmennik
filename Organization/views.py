import io

from django.http import FileResponse, HttpResponse
from django.template import loader
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.pdfgen import canvas
from rest_framework.generics import ListAPIView
from django.shortcuts import render
from django.views.generic import ListView
from .models import Valuta

from .serializers import *


class UserInfoView(ListAPIView):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()


def some_view(request):
    serializer = OperationSerializer(Operation.objects.all(), many=True)
    queryset = serializer.data

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
    p = canvas.Canvas(response)
    MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(MyFontObject)
    i = 10
    for query in queryset:
        p.drawString(100, 350 + i, query['contract']['date'])
        p.drawString(180, 350 + i, query['contract']['client']['fio'])
        p.drawString(300, 350 + i, query['category'])
        i = i + 10
        print(query['category'])

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return response


def get_base_html(request):
    return render(request, 'base.html', {})


def get_currency(request):
    if request.method == "GET":
        valuta = Valuta.objects.all()
        return render(request, 'base.html', {"valuta": valuta})


def get_org_sved_html(request):
    list = Organization.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('org_svedenye.html')
    return HttpResponse(html_template.render(context, request))


def get_org_sved_html(request):
    list = Organization.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('org_svedenye.html')
    return HttpResponse(html_template.render(context, request))


class OrganizationValutaAccountView(ListView):
    model = OrganizationValutaAccount
    template_name = 'organization_valuta_accounts.html'

    def get_context_data(self, **kwargs):
        context = super(OrganizationValutaAccountView, self).get_context_data(**kwargs)
        context['object_list_name'] = ["Код валюты", "Код Организации", "Номер валюты"]
        context['name'] = "Валютные счета организации"
        return context


class EmployeesView(ListView):
    model = Sotrudnik
    template_name = 'employess.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeesView, self).get_context_data(**kwargs)
        context['object_list_name'] = ["Код содтрудник", "ФИО сотрудник"]
        context['name'] = "Сотрудники"
        return context


class CurrencyView(ListView):
    model = Valuta
    template_name = 'currency.html'

    def get_context_data(self, **kwargs):
        context = super(CurrencyView, self).get_context_data(**kwargs)
        context['object_list_name'] = ["Код Валюты", "Валюта"]
        context['name'] = "Валюты"
        return context


def clients_html(request):
    list = Client.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('clients.html')
    return HttpResponse(html_template.render(context, request))


def valut_clients_html(request):
    list = ClientValutaAccount.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('valut_clients.html')
    return HttpResponse(html_template.render(context, request))


def banks_html(request):
    list = Bank.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('banks.html')
    return HttpResponse(html_template.render(context, request))


def dogovor_html(request):
    list = Contract.objects.all()
    context = {
        'list': list,
    }
    html_template = loader.get_template('dogovor.html')
    return HttpResponse(html_template.render(context, request))


class SessionsView(ListView):
    model = Session
    template_name = 'sessions.html'

    def get_context_data(self, **kwargs):
        context = super(SessionsView, self).get_context_data(**kwargs)
        context['object_list_name'] = ["Дата сессии", "Код сотрудник"]
        context['name'] = "Сессии"

        return context


def operations_html(request):
    contract_id = request.GET.get("contract_id")
    if contract_id:
        list = Operation.objects.filter(contract=contract_id)
    else:
        list = Operation.objects.all()
    context = {
        'list': list,
    }
    html_template = loader.get_template('operations.html')
    return HttpResponse(html_template.render(context, request))


def curs_valuta_html(request):
    valute_id = request.GET.get('valute_id')
    if valute_id:
        list = CursValuta.objects.filter(code_valuta_id=valute_id)
    else:
        list = CursValuta.objects.all()
    context = {
        'list': list,
    }
    html_template = loader.get_template('valut_curs.html')
    return HttpResponse(html_template.render(context, request))


def employees_info_html(request):

    operations = Operation.objects.all()
    context = {
        'list': operations,
    }
    html_template = loader.get_template('employess_info.html')
    return HttpResponse(html_template.render(context, request))
