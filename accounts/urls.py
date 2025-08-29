from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("verify/", views.verify, name="verify"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # path("edit-profile/", views.edit_profile, name="edit_profile"),  # فرم ویرایش پروفایل
    # path("submit-request/", views.submit_request, name="submit_request"),  # فرم ثبت درخواست جدید
]
