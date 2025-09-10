from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("verify/", views.verify, name="verify"),
    path("signup/", views.signup, name="signup"),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path("staff_dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path('staff_login_check/', views.staff_login_check, name='staff_login_check'),
    path("staff_login/", views.staff_login, name="staff_login"),
    path('check_national_id/', views.check_national_id, name='check_national_id'),
]
