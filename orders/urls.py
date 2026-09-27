from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # ADD TO CART
    # =========================

    path(
        'add/<uuid:token>/<int:food_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    # =========================
    # INCREASE QUANTITY
    # =========================

    path(
        'increase/<uuid:token>/<int:food_id>/',
        views.increase_cart,
        name='increase_cart'
    ),

    # =========================
    # DECREASE QUANTITY
    # =========================

    path(
        'decrease/<uuid:token>/<int:food_id>/',
        views.decrease_cart,
        name='decrease_cart'
    ),

    # =========================
    # REMOVE FROM CART
    # =========================

    path(
        'remove/<uuid:token>/<int:food_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # =========================
    # CHECKOUT
    # =========================

    path(
        'checkout/<uuid:token>/',
        views.checkout,
        name='checkout'
    ),

    # =========================
    # PLACE ORDER
    # =========================

    path(
        'place-order/<uuid:token>/',
        views.place_order,
        name='place_order'
    ),

    # =========================
    # ADMIN ORDERS
    # =========================

    path(
        'admin-orders/',
        views.admin_orders,
        name='admin_orders'
    ),
    path(
    'admin-orders/<int:order_id>/<str:status>/',
    views.update_order_status,
    name='update_order_status'
),

# =========================
# CUSTOMER ORDER TRACKING
# =========================

path(
    'track-order/<int:order_id>/',
    views.order_tracking,
    name='order_tracking'
),

path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),

path(
    'analytics/',
    views.analytics,
    name='analytics'
),

path(
    'order-history/',
    views.order_history,
    name='order_history'
),
]