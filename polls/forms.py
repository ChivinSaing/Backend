from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ClearableFileInput
from django.utils import timezone

from polls.models import Category, Customer, Drink, Order, OrderItem, Staff

User = get_user_model()


class StaffLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "cafe-input")


class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = [
            "category",
            "name",
            "size",
            "price",
            "price_s",
            "price_m",
            "price_l",
            "sugar",
            "stock_qty",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["price"].help_text = "Default price (used if size prices are empty)."
        self.fields["price_s"].label = "Price (S)"
        self.fields["price_m"].label = "Price (M)"
        self.fields["price_l"].label = "Price (L)"
        self.fields["price_s"].required = False
        self.fields["price_m"].required = False
        self.fields["price_l"].required = False

        # On edit: only show per-size price inputs for sizes this drink supports.
        # (Keeps the form simple when a drink has only M,L etc.)
        raw_sizes = ""
        try:
            raw_sizes = (getattr(self.instance, "size", "") or "").strip()
        except Exception:
            raw_sizes = ""
        if raw_sizes:
            tokens = [t.strip().upper() for t in raw_sizes.replace("/", ",").split(",") if t.strip()]
            allowed = set(tokens)
            if "S" not in allowed:
                self.fields.pop("price_s", None)
            if "M" not in allowed:
                self.fields.pop("price_m", None)
            if "L" not in allowed:
                self.fields.pop("price_l", None)

        self.fields["image"].widget = ClearableFileInput(
            attrs={
                "accept": "image/*",
                "class": "cafe-file-input",
            }
        )
        for name in self.fields:
            if name == "image":
                continue
            self.fields[name].widget.attrs.setdefault("class", "cafe-input")
        self.fields["sugar"].widget.attrs.setdefault(
            "placeholder",
            "e.g. 10%, 20%, 30%, 50%, 70%, 100%",
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.setdefault("class", "cafe-input")


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.setdefault("class", "cafe-input")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["user", "order_date", "total_price", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.setdefault("class", "cafe-input")
        self.fields["order_date"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "cafe-input"},
            format="%Y-%m-%dT%H:%M",
        )
        self.fields["order_date"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]
        if self.instance.pk and self.instance.order_date:
            od = self.instance.order_date
            if timezone.is_aware(od):
                od = timezone.localtime(od)
            self.fields["order_date"].initial = od.strftime("%Y-%m-%dT%H:%M")


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "drink", "qty", "price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.setdefault("class", "cafe-input")


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["user", "name", "phone", "gender", "is_active"]
        labels = {
            "user": "Login user (optional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.order_by("username")
        self.fields["user"].required = False
        self.fields["user"].help_text = (
            "Link this employee to a portal login (same username). "
            "Leave empty if they do not sign in."
        )
        for name in self.fields:
            self.fields[name].widget.attrs.setdefault("class", "cafe-input")
