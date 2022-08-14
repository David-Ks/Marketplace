from django.urls import path, include

from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='products'),
    path('busket/', BusketView.as_view(), name='busket'),
    path('saves/', SavesView.as_view(), name='saves'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('checkout/pay/', PayView.as_view(), name='pay'),
    path('checkout/pay/idram/', IdramPayView.as_view(), name='pay_idram'),
    path('info/', InfoView.as_view(), name='info'),

    path('error/', HomeView.as_view(), name='error'),  # WE NEED ERROR PAGE
]

