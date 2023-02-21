from django.urls import path

from . import views

app_name = 'budget'
urlpatterns = [
    path('', views.index, name='index'),
    path('payments', views.viewPayments, name='payments'),
    path('spending', views.viewSpendings, name='spendings'),
    path('addSpending', views.addSpendings, name='addSpending')
]