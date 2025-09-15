from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .decorators import login_required, matricula_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

from .models import Curso, Aula, Alternativa, RespostaQuestao, ProgressoAula, Questao, Matricula, Comentario, Atividade

@require_http_methods(["GET"])
def index(request):
    if request.user.is_authenticated:
        return redirect("ccapp:cursos")
    return render(request, "ccapp/pages/landing.html")

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Entrar por email, se user não existe então 
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect("ccapp:cursos")
        else:
            return render(request, "ccapp/pages/login.html", {
                "message": "Credenciais inválidas"
            })

    return render(request, "ccapp/pages/login.html", {
        "message": None,
    })
    
@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Checa se usuário ou email já estão em uso
        if User.objects.filter(email=email).exists():
            return render(request, "ccapp/pages/cadastro.html", {
                "message": "Email já está em uso"
            })
        elif User.objects.filter(username=username).exists():
            return render(request, "ccapp/pages/cadastro.html", {
                "message": "Nome de usuário já em uso"
            })
        
        # Checa se a senha atende critérios mínimos
        if (password != confirm_password):
            return render(request, "ccapp/pages/cadastro.html", {
                "message": "As senhas não coincidem!"
            })
        
        if (len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password)):
            return render(request, "ccapp/pages/cadastro.html", {
                "message": "A senha deve ter no mínimo 8 caracteres e conter letras e números!"
            })
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("ccapp:cursos")

    return render(request, "ccapp/pages/cadastro.html")


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect("ccapp:login")

#---------------------------------------------------------------
#Funções logadas

@never_cache
@require_http_methods(["GET"])
@login_required
def cursos(request, user):
    # Nota: precisei fazer uma verificação a mais nesta parte para saber se era request htmx ou não, só o get_layout não dava conta
    is_htmx = request.headers.get("HX-Request") == "true"
    hx_target = request.headers.get("HX-Target")

    filtro = request.GET.get('filtro', None)
    cursos_matriculados = Matricula.objects.filter(aluno=user).values_list('curso__nome', flat=True)
    if filtro == 'meus':
        lista_cursos = Curso.objects.filter(nome__in=cursos_matriculados)
    elif filtro == 'outros':
        lista_cursos = Curso.objects.exclude(nome__in=cursos_matriculados)
    else:
        lista_cursos = Curso.objects.all()
    
    dados_progresso = {}
    for nome in cursos_matriculados:
        curso = Curso.objects.get(nome=nome)
        dados_progresso[curso.id] = curso.get_progresso_curso(user)
        
    context = {
        "username": user.username,
        "cursos": lista_cursos,
        "cursos_matriculados": cursos_matriculados,
        "dados_progresso": dados_progresso,
    }

    if is_htmx and hx_target=="lista-cursos":
        return render(request, "ccapp/partials/lista_cursos.html", context)
    
    context["layout"] = get_layout(request)
    return render(request, "ccapp/partials/cursos.html", context)

@never_cache
@require_http_methods(["POST"])
@login_required
def matricular_curso(request, user, url_curso):
    nome_curso = url_curso.replace("-", " ")
    curso = get_object_or_404(Curso, nome=nome_curso)
    Matricula.objects.get_or_create(aluno=user, curso=curso)

    # Fix para conseguir redirecionar à pagina certa
    redirect_url = reverse('ccapp:aulas', kwargs={'url_curso': url_curso})
    if request.headers.get('HX-Request') == 'true':
        return HttpResponse(status=204, headers={'HX-Redirect': redirect_url})

    return redirect(redirect_url)

@never_cache
@require_http_methods(["GET"])
@login_required
@matricula_required
def aulas(request, url_curso, user):
    layout = get_layout(request)
    nome_curso = url_curso.replace("-", " ")
    curso = Curso.objects.get(nome=nome_curso)

    aulas_concluidas = ProgressoAula.objects.filter(
        aluno=user,
        aula__curso=curso,
        concluida=True
    ).values_list('aula_id', flat=True)
    todas_as_aulas = curso.aulas.order_by('num')
    proxima_aula = todas_as_aulas.exclude(id__in=aulas_concluidas).first()


    return render(request, "ccapp/partials/aulas.html", {
        "layout": layout,
        "username": user,
        "curso": curso.nome,
        "aulas": todas_as_aulas,
        "aulas_concluidas": aulas_concluidas,
        "proxima_aula": proxima_aula,
    })
    
@never_cache
@require_http_methods(["GET"])
@login_required
@matricula_required
def aula(request, url_curso, url_aula, user):
    layout = get_layout(request)
    nome_aula = url_aula.replace("-", " ")

    aula_obj = get_object_or_404(Aula, nome=nome_aula)
    questoes = aula_obj.questoes.all()

    progresso, created = ProgressoAula.objects.get_or_create(aluno=user, aula=aula_obj)

    return render(request, "ccapp/partials/class.html", {
        "layout": layout,
        "username": user,
        "aula": Aula.objects.get(nome=nome_aula),
        "progresso": progresso,
    })

@login_required
@require_http_methods(["POST"])
def submeter_atividade(request, user, atividade_id):
    """
    Gerencia o Submit de uma única atividade
    """
    atividade = get_object_or_404(Atividade, pk=atividade_id)
    aula = atividade.aula
    aluno = user

    # Processa o tipo CHECKBOX
    if atividade.tipo == Atividade.TipoAtividade.CHECKBOX:
        ProgressoAula.objects.altera_status_conclusao(user=user, aula=aula)

    progresso_atualizado = ProgressoAula.objects.filter(aluno=aluno, aula=aula).first()

    context = {
        "aula": aula,
        "progresso": progresso_atualizado
    }

    return render(request, "ccapp/partials/atividades.html", context)

@never_cache
@require_http_methods(["GET"])
@login_required
def user(request, username, user):
    #profile_user = User.objects.get(username=username) -> O recomendado é usar o get_object_or_404
    profile_user = get_object_or_404(User, username=username)
    layout = get_layout(request)

    cursos_do_user = Curso.objects.filter(matriculas__aluno=profile_user)

    dados_progresso = {}
    for curso in cursos_do_user:
        dados_progresso[curso.id] = curso.get_progresso_curso(profile_user)

    comentarios = profile_user.comentarios_feitos

    return render(request, "ccapp/partials/user.html", {
        "layout": layout, 
        "username": user.username,
        "profile_username": profile_user.username,
        "cursos_do_user": cursos_do_user,
        "dados_progresso": dados_progresso,
        "biografia": profile_user.perfil.biografia,
        "comentarios": comentarios,
    })

@never_cache
@require_http_methods(["POST"])
@login_required
def curtir_comentario(request, id_comentario, user):
    comentario = get_object_or_404(Comentario, id=id_comentario)
    
    if user in comentario.curtidas.all():
        comentario.curtidas.remove(user)
    else:
        comentario.curtidas.add(user)

    return render(request, "ccapp/partials/like.html", {
        "comentario": comentario,
    })

@never_cache
@require_http_methods(["GET"])
@login_required
def obter_comentarios(request, id_aula, user):
    aula = get_object_or_404(Aula, pk=id_aula)

    comentarios_pai = aula.comentarios_aula.filter(parent=None)
    context = {
        'aula': aula,
        'comentarios': comentarios_pai,
    }

    return render(request, "ccapp/partials/comentarios.html", context)

@never_cache
@require_http_methods(["POST"])
@login_required
def postar_comentario(request, id_aula, user):
    aula = get_object_or_404(Aula, pk=id_aula)
    texto = request.POST.get('texto')

    if texto:
        Comentario.objects.create(aula=aula, user=user, texto=texto)
        # Lidar com parentes aqui mesmo?

    comentarios_pai = aula.comentarios_aula.filter(parent=None)
    context = {
        'aula': aula,
        'comentarios': comentarios_pai,
    }

    return render(request, "ccapp/partials/comentarios.html", context)

# Provavelmente seria melhor refazer a função de cima para poder usar na mesma url da api, mas deixei aqui por simplicidade
@never_cache
@require_http_methods(["GET"])
@login_required
def responder_comentario(request, id_comentario, user):
    comentario_pai = get_object_or_404(Comentario, pk=id_comentario)

    context = {
        "comentario": comentario_pai,
        "is_reply": True,
    }

    return render(request, "ccapp/partials/responder_comentario.html", context)

@never_cache
@require_http_methods(["POST"])
@login_required
def postar_resposta(request, id_comentario, user):
    comentario_pai = get_object_or_404(Comentario, pk=id_comentario)
    aula=comentario_pai.aula
    texto=request.POST.get('texto')
    if texto:
        Comentario.objects.create(
            user=user,
            aula=aula,
            texto=texto,
            parent=comentario_pai
        )

    # Re-renderiza os comentarios
    comentarios_pai = aula.comentarios_aula.filter(parent=None)
    context = {
        'aula': aula,
        'comentarios': comentarios_pai,
    }

    return render(request, "ccapp/partials/comentarios.html", context)


## Função para retornar layout certo
def get_layout(request):
    return "ccapp/partials/block.html" if request.headers.get("HX-Request") == "true" else "ccapp/pages/layout.html"