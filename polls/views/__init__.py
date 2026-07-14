"""Cafe portal views (one module per page)."""

from polls.views.categories import (
    categories_list,
    category_create,
    category_edit,
)
from polls.views.customers import (
    customer_create,
    customer_edit,
    customers_list,
)
from polls.views.dashboard import dashboard
from polls.views.inventory import drink_create, drink_edit, inventory
from polls.views.order_items import (
    order_item_create,
    order_item_edit,
    order_items_list,
)
from polls.views.orders import order_create, order_edit, orders_list
from polls.views.workforce import (
    staff_attendance,
    staff_clock_in,
    staff_clock_out,
    staff_create,
    staff_edit,
    staff_list,
)
from polls.views.api_menu import menu_api
from polls.views.api_drink_view import drink_record_view
from polls.views.api_drinks import drinks_api

__all__ = [
    "categories_list",
    "category_create",
    "category_edit",
    "customer_create",
    "customer_edit",
    "customers_list",
    "dashboard",
    "drink_create",
    "drink_edit",
    "inventory",
    "order_create",
    "order_edit",
    "order_item_create",
    "order_item_edit",
    "order_items_list",
    "orders_list",
    "staff_attendance",
    "staff_clock_in",
    "staff_clock_out",
    "staff_create",
    "staff_edit",
    "staff_list",
    "menu_api",
    "drink_record_view",
    "drinks_api",
]
