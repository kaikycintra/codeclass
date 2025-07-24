from django.shortcuts import redirect, get_object_or_404
from functools import wraps
from django.http import HttpResponseForbidden
from .models import Aula, Curso, Matricula

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("ccapp:login")
        # Pass the user explicitly to the view function
        return view_func(request, user=request.user, *args, **kwargs) # É necessário usar user=request.user? já dá pra acessar com request.user
    return _wrapped_view

def matricula_required(view_func):
    """
    Decorator para verificar se um usuário está inscrito em um curso
    A ideia é que para acessar conteúdos dentro do curso seja necessário estar matriculado
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'url_curso' in kwargs:
            nome_curso = kwargs['url_curso'].replace("-", " ")
            curso = get_object_or_404(Curso, nome=nome_curso)
        else:
            return HttpResponseForbidden("Algo estranho ocorreu!")
        
        is_enrolled = Matricula.objects.filter(aluno=request.user, curso=curso).exists()
        if not is_enrolled:
            return HttpResponseForbidden("Você precisa estar inscrito neste curso para acessar este conteúdo")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view