from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect


def home(request):
    return redirect('/menu/')


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Admin / restaurant management
    path('restaurant/', include('restaurant.urls')),

    # Orders
    path('orders/', include('orders.urls')),

    # Menu management
    path('menu/', include('menu.urls')),

    # Customer QR menu
    path('customer/', include('customer.urls')),
]