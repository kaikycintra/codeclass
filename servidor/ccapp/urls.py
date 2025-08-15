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
    path("user/<str:username>", views.user, name="user"),
    path('submit-answers/<str:url_aula>/', views.submit_answers, name='submit_answers'),
    path("matricular/<str:url_curso>/", views.matricular_curso, name="matricular_curso"),
    path("curtir-comentario/<int:id_comentario>/", views.curtir_comentario, name="curtir_comentario"),
    path("obter-comentarios/<int:id_aula>/", views.obter_comentarios, name="obter_comentarios"),
    path("postar-comentario/<int:id_aula>/", views.postar_comentario, name="postar_comentario"),
    path("responder-comentario/<int:id_comentario>/", views.responder_comentario, name="responder_comentario"),
    path("postar-resposta/<int:id_comentario>/", views.postar_resposta, name="postar_resposta"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)