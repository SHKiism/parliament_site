from django.urls import path
from . import views

urlpatterns = [
    path("<int:req_id>/", views.request_detail, name="request_detail"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),  # فرم ویرایش پروفایل
    path("submit-request/", views.submit_request, name="submit_request"),  # فرم ثبت درخواست جدید
]
