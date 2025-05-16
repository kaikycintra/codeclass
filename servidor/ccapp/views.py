from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def index(request):
    return render(request, "ccapp/landing.html")

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        pass
    return render(request, "ccapp/login.html")