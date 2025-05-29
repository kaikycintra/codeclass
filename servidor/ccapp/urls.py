from django.urls import path

from . import views

app_name = "ccapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("cursos/", views.cursos, name="cursos"),
    path("cursos/aulas/", views.aulas, name="aulas"),
    path("user/<str:username>", views.user, name="user")
]
