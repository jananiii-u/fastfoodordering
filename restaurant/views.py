import qrcode

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Table


def table_menu(request, token):
    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    from menu.models import Food

    foods = Food.objects.filter(
        is_available=True
    ).select_related('category')

    # Get cart from session
    cart = request.session.get('cart', {})

    # Get food IDs from cart
    food_ids = cart.keys()

    # Get actual food objects
    cart_foods = Food.objects.filter(
        id__in=food_ids
    )

    cart_items = []
    cart_count = 0
    subtotal = 0

    for food in cart_foods:
        quantity = cart.get(str(food.id), 0)

        item_total = food.price * quantity

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'item_total': item_total,
        })

        cart_count += quantity
        subtotal += item_total

    gst = subtotal * 5 / 100
    total = subtotal + gst

    return render(
        request,
        'customer/menu.html',
        {
            'table': table,
            'foods': foods,

            # Cart data
            'cart_items': cart_items,
            'cart_count': cart_count,
            'subtotal': subtotal,
            'gst': gst,
            'total': total,
        }
    )


def table_qr(request, token):
    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    table_url = request.build_absolute_uri(
        reverse('table_menu', args=[table.qr_token])
    )

    qr = qrcode.make(table_url)

    response = HttpResponse(content_type='image/png')
    qr.save(response, 'PNG')

    return response

    # =========================
# TABLE MANAGEMENT
# =========================

def table_management(request):

    tables = Table.objects.all().order_by('table_number')

    return render(
        request,
        'admin_panel/tables.html',
        {
            'tables': tables,
        }
    )