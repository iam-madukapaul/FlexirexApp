from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('affiliate/', views.affiliate, name='affiliate'),
    path('faq/', views.faq, name='faq'),
    path('policy/', views.policy, name='policy'),
    path('detail_post/<str:slug>/', views.detail_post, name='detail_post'),
    path('plan/', views.plan, name='plan'),
]