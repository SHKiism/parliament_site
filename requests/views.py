# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from accounts.models import Citizen
from .models import Request


def request_detail(request, req_id):
    req = get_object_or_404(Request, id=req_id)
    return render(request, "requests/review_request.html", {"request_obj": req})


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


def review_request_staff(request, pk):
    req = get_object_or_404(Request, pk=pk)

    if request.method == "POST":
        new_status = request.POST.get("status")
        response_text = request.POST.get("response")

        if new_status:
            req.status = new_status
        if response_text:
            req.response = response_text

        req.save()
        return redirect("staff_dashboard")  # بعد از ذخیره برگرد به داشبورد

    return render(request, "requests/review_request_staff.html", {"req": req})
