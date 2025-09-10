# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from accounts.models import Citizen
from .models import Request


def request_detail(request, req_id):
    req = get_object_or_404(Request, id=req_id)
    return render(request, "requests/detail.html", {"request_obj": req})


def submit_request(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        attachment = request.FILES.get("attachment")

        national_id = request.session.get("national_id")  # فرض بر اینه که کاربر لاگین کرده
        if not national_id:
            messages.error(request, "لطفاً ابتدا وارد شوید.")
            return redirect("login")


        citizen, created = Citizen.objects.get_or_create(national_id=national_id)

        Request.objects.create(
            citizen=citizen,
            title=title,
            description=description,
            attachment=attachment
        )

        messages.success(request, "درخواست شما با موفقیت ثبت شد.")
        return redirect("user_dashboard")

    return render(request, "requests/submit_request.html")


def edit_profile(request):
    return render(request, "requests/edit_profile.html")
