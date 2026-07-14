from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from polls.forms import StaffForm
from polls.models import Staff, StaffTimeLog
from polls.views.staff import staff_required


@staff_required
def staff_list(request):
    staff_members = Staff.objects.order_by("name")
    return render(
        request,
        "polls/pages/staff_list.html",
        {
            "page_title": "Staff",
            "main_title": "Staff team",
            "active_page": "staff_list",
            "staff_members": staff_members,
        },
    )


@staff_required
def staff_create(request):
    cancel = reverse("staff_list")
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member saved.")
            return redirect("staff_list")
    else:
        form = StaffForm()
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Add staff",
            "main_title": "Add staff member",
            "active_page": "staff_add",
            "form": form,
            "form_heading": "New staff member",
            "cancel_href": cancel,
            "cancel_label": "← Back to staff",
        },
    )


@staff_required
def staff_edit(request, pk):
    member = get_object_or_404(Staff, pk=pk)
    cancel = reverse("staff_list")
    if request.method == "POST":
        form = StaffForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff updated.")
            return redirect("staff_list")
    else:
        form = StaffForm(instance=member)
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Edit staff",
            "main_title": "Edit staff member",
            "active_page": "staff_edit",
            "form": form,
            "form_heading": member.name,
            "cancel_href": cancel,
            "cancel_label": "← Back to staff",
        },
    )


@staff_required
def staff_attendance(request):
    open_shifts = (
        StaffTimeLog.objects.filter(clock_out__isnull=True)
        .select_related("staff")
        .order_by("-clock_in")
    )
    recent_logs = StaffTimeLog.objects.select_related("staff").order_by("-clock_in")[
        :80
    ]
    staff_for_clock_in = Staff.objects.filter(is_active=True).order_by("name")
    return render(
        request,
        "polls/pages/staff_attendance.html",
        {
            "page_title": "Attendance",
            "main_title": "Staff attendance",
            "active_page": "staff_attendance",
            "open_shifts": open_shifts,
            "recent_logs": recent_logs,
            "staff_for_clock_in": staff_for_clock_in,
        },
    )


@staff_required
@require_POST
def staff_clock_in(request):
    staff_id = request.POST.get("staff_id")
    member = get_object_or_404(Staff, pk=staff_id, is_active=True)
    if StaffTimeLog.objects.filter(staff=member, clock_out__isnull=True).exists():
        messages.error(
            request,
            f"{member.name} is already clocked in. Clock out first.",
        )
        return redirect("staff_attendance")
    StaffTimeLog.objects.create(staff=member, clock_in=timezone.now())
    messages.success(request, f"{member.name} clocked in.")
    return redirect("staff_attendance")


@staff_required
@require_POST
def staff_clock_out(request):
    log_id = request.POST.get("log_id")
    log = get_object_or_404(StaffTimeLog, pk=log_id, clock_out__isnull=True)
    log.clock_out = timezone.now()
    log.save(update_fields=["clock_out"])
    messages.success(
        request,
        f"{log.staff.name} clocked out.",
    )
    return redirect("staff_attendance")
