from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from decimal import Decimal

from menu.models import Food
from restaurant.models import Table
from .models import Order, OrderItem


# =========================
# ADD TO CART
# =========================

def add_to_cart(request, token, food_id):

    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    food = get_object_or_404(
        Food,
        id=food_id,
        is_available=True
    )

    cart = request.session.get(
        'cart',
        {}
    )

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{food.name} added to cart!"
    )

    return redirect(
        'customer_menu',
        token=table.qr_token
    )


# =========================
# INCREASE QUANTITY
# =========================

def increase_cart(request, token, food_id):

    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    cart = request.session.get(
        'cart',
        {}
    )

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect(
        'customer_menu',
        token=table.qr_token
    )


# =========================
# DECREASE QUANTITY
# =========================

def decrease_cart(request, token, food_id):

    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    cart = request.session.get(
        'cart',
        {}
    )

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] -= 1

        if cart[food_id] <= 0:
            del cart[food_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect(
        'customer_menu',
        token=table.qr_token
    )


# =========================
# REMOVE FROM CART
# =========================

def remove_from_cart(request, token, food_id):

    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    cart = request.session.get(
        'cart',
        {}
    )

    food_id = str(food_id)

    if food_id in cart:
        del cart[food_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect(
        'customer_menu',
        token=table.qr_token
    )


# =========================
# CHECKOUT
# =========================

def checkout(request, token):

    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    cart = request.session.get(
        'cart',
        {}
    )

    cart_items = []

    subtotal = Decimal('0.00')

    for food_id, quantity in cart.items():

        food = get_object_or_404(
            Food,
            id=int(food_id),
            is_available=True
        )

        item_total = food.price * quantity

        subtotal += item_total

        cart_items.append({
            'food': food,
            'quantity': quantity,
            'item_total': item_total,
        })

    gst = subtotal * Decimal('0.05')

    total = subtotal + gst

    return render(
        request,
        'customer/checkout.html',
        {
            'table': table,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'gst': gst,
            'total': total,
        }
    )


# =========================
# PLACE ORDER
# =========================

def place_order(request, token):

    if request.method != 'POST':
        return redirect(
            'checkout',
            token=token
        )

    table = get_object_or_404(
        Table,
        qr_token=token,
        is_active=True
    )

    cart = request.session.get('cart', {})

    if not cart:
        messages.error(
            request,
            'Your cart is empty!'
        )

        return redirect(
            'table_menu',
            token=table.qr_token
        )

    subtotal = Decimal('0.00')

    # Create Order
    order = Order.objects.create(
        table=table,
        status='Pending',
        total_amount=Decimal('0.00')
    )

    # Create Order Items
    for food_id, quantity in cart.items():

        food = get_object_or_404(
            Food,
            id=int(food_id),
            is_available=True
        )

        item_total = food.price * quantity
        subtotal += item_total

        OrderItem.objects.create(
            order=order,
            food=food,
            quantity=quantity,
            price=food.price
        )

    # GST 5%
    gst = subtotal * Decimal('0.05')

    total = subtotal + gst

    # Save final total
    order.total_amount = total
    order.save()

    # Clear cart
    request.session['cart'] = {}
    request.session.modified = True

    # Go directly to Order Tracking
    return redirect(
        'order_tracking',
        order_id=order.id
    )

# =========================
# ADMIN ORDERS
# =========================

def admin_orders(request):

    status = request.GET.get('status')

    table_number = request.GET.get('table')

    orders = Order.objects.all().order_by(
        '-created_at'
    )

    if status:
        orders = orders.filter(
            status=status
        )

    if table_number:
        orders = orders.filter(
            table__table_number=table_number
        )

    tables = Table.objects.filter(
        is_active=True
    ).order_by(
        'table_number'
    )

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    preparing_orders = Order.objects.filter(
        status='Preparing'
    ).count()

    ready_orders = Order.objects.filter(
        status='Ready'
    ).count()

    completed_orders = Order.objects.filter(
        status='Completed'
    ).count()

    return render(
        request,
        'admin_panel/orders.html',
        {
            'orders': orders,
            'tables': tables,

            'selected_status': status,
            'selected_table': table_number,

            'pending_orders': pending_orders,
            'preparing_orders': preparing_orders,
            'ready_orders': ready_orders,
            'completed_orders': completed_orders,
        }
    )


# =========================
# UPDATE ORDER STATUS
# =========================

def update_order_status(
    request,
    order_id,
    status
):

    if request.method == 'POST':

        order = get_object_or_404(
            Order,
            id=order_id
        )

        if status in dict(
            Order.STATUS_CHOICES
        ):

            order.status = status

            order.save()

    return redirect(
        'admin_orders'
    )


# =========================
# CUSTOMER ORDER TRACKING
# =========================

def order_tracking(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        'customer/order_tracking.html',
        {
            'order': order,
        }
    )


# =========================
# ADMIN DASHBOARD
# =========================

def dashboard(request):

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    preparing_orders = Order.objects.filter(
        status='Preparing'
    ).count()

    ready_orders = Order.objects.filter(
        status='Ready'
    ).count()

    completed_orders = Order.objects.filter(
        status='Completed'
    ).count()

    total_sales = sum(
        order.total_amount
        for order in Order.objects.all()
        if order.total_amount
    )

    recent_orders = Order.objects.order_by(
        '-id'
    )[:5]

    return render(
        request,
        'admin_panel/dashboard.html',
        {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'preparing_orders': preparing_orders,
            'ready_orders': ready_orders,
            'completed_orders': completed_orders,
            'total_sales': total_sales,
            'recent_orders': recent_orders,
        }
    )


# =========================
# ANALYTICS
# =========================

def analytics(request):

    total_orders = Order.objects.count()

    total_sales = sum(
        order.total_amount
        for order in Order.objects.all()
        if order.total_amount
    )

    pending_orders = Order.objects.filter(
        status='Pending'
    ).count()

    preparing_orders = Order.objects.filter(
        status='Preparing'
    ).count()

    ready_orders = Order.objects.filter(
        status='Ready'
    ).count()

    completed_orders = Order.objects.filter(
        status='Completed'
    ).count()

    food_sales = {}

    for order in Order.objects.all():

        for item in order.items.all():

            food_name = item.food.name

            if food_name not in food_sales:
                food_sales[food_name] = 0

            food_sales[food_name] += item.quantity

    food_sales = dict(
        sorted(
            food_sales.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )

    return render(
        request,
        'admin_panel/analytics.html',
        {
            'total_orders': total_orders,
            'total_sales': total_sales,
            'pending_orders': pending_orders,
            'preparing_orders': preparing_orders,
            'ready_orders': ready_orders,
            'completed_orders': completed_orders,
            'food_sales': food_sales,
        }
    )


# =========================
# ORDER HISTORY
# =========================

def order_history(request):

    status = request.GET.get(
        'status'
    )

    if status:

        orders = Order.objects.filter(
            status=status
        ).order_by('-id')

    else:

        orders = Order.objects.all().order_by(
            '-id'
        )

    return render(
        request,
        'admin_panel/order_history.html',
        {
            'orders': orders,
            'selected_status': status,
        }
    )