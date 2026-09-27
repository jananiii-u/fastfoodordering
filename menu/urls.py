from django.urls import path
from . import views


urlpatterns = [

    # Menu Management
    path(
        '',
        views.menu_management,
        name='menu_management'
    ),

    # Same menu page - used by Admin Panel
    path(
        '',
        views.menu_management,
        name='admin_menu'
    ),

    # Add Food
    path(
        'add-food/',
        views.add_food,
        name='add_food'
    ),

    # Edit Food
    path(
        'edit-food/<int:food_id>/',
        views.edit_food,
        name='edit_food'
    ),

    # Delete Food
    path(
        'delete-food/<int:food_id>/',
        views.delete_food,
        name='delete_food'
    ),

    # Toggle Food Availability
    path(
        'toggle-food/<int:food_id>/',
        views.toggle_food,
        name='toggle_food'
    ),
]