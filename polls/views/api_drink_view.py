"""Increment drink view count (used by frontend detail page)."""

from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from polls.models import Drink


@csrf_exempt
def drink_record_view(request, drink_id: int):
    if request.method != "POST":
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        pk = int(drink_id)
    except (TypeError, ValueError):
        return JsonResponse({"detail": "Invalid drink id"}, status=400)

    updated = Drink.objects.filter(pk=pk).update(view_count=F("view_count") + 1)
    if updated == 0:
        return JsonResponse({"detail": "Drink not found"}, status=404)

    return JsonResponse({"ok": True})
