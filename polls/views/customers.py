from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from polls.forms import CustomerForm
from polls.models import Customer
from polls.views.staff import staff_required


@staff_required
def customers_list(request):
    customers = Customer.objects.order_by("-created_at")
    return render(
        request,
        "polls/pages/customers.html",
        {
            "page_title": "Customers",
            "main_title": "Customers",
            "active_page": "customers",
            "customers": customers,
        },
    )


@staff_required
def customer_create(request):
    cancel = reverse("customers")
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer saved.")
            return redirect("customers")
    else:
        form = CustomerForm()
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Add customer",
            "main_title": "Add customer",
            "active_page": "customer_add",
            "form": form,
            "form_heading": "New customer",
            "cancel_href": cancel,
            "cancel_label": "← Back to customers",
        },
    )


@staff_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    cancel = reverse("customers")
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated.")
            return redirect("customers")
    else:
        form = CustomerForm(instance=customer)
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Edit customer",
            "main_title": "Edit customer",
            "active_page": "customer_edit",
            "form": form,
            "form_heading": customer.name,
            "cancel_href": cancel,
            "cancel_label": "← Back to customers",
        },
    )
