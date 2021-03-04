import io
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.http import FileResponse, HttpResponse
from django.template import loader
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.pdfgen import canvas
from rest_framework.generics import ListAPIView
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .serializers import *

message_login = "Вам надо зайти"
def is_autheticated_redirect(request):
    user = request.user
    print(user.is_authenticated)
    if not user.is_authenticated:
        print("ad")
        return redirect("login_page")


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
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    list = Organization.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('org_svedenye.html')
    return HttpResponse(html_template.render(context, request))


def organization_valuta_account(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    object_list = OrganizationValutaAccount.objects.all()
    context = {
        "object_list": object_list,
        "object_list_name": ["Код валюты", "Код Организации", "Номер валюты"],
        "name": "Валютные счета организации"
    }
    html_template = loader.get_template('organization_valuta_accounts.html')
    return HttpResponse(html_template.render(context, request))


def employess(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    object_list = Sotrudnik.objects.all()
    context = {
        "object_list": object_list,
        "object_list_name": ["Код содтрудник", "ФИО сотрудник"],
        "name": "Сотрудники"
    }
    html_template = loader.get_template('employess.html')
    return HttpResponse(html_template.render(context, request))


def currency(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    object_list = Valuta.objects.all()
    context = {
        "object_list": object_list,
        "object_list_name": ["Код Валюты", "Валюта"],
        "name": "Валюты"
    }
    html_template = loader.get_template('currency.html')
    return HttpResponse(html_template.render(context, request))


def clients_html(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    list = Client.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('clients.html')
    return HttpResponse(html_template.render(context, request))


def valut_clients_html(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    list = ClientValutaAccount.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('valut_clients.html')
    return HttpResponse(html_template.render(context, request))


def banks_html(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    list = Bank.objects.all()
    context = {
        'list': list
    }
    html_template = loader.get_template('banks.html')
    return HttpResponse(html_template.render(context, request))


def dogovor_html(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    list = Contract.objects.all()
    context = {
        'list': list,
    }
    html_template = loader.get_template('dogovor.html')
    return HttpResponse(html_template.render(context, request))


def session(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    object_list = Session.objects.all()
    context = {
        "object_list": object_list,
        "object_list_name": ["Дата сессии", "Код сотрудник"],
        "name": "Сессии"
    }
    html_template = loader.get_template('currency.html')
    return HttpResponse(html_template.render(context, request))


def operations_html(request):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
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
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
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
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    operations = Operation.objects.all()
    context = {
        'list': operations,
    }
    html_template = loader.get_template('employess_info.html')
    return HttpResponse(html_template.render(context, request))


def operation_pokupki(request, id: int):
    if not request.user.is_authenticated:
        messages.error(request, message_login)
        return redirect("login_page")
    vid1 = "покупок" if int(id) == 2 else "продаж"
    operations = Session.objects.filter(operation__category_id=id)
    context = {
        'list': operations,
        'vid1': vid1,
        'vid': "Покупки" if int(id) == 2 else "Продажи",
    }
    html_template = loader.get_template('operation_pokupki.html')
    return HttpResponse(html_template.render(context, request))


def login_page(request):
    if request.method == "GET":
        return render(request, 'login.html', {})


@csrf_exempt
def login(request):
    if request.method == "POST":
        phone = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("get_org_sved_html")
        messages.error(request, "Логин либо пароль неверный")
    return redirect("login_page")
