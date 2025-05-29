from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "ccapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("cursos/", views.cursos, name="cursos"),
    path("curso/<str:url_curso>/", views.aulas, name="aulas"),
    path("curso/<str:url_curso>/<str:url_aula>", views.aula, name="aula"),
    path("user/<str:username>", views.user, name="user")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)