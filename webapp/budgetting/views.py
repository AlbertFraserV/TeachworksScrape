from django.http import HttpResponse

from .models import DailyPaid

def index(request):
    latest_earnings = DailyPaid.objects.order_by('-paid_date')
    output = ', '.join([dp.paid_amount for dp in latest_earnings])
    return HttpResponse(output)