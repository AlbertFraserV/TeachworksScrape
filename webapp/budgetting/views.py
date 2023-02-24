from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import Round

from datetime import date

from .models import DailyPaid, DailySpent, DailyNet

def index(request):
    latest_earnings = DailyPaid.objects.order_by('-paid_date')
    
    template = loader.get_template('index.html')
    context = {
        'latest_earnings': latest_earnings,
    }
    return render(request, 'index.html', context)

def viewPayments(request):
    latest_earnings = DailyPaid.objects.order_by('-paid_date')
    #l
    context = {
        'latest_earnings': latest_earnings,
    }
    return render(request, 'payments.html', context)

def viewSpendings(request):
    latest_spendings = DailySpent.objects.order_by('-spent_date')
    context = {
        'latest_spendings': latest_spendings,
    }
    return render(request, 'spending.html', context)

def addSpendings(request):
    new_amount = DailySpent(spent_date=request.POST['spent_date'], spent_amount=request.POST['spent_amount'], spent_name=request.POST['spent_name'])
    new_amount.save()
    updateNetSpendingDay(date=request.POST['spent_date'])
    return HttpResponseRedirect(reverse('budget:spendings'))


def updateNetSpendingDay():
    # Get unique dates from both Payment and Spending models
    dates_paid = list(DailyPaid.objects.values_list('paid_date', flat=True).distinct())
    dates_spent = list(DailySpent.objects.values_list('spent_date', flat=True).distinct())
    dates = set(dates_paid+dates_spent)
    for date in dates:
        total_payments = DailyPaid.objects.filter(paid_date=date).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        total_spendings = DailySpent.objects.filter(spent_date=date).aggregate(Sum('spent_amount'))['spent_amount__sum'] or 0
        net_pay = total_payments - total_spendings
        DailyNet.objects.update_or_create(daily_date=date, defaults={'daily_net_earnings': f'{net_pay}'})

def recalcAllNetSpendings(request):
    all_dates = DailyPaid.objects.values('paid_date').distinct()
    for dates in all_dates:
        updateNetSpendingDay(dates['spent_date'])

def calculateTotalNetEarnings():
    total = DailyNet.objects.aggregate(total=Round(Sum('daily_net_earnings'),2))
