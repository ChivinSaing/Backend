from django.shortcuts import render

from polls.views.staff import staff_required


@staff_required
def dashboard(request):
    return render(
        request,
        "polls/pages/dashboard.html",
        {
            "page_title": "Dashboard",
            "main_title": "Cafe Admin Portal",
            "active_page": "dashboard",
        },
    )
