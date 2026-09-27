from django.urls import path
from . import views


urlpatterns = [

    path(
        '<uuid:token>/',
        views.customer_menu,
        name='customer_menu'
    ),

]