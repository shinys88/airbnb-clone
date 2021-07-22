from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login2", views.LoginFormView.as_view(), name="login2"),
    path("logout", views.log_out, name="logout")
    ]
