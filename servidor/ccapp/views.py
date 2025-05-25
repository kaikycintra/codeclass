from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .decorators import login_required
from django.contrib.auth.models import User

@require_http_methods(["GET"])
def index(request):
    if request.user.is_authenticated:
        return redirect("ccapp:cursos")
    return render(request, "ccapp/pages/landing.html")

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        pass
    return render(request, "ccapp/pages/login.html")

#---------------------------------------------------------------
#Funções logadas

@require_http_methods(["GET"])
@login_required
def cursos(request, user):
    # Check if the request is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    layout = "ccapp/partials/block.html" if is_htmx else "ccapp/pages/layout.html"
    return render(request, "ccapp/partials/cursos.html", {
        "layout": layout, 
        "username": user.username,
    })

@require_http_methods(["GET"])
@login_required
def aulas(request, user):
    return render(request, "ccapp/partials/aulas.html", {
        "username": user,
    })

@require_http_methods(["GET"])
@login_required
def aulas(request, user):
    return render(request, "ccapp/partials/aulas.html", {
        "username": user,
    })


@require_http_methods(["GET"])
@login_required
def user(request, username, user):
    profile_user = User.objects.get(username=username)
    is_htmx = request.headers.get("HX-Request") == "true"
    layout = "ccapp/partials/block.html" if is_htmx else "ccapp/pages/layout.html"
    if not profile_user:
        pass
    
    return render(request, "ccapp/partials/user.html", {
        "layout": layout, 
        "username": user.username,
        "profile_username": profile_user.username
    })