import random
from .models import User
from requests.models import Request
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        national_id = request.POST.get("national_id")
        code = request.POST.get("verify_code")  # کد تولید شده از JS
        request.session["verify_code"] = code
        request.session["national_id"] = national_id
        print("entered_otp:", code)
        return render(request, "accounts/verify.html", {"code": code})

    return render(request, "accounts/login.html")

def verify(request):
    error = None
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("verify_code")
        national_id = request.session.get("national_id")
        print(">>>>>>>>>>>>>>>>> entered_otp:", entered_otp)
        print("saved_otp:", saved_otp)
        print("national_id:", national_id)
        if entered_otp == saved_otp:
            user, created = User.objects.get_or_create(username=national_id,defaults={"national_id": national_id})
            # user = User.objects.get(id=national_id)
            user.is_verified = True
            user.save()

            # ورود موفق → ذخیره وضعیت در session
            request.session["is_logged_in"] = True
            request.session["user_id"] = user.id
            # request.session["role"] = user.role
            request.session["role"] = getattr(user, "role", "user")  # اگر role موجود باشد
            print(">>> OTP صحیح بود، رفتیم به داشبورد")

            return redirect("dashboard")
        else:
            error = "کد وارد شده صحیح نیست. لطفاً دوباره تلاش کنید."

    return render(request, "accounts/verify.html", {"error": error})
    # return render(request, "accounts/verify.html")

def dashboard(request):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    user_id = request.session.get("user_id")
    role = request.session.get("role")

    if role == "employee":
        # داشبورد کارمند: همه درخواست‌ها
        all_requests = Request.objects.all().order_by("-created_at")
        return render(request, "accounts/staff_dashboard.html", {"requests": all_requests})
    else:
        # داشبورد کاربر: فقط درخواست‌های خودش
        user_requests = Request.objects.filter(user_id=user_id).order_by("-created_at")
        return render(request, "accounts/user_dashboard.html", {"requests": user_requests})
