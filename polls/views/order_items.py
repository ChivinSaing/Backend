from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from polls.forms import OrderItemForm
from polls.models import OrderItem
from polls.views.staff import staff_required


@staff_required
def order_items_list(request):
    items = OrderItem.objects.select_related("order", "drink").order_by(
        "-order__order_date", "order_id", "pk"
    )
    return render(
        request,
        "polls/pages/order_items.html",
        {
            "page_title": "Order items",
            "main_title": "Order items",
            "active_page": "order_items",
            "items": items,
        },
    )


@staff_required
def order_item_create(request):
    cancel = reverse("order_items")
    initial = {}
    oid = request.GET.get("order")
    if oid and str(oid).isdigit():
        initial["order"] = int(oid)

    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Line item saved.")
            return redirect("order_items")
    else:
        form = OrderItemForm(
            initial={
                **initial,
                "qty": 1,
                "price": Decimal("0.00"),
            }
        )
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Add order line",
            "main_title": "Add order line",
            "active_page": "order_item_add",
            "form": form,
            "form_heading": "New order line",
            "cancel_href": cancel,
            "cancel_label": "← Back to order items",
        },
    )


@staff_required
def order_item_edit(request, pk):
    item = get_object_or_404(OrderItem.objects.select_related("order", "drink"), pk=pk)
    cancel = reverse("order_items")
    if request.method == "POST":
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Line item updated.")
            return redirect("order_items")
    else:
        form = OrderItemForm(instance=item)
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Edit order line",
            "main_title": "Edit order line",
            "active_page": "order_item_edit",
            "form": form,
            "form_heading": f"Line #{item.pk} — order #{item.order_id}",
            "cancel_href": cancel,
            "cancel_label": "← Back to order items",
        },
    )
