from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Category


def menu_management(request):
    foods = Food.objects.all().order_by('-created_at')

    return render(
        request,
        "admin_panel/menu.html",
        {
            "foods": foods
        }
    )


def add_food(request):

    categories = Category.objects.all()

    if request.method == "POST":

        category_id = request.POST.get("category")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        category = Category.objects.get(id=category_id)

        Food.objects.create(
            category=category,
            name=name,
            description=description,
            price=price,
            image=image,
            is_available=True
        )

        return redirect("menu_management")

    return render(
        request,
        "admin_panel/add_food.html",
        {
            "categories": categories
        }
    )


def edit_food(request, food_id):

    food = get_object_or_404(Food, id=food_id)
    categories = Category.objects.all()

    if request.method == "POST":

        food.category_id = request.POST.get("category")
        food.name = request.POST.get("name")
        food.description = request.POST.get("description")
        food.price = request.POST.get("price")

        if request.FILES.get("image"):
            food.image = request.FILES.get("image")

        food.save()

        return redirect("menu_management")

    return render(
        request,
        "admin_panel/edit_food.html",
        {
            "food": food,
            "categories": categories
        }
    )


def delete_food(request, food_id):

    food = get_object_or_404(Food, id=food_id)

    if request.method == "POST":
        food.delete()

    return redirect("menu_management")


def toggle_food(request, food_id):

    food = get_object_or_404(Food, id=food_id)

    food.is_available = not food.is_available
    food.save()

    return redirect("menu_management")