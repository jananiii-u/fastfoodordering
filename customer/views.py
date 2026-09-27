from django.shortcuts import render, get_object_or_404
from decimal import Decimal

from menu.models import Food, Category
from restaurant.models import Table


def customer_menu(request, token):

    # Get the restaurant table using QR token
    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    # Get all available foods
    foods = Food.objects.filter(
        is_available=True
    ).order_by(
        'category',
        'name'
    )

    # Get categories which contain available foods
    category_ids = foods.values_list(
        'category_id',
        flat=True
    ).distinct()

    categories = Category.objects.filter(
        id__in=category_ids
    ).order_by('name')

    # =========================
    # CART
    # =========================

    cart = request.session.get(
        'cart',
        {}
    )

    cart_items = []

    subtotal = Decimal('0.00')

    cart_count = 0

    for food_id, quantity in cart.items():

        food = get_object_or_404(
            Food,
            id=int(food_id),
            is_available=True
        )

        item_total = food.price * quantity

        subtotal += item_total

        cart_count += quantity

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'item_total': item_total,
        })

    # =========================
    # GST
    # =========================

    gst = subtotal * Decimal('0.05')

    total = subtotal + gst

    # =========================
    # SEND DATA TO TEMPLATE
    # =========================

    return render(
        request,
        "customer/menu.html",
        {
            "foods": foods,
            "categories": categories,
            "table": table,

            "cart_items": cart_items,
            "cart_count": cart_count,

            "subtotal": subtotal,
            "gst": gst,
            "total": total,
        }
    )