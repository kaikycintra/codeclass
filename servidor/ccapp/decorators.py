from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("ccapp:login")
        # Pass the user explicitly to the view function
        return view_func(request, user=request.user, *args, **kwargs)
    return _wrapped_view