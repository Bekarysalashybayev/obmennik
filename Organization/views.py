import io

from django.http import FileResponse, HttpResponse
from django.template import loader
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.pdfgen import canvas
from rest_framework.generics import ListAPIView
from django.shortcuts import render
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
