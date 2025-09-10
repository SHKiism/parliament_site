from django.urls import path
from . import views

urlpatterns = [
    path("<int:req_id>/", views.request_detail, name="request_detail"),
    path("submit-request/", views.submit_request, name="submit_request"),  # فرم ثبت درخواست جدید
    path('review_request_staff/<int:pk>/', views.review_request_staff, name='review_request_staff'),
]
