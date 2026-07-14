from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from polls.forms import DrinkForm
from polls.models import Drink
from polls.views.staff import staff_required


@staff_required
def inventory(request):
    drinks = Drink.objects.select_related("category").order_by("-id", "name")
    return render(
        request,
        "polls/pages/inventory.html",
        {
            "page_title": "Inventory",
            "main_title": "Drinks",
            "active_page": "inventory",
            "drinks": drinks,
        },
    )


@staff_required
def drink_create(request):
    if request.method == "POST":
        form = DrinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Drink saved.")
            return redirect("inventory")
    else:
        form = DrinkForm()
    cancel = reverse("inventory")
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Add drink",
            "main_title": "Add drink",
            "active_page": "drink_add",
            "form": form,
            "form_heading": "New drink",
            "cancel_href": cancel,
            "cancel_label": "← Back to inventory",
            "form_multipart": True,
        },
    )


@staff_required
def drink_edit(request, pk):
    drink = get_object_or_404(Drink, pk=pk)
    if request.method == "POST":
        form = DrinkForm(request.POST, request.FILES, instance=drink)
        if form.is_valid():
            form.save()
            messages.success(request, "Drink updated.")
            return redirect("inventory")
    else:
        form = DrinkForm(instance=drink)
    cancel = reverse("inventory")
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Edit drink",
            "main_title": "Edit drink",
            "active_page": "drink_edit",
            "form": form,
            "form_heading": drink.name,
            "cancel_href": cancel,
            "cancel_label": "← Back to inventory",
            "form_multipart": True,
        },
    )
