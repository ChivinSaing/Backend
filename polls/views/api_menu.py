from django.http import JsonResponse

from polls.models import Category, Drink


def menu_api(request):
    """
    Public menu endpoint for frontend.

    Returns:
      {
        "categories": [
            {"id":..., "name":...}, ...,
        ],
        "drinks": [
            {"id":..., "category": {"id":..., "name":...}, ...}, ...
        ]
      }
    """
    if request.method != "GET":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    categories_qs = Category.objects.all().order_by("name")
    drinks_qs = (
        Drink.objects.select_related("category")
        .all()
        .order_by("category__name", "name")
    )

    categories = [{"id": c.id, "name": c.name} for c in categories_qs]

    drinks = []
    for d in drinks_qs:
        image_url = ""
        try:
            if d.image:
                image_url = request.build_absolute_uri(d.image.url)
        except Exception:
            image_url = ""

        # Decimal -> float for JSON friendliness
        try:
            price_value = float(d.price)
        except Exception:
            price_value = str(d.price)

        # Per-size prices for frontend (fallback to default `price`)
        prices = {}
        try:
            sizes = [s.strip() for s in (d.size or "").replace("/", ",").split(",") if s.strip()]
        except Exception:
            sizes = []
        for s in sizes:
            key = s.upper()
            field_value = None
            if key == "S":
                field_value = getattr(d, "price_s", None)
            elif key == "M":
                field_value = getattr(d, "price_m", None)
            elif key == "L":
                field_value = getattr(d, "price_l", None)
            if field_value is None:
                prices[s] = price_value
            else:
                try:
                    prices[s] = float(field_value)
                except Exception:
                    prices[s] = str(field_value)

        drinks.append(
            {
                "id": d.id,
                "name": d.name,
                "size": d.size,
                "price": price_value,
                "prices": prices,
                "sugar": d.sugar_display,
                "stock_qty": d.stock_qty,
                "image_url": image_url,
                "view_count": int(getattr(d, "view_count", 0) or 0),
                "category": {"id": d.category_id, "name": d.category.name},
            }
        )

    return JsonResponse({"categories": categories, "drinks": drinks})

