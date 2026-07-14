from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from polls.forms import OrderForm
from polls.models import Order
from polls.views.staff import staff_required


@staff_required
def orders_list(request):
    orders = Order.objects.select_related("user").order_by("-order_date")
    status = request.GET.get("status")
    if status in (Order.Status.PENDING, Order.Status.COMPLETED, Order.Status.CANCELLED):
        orders = orders.filter(status=status)
    return render(
        request,
        "polls/pages/orders.html",
        {
            "page_title": "Orders",
            "main_title": "Orders",
            "active_page": "orders",
            "orders": orders,
            "status_filter": status or "",
        },
    )


@staff_required
def order_create(request):
    cancel = reverse("orders")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Order saved.")
            return redirect("orders")
    else:
        form = OrderForm(
            initial={
                "order_date": timezone.localtime(timezone.now()).strftime(
                    "%Y-%m-%dT%H:%M"
                ),
                "total_price": Decimal("0.00"),
                "status": Order.Status.PENDING,
            }
        )
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Add order",
            "main_title": "Add order",
            "active_page": "order_add",
            "form": form,
            "form_heading": "New order",
            "cancel_href": cancel,
            "cancel_label": "← Back to orders",
        },
    )

@staff_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    cancel = reverse("orders")
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated.")
            return redirect("orders")
    else:
        form = OrderForm(instance=order)
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Edit order",
            "main_title": "Edit order",
            "active_page": "order_edit",
            "form": form,
            "form_heading": f"Order #{order.pk}",
            "cancel_href": cancel,
            "cancel_label": "← Back to orders",
        },
    )
