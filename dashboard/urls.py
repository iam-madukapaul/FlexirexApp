from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account, name='account'),
    path('investment/', views.investment, name='investment'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('history/', views.history, name='history'),
    path('withdrawal_history/', views.withdrawal_history, name='withdrawal_history'),
    path('referral/<str:referral_code>/', views.referral, name='referral'),
]