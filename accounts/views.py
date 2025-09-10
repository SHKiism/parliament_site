from django.urls import reverse

from requests.models import Request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Citizen, Employee
import json


def login_view(request):
    if request.method == "POST":
        national_id = request.POST.get("national_id")
        code = request.POST.get("verify_code")
        request.session["verify_code"] = code
        request.session["national_id"] = national_id
        request.session["is_signup"] = False
        request.session["user_type"] = "citizen"
        print("entered_otp:", code)
        return render(request, "accounts/verify.html", {"code": code})

    return render(request, "accounts/login.html")


def signup(request):
    if request.method == "POST":
        national_id = request.POST.get("national_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        code = request.POST.get("verify_code")  # کد تولید شده از JS

        request.session["verify_code"] = code
        request.session["national_id"] = national_id
        request.session["is_signup"] = True
        request.session["user_type"] = "citizen"
        request.session["first_name"] = first_name
        request.session["last_name"] = last_name
        request.session["phone"] = phone

        print("entered_otp:", code)
        return render(request, "accounts/verify.html", {"code": code})
    return render(request, "accounts/signup.html")


def check_national_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        national_id = data.get("national_id")
        exists = Citizen.objects.filter(national_id=national_id).exists()
        print(f"Checked national_id={national_id}, exists={exists}")
        return JsonResponse({"exists": exists})
    return JsonResponse({"exists": False})


def staff_login(request):
    request.session["user_type"] = "employee"
    if request.method == "POST":
        national_id = request.POST.get("national_id")
        code = request.POST.get("verify_code")
        request.session["verify_code"] = code
        request.session["national_id"] = national_id
        request.session["is_signup"] = False

        return render(request, "accounts/verify.html", {"code": code})

    return render(request, "accounts/staff_login.html")


def staff_login_check(request):
    if request.method == "POST":
        data = json.loads(request.body)
        national_id = data.get("national_id")
        exists = Employee.objects.filter(national_id=national_id).exists()

        return JsonResponse({"exists": exists})

    return JsonResponse({"exists": False})


def verify(request):
    error = None
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("verify_code")
        national_id = request.session.get("national_id")
        is_signup = request.session.get("is_signup", False)
        user_type = request.session["user_type"]

        if entered_otp == saved_otp and user_type == "citizen":
            citizen = Citizen.objects.filter(national_id=national_id).first()

            if is_signup:
                # ساخت کاربر جدید
                phone = request.session.get("phone")
                first_name = request.session.get("first_name")
                last_name = request.session.get("last_name")
                citizen = Citizen.objects.create(
                    national_id=national_id,
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name,
                )
            elif not citizen:
                error = "کاربری با این کد ملی پیدا نشد."
                return render(request, "accounts/verify.html", {"error": error})
            # ورود موفق → ذخیره وضعیت در session
            request.session["is_logged_in"] = True
            request.session["national_id"] = citizen.national_id
            return redirect("user_dashboard")
        elif entered_otp == saved_otp and user_type == "employee":
            print(request)
            return redirect(reverse('staff_dashboard'))
        else:
            error = "کد وارد شده صحیح نیست. لطفاً دوباره تلاش کنید."

    return render(request, "accounts/verify.html", {"error": error})


def user_dashboard(request):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    national_id = request.session.get("national_id")

    # داشبورد کاربر: فقط درخواست‌های خودش
    user_requests = Request.objects.filter(citizen__national_id=national_id).order_by("-created_at")
    return render(request, "accounts/user_dashboard.html", {"requests": user_requests})


def staff_dashboard(request):
    print(">>> staff_dashboard called")
    print(request)
    all_requests = Request.objects.all().order_by("-created_at")

    stats = {
        'total': all_requests.count(),
        'pending': all_requests.filter(status='pending').count(),
        'in_progress': all_requests.filter(status='in_progress').count(),
        'done': all_requests.filter(status='done').count(),
        'rejected': all_requests.filter(status='rejected').count(),
    }

    # اعمال فیلتر
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', 'all')

    filtered_requests = all_requests
    if search_query:
        filtered_requests = filtered_requests.filter(title__icontains=search_query)
    if status_filter != 'all':
        filtered_requests = filtered_requests.filter(status=status_filter)

    context = {
        'stats': stats,
        'requests': filtered_requests,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    print(filtered_requests)
    print(stats)

    return render(request, 'accounts/staff_dashboard.html', context)


def edit_profile(request):
    national_id = request.session.get("national_id")
    citizen = Citizen.objects.get(national_id=national_id)

    if request.method == "POST":
        citizen.first_name = request.POST.get("first_name")
        citizen.last_name = request.POST.get("last_name")
        citizen.phone = request.POST.get("phone")
        citizen.save()
        return redirect("user_dashboard")

    return render(request, "accounts/edit_profile.html", {"citizen": citizen})
