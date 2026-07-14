import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from polls.models import Category, Drink


def _bad_request(detail: str):
    return JsonResponse({"detail": detail}, status=400)


@csrf_exempt
def drinks_api(request):
    """
    Minimal JSON API for Postman testing.

    Note: image upload is not supported here (use the UI form for that).
    """
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        payload = json.loads((request.body or b"").decode("utf-8") or "{}")
    except Exception:
        return _bad_request("Invalid JSON body")

    category_id = payload.get("category_id")
    name = (payload.get("name") or "").strip()
    size = (payload.get("size") or "").strip()
    sugar = (payload.get("sugar") or "").strip()
    stock_qty = payload.get("stock_qty", 0)
    price_raw = payload.get("price")

    if not category_id:
        return _bad_request("Missing required field: category_id")
    if not name:
        return _bad_request("Missing required field: name")
    if not size:
        return _bad_request("Missing required field: size")
    if price_raw is None or price_raw == "":
        return _bad_request("Missing required field: price")

    try:
        category = Category.objects.get(pk=int(category_id))
    except Exception:
        return _bad_request("Invalid category_id (category not found)")

    try:
        price = Decimal(str(price_raw))
    except (InvalidOperation, ValueError):
        return _bad_request("Invalid price (must be a number)")

    try:
        stock_qty_int = int(stock_qty)
        if stock_qty_int < 0:
            return _bad_request("Invalid stock_qty (must be >= 0)")
    except Exception:
        return _bad_request("Invalid stock_qty (must be an integer)")

    drink = Drink.objects.create(
        category=category,
        name=name,
        size=size,
        price=price,
        sugar=sugar or "—",
        stock_qty=stock_qty_int,
    )

    image_url = ""
    try:
        if drink.image:
            image_url = request.build_absolute_uri(drink.image.url)
    except Exception:
        image_url = ""

    return JsonResponse(
        {
            "id": drink.id,
            "name": drink.name,
            "size": drink.size,
            "price": float(drink.price),
            "sugar": drink.sugar_display,
            "stock_qty": drink.stock_qty,
            "image_url": image_url,
            "category": {"id": drink.category_id, "name": drink.category.name},
        },
        status=201,
    )

