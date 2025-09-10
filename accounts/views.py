from requests.models import Request
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Citizen
import json


def login_view(request):
    if request.method == "POST":
        national_id = request.POST.get("national_id")
        code = request.POST.get("verify_code")  # کد تولید شده از JS
        request.session["verify_code"] = code
        request.session["national_id"] = national_id
        request.session["is_signup"] = False
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


def verify(request):
    error = None
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("verify_code")
        national_id = request.session.get("national_id")
        is_signup = request.session.get("is_signup", False)

        print(">>>>>>>>>>>>>>>>> entered_otp:", entered_otp)
        print("saved_otp:", saved_otp)
        print("national_id:", national_id)
        if entered_otp == saved_otp:
            citizen = Citizen.objects.filter(national_id=national_id).first()

            if is_signup and not citizen:
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
            print(">>> OTP صحیح بود، رفتیم به داشبورد")

            return redirect("user_dashboard")
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
    return render(request, "accounts/staff_dashboard.html")
