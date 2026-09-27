from django.urls import path
from . import views

urlpatterns = [
    path(
        'table/<uuid:token>/',
        views.table_menu,
        name='table_menu'
    ),

    path(
        'table/<uuid:token>/qr/',
        views.table_qr,
        name='table_qr'
    ),

    path(
    'tables/',
    views.table_management,
    name='table_management'
),
]