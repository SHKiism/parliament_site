from django.urls import path
from . import views

urlpatterns = [
    path("<int:req_id>/", views.request_detail, name="request_detail"),
]
