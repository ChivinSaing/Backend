from django import template
from django.db.models import Sum

from polls.models import Customer, Drink, Order

register = template.Library()


@register.inclusion_tag("polls/cafe_dashboard_panel.html", takes_context=True)
def cafe_dashboard_panel(context):
    request = context.get("request")
    if request is None or not getattr(request.user, "is_staff", False):
        return {}

    revenue = Order.objects.filter(status=Order.Status.COMPLETED).aggregate(
        total=Sum("total_price")
    )["total"]
    if revenue is None:
        revenue = 0

    return {
        "order_total": Order.objects.count(),
        "pending_orders": Order.objects.filter(status=Order.Status.PENDING).count(),
        "completed_orders": Order.objects.filter(status=Order.Status.COMPLETED).count(),
        "customer_total": Customer.objects.count(),
        "drink_total": Drink.objects.count(),
        "low_stock": Drink.objects.filter(stock_qty__lte=10).order_by("stock_qty")[:6],
        "recent_orders": Order.objects.select_related("user")
        .order_by("-order_date")[:8],
        "revenue": revenue,
    }
