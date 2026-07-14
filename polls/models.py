from django.conf import settings
from django.db import models


class Customer(models.Model):
    """Customer record; stored in DB table `users` (per schema)."""

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Drink(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column="cat_id",
        related_name="drinks",
    )
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Optional per-size pricing. If empty, frontend falls back to `price`.
    price_s = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_m = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_l = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sugar = models.CharField(
        max_length=128,
        verbose_name="Sugar (% options)",
        help_text=(
            "Sweetness levels offered for this drink, as percentages. "
            "Enter comma-separated values, e.g. 10%, 20%, 30%, 50%, 70%, 100%."
        ),
    )
    stock_qty = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times customers opened this drink’s detail page; homepage carousel shows most-viewed drinks.",
    )
    image = models.ImageField(
        upload_to="drinks/",
        blank=True,
        help_text="Upload a product photo (JPG, PNG, WebP, etc.).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "drinks"

    @property
    def sugar_display(self):
        """Format sugar options for tables (adds % if missing, comma + space between)."""
        raw = (self.sugar or "").strip()
        if not raw:
            return "—"
        parts = []
        for chunk in raw.split(","):
            p = chunk.strip()
            if not p:
                continue
            parts.append(p if p.endswith("%") else f"{p}%")
        return ", ".join(parts) if parts else "—"

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="orders",
    )
    order_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=64,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order {self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column="order_id",
        related_name="items",
    )
    drink = models.ForeignKey(
        Drink,
        on_delete=models.CASCADE,
        db_column="drink_id",
        related_name="order_items",
    )
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_item"

    def __str__(self):
        return f"{self.drink_id} x{self.qty}"


class Staff(models.Model):
    """Cafe employee. Optional link to a Django login user (same person can sign in)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cafe_staff",
    )
    name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=10,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive staff are hidden from clock-in and lists by default.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cafe_staff"
        ordering = ["name"]

    def __str__(self):
        return self.name


class StaffTimeLog(models.Model):
    """One shift segment: clock-in time and optional clock-out (end of work)."""

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="time_logs",
    )
    clock_in = models.DateTimeField(
        help_text="When the staff member started work.",
    )
    clock_out = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the staff member finished work (empty = still on shift).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cafe_staff_time_log"
        ordering = ["-clock_in"]

    @property
    def is_open(self):
        return self.clock_out is None

    def __str__(self):
        return f"{self.staff.name} {self.clock_in:%Y-%m-%d %H:%M}"
