from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from polls.forms import CategoryForm
from polls.models import Category
from polls.views.staff import staff_required


@staff_required
def categories_list(request):
    categories = Category.objects.order_by("-id");
    return render(
        request,
        "polls/pages/categories.html",
        {
            "page_title": "Categories",
            "main_title": "Categories",
            "active_page": "categories",
            "categories": categories,
        },
    )


@staff_required
def category_create(request):
    cancel = reverse("categories")
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category saved.")
            return redirect("categories")
    else:
        form = CategoryForm()
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Add category",
            "main_title": "Add category",
            "active_page": "category_add",
            "form": form,
            "form_heading": "New category",
            "cancel_href": cancel,
            "cancel_label": "← Back to categories",
        },
    )


@staff_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    cancel = reverse("categories")
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated.")
            return redirect("categories")
    else:
        form = CategoryForm(instance=category)
    return render(
        request,
        "polls/pages/portal_form.html",
        {
            "page_title": "Edit category",
            "main_title": "Edit category",
            "active_page": "category_edit",
            "form": form,
            "form_heading": category.name,
            "cancel_href": cancel,
            "cancel_label": "← Back to categories",
        },
    )
