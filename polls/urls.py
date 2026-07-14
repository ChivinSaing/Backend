from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from polls import views
from polls.forms import StaffLoginForm

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="polls/pages/login.html",
            authentication_form=StaffLoginForm,
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="home"),
    path(
        "cafe_dashboard_panel/",
        views.dashboard,
        name="cafe_dashboard_panel",
    ),
    path("categories/add/", views.category_create, name="category_add"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/", views.categories_list, name="categories"),
    path("customers/add/", views.customer_create, name="customer_add"),
    path("customers/<int:pk>/edit/", views.customer_edit, name="customer_edit"),
    path("customers/", views.customers_list, name="customers"),
    path("staff/attendance/clock-in/", views.staff_clock_in, name="staff_clock_in"),
    path("staff/attendance/clock-out/", views.staff_clock_out, name="staff_clock_out"),
    path("staff/attendance/", views.staff_attendance, name="staff_attendance"),
    path("staff/add/", views.staff_create, name="staff_add"),
    path("staff/<int:pk>/edit/", views.staff_edit, name="staff_edit"),
    path("staff/", views.staff_list, name="staff_list"),
    path("inventory/add/", views.drink_create, name="drink_add"),
    path("inventory/<int:pk>/edit/", views.drink_edit, name="drink_edit"),
    path("inventory/", views.inventory, name="inventory"),
    path("order-items/add/", views.order_item_create, name="order_item_add"),
    path(
        "order-items/<int:pk>/edit/",
        views.order_item_edit,
        name="order_item_edit",
    ),
    path("order-items/", views.order_items_list, name="order_items"),
    path("orders/add/", views.order_create, name="order_add"),
    path("orders/<int:pk>/edit/", views.order_edit, name="order_edit"),
    path("orders/", views.orders_list, name="orders"),
    # Public menu API (for frontend)
    path("api/menu/", views.menu_api, name="api_menu"),
    path(
        "api/drinks/<int:drink_id>/view/",
        views.drink_record_view,
        name="api_drink_view",
    ),
    # Simple create drink API (for Postman)
    path("api/drinks/", views.drinks_api, name="api_drinks"),
]
