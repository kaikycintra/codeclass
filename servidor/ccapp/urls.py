from django.urls import path

from . import views

app_name = "ccapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("cursos/", views.cursos, name="cursos"),
    path("aulas/", views.aulas, name="aulas"),
    path("user/<str:username>", views.user, name="user")
]
