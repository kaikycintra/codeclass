from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

from .models import Curso, Aula

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
    # Check if the request is an HTMX request
    layout = get_layout(request)
    return render(request, "ccapp/partials/cursos.html", {
        "layout": layout, 
        "username": user.username,
        "cursos": Curso.objects.all()
    })

@never_cache
@require_http_methods(["GET"])
@login_required
def aulas(request, url_curso, user):
    layout = get_layout(request)
    nome_curso = url_curso.replace("-", " ")
    curso = Curso.objects.get(nome=nome_curso)
    return render(request, "ccapp/partials/aulas.html", {
        "layout": layout,
        "username": user,
        "curso": curso.nome,
        "aulas": curso.aulas.all()
    })
    
@never_cache
@require_http_methods(["GET"])
@login_required
def aula(request, url_curso, url_aula, user):
    layout = get_layout(request)
    nome_aula = url_aula.replace("-", " ")
    return render(request, "ccapp/partials/class.html", {
        "layout": layout,
        "username": user,
        "aula": Aula.objects.get(nome=nome_aula)
    })


@never_cache
@require_http_methods(["GET"])
@login_required
def user(request, username, user):
    profile_user = User.objects.get(username=username)
    layout = get_layout(request)
    if not profile_user:
        pass
    
    return render(request, "ccapp/partials/user.html", {
        "layout": layout, 
        "username": user.username,
        "profile_username": profile_user.username
    })

## Função para retornar layout certo
def get_layout(request):
    return "ccapp/partials/block.html" if request.headers.get("HX-Request") == "true" else "ccapp/pages/layout.html"