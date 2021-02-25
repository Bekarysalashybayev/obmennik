import io

from django.http import FileResponse, HttpResponse
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.pdfgen import canvas
from rest_framework.generics import ListAPIView

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
